from django.shortcuts import render

# Create your views here.
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pickle
import numpy as np
from .serializers import PredictSerializer
from sklearn.exceptions import NotFittedError

class PredictView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Diretório da aplicação Django
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Caminho para o modelo e scaler
        model_path = os.path.join(base_dir, 'predictions', 'best_model.pkl')
        scaler_path = os.path.join(base_dir, 'predictions', 'scaler.pkl')
        
        try:
            # Carregando o modelo e o scaler
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
        except (FileNotFoundError, pickle.UnpicklingError) as e:
            self.model = None
            self.scaler = None
            print(f"Error loading model or scaler: {e}")

    def post(self, request, *args, **kwargs):
        if not self.model or not self.scaler:
            return Response({'error': 'Model or scaler not loaded properly.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = PredictSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            sla = data['SLA']
            banda_up = data['Banda_UP']
            banda_down = data['Banda_DOWN']
            features = np.array([[sla, banda_up, banda_down]])

            try:
                features_scaled = self.scaler.transform(features)
                prediction = self.model.predict(features_scaled)
                # Arredondando o valor para duas casas decimais
                prediction_rounded = round(prediction[0], 2)
                return Response({'mensalidade': prediction_rounded}, status=status.HTTP_200_OK)
            except NotFittedError as e:
                return Response({'error': f'Model is not fitted: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({'error': f'Error during prediction: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.http import HttpResponse

def index(request):
    return HttpResponse("Bem-vindo à minha aplicação de previsões!")