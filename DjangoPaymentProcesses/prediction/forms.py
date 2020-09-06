from django import forms
from prediction.models import Prediction
from django.forms import ModelForm

class PredictionForm():

    class Meta:
        model = Prediction
        fields =["date"]

    