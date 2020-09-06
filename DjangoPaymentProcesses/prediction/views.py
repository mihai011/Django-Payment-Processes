from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.forms.models import model_to_dict

from prediction.forms import PredictionForm

from django_celery_results.models import TaskResult
from http import HTTPStatus

import json

def process_task_result(task):

    data = {}
    data["resolver"] = json.loads(task.result)["resolver"]
    data["task_id"] = task.task_id
    data["status"] = task.status

    return data

class PredictionView(TemplateView):

    form_class = PredictionForm
    template_name = "prediction.html"

    def get(self, request):

        form = self.form_class()
        
        return render(request, self.template_name, {'form':form}, status=HTTPStatus.OK)

    def post(self, request):

        form = self.form_class(request.POST)

        