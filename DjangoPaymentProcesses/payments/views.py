from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.forms.models import model_to_dict

from payments.forms import PaymentForm

from django_celery_results.models import TaskResult
from http import HTTPStatus

import json
# Create your views here.


def process_task_result(task):

    data = {}
    data["resolver"] = json.loads(task.result)["resolver"]
    data["task_id"] = task.task_id
    data["status"] = task.status

    return data


def handler500(request, *args, **argv):
    
    return render(request, "500.html", {}, status=HTTPStatus.INTERNAL_SERVER_ERROR)


class PaymentView(TemplateView):
    
    form_class = PaymentForm
    template_name = "payment.html"

    
    def get(self, request):

        # TaskResult.objects.all().delete()

        form = self.form_class()
        tasks = TaskResult.objects.all().order_by('-date_created')

        tasks = list(map(process_task_result,tasks))

        return render(request, self.template_name, {'form':form, 'tasks':tasks}, status=HTTPStatus.OK)

    def post(self, request):
        
        form = self.form_class(request.POST)

        tasks = list(map(model_to_dict, TaskResult.objects.all().order_by('-date_created')))
        
        if form.is_valid():
            form.save()
            form = self.form_class()
            return render(request, self.template_name, {'form':form, 'tasks':tasks}, status=HTTPStatus.OK)
        else:
            return render(request, self.template_name, {'form':form, 'tasks':tasks}, status=HTTPStatus.BAD_REQUEST)
    


