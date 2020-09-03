from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import TemplateView
from django.forms.models import model_to_dict
from django.http import JsonResponse

from payments.forms import PaymentForm
from payments.tasks import add
from payments.dispatcher import Dispatcher

from django_celery_results.models import TaskResult
# Create your views here.


class PaymentView(TemplateView):
    
    form_class = PaymentForm
    template_name = "payment.html"

    dispatch_method = Dispatcher.dispatch

    
    def get(self, request):

        form = self.form_class()

        tasks = list(map(model_to_dict, TaskResult.objects.all().order_by('-date_created')))

        return render(request, self.template_name, {'form':form, 'tasks':tasks}, status=200)

    def post(self, request):
        
        form = self.form_class(request.POST)

        tasks = list(map(model_to_dict, TaskResult.objects.all()))
        TaskResult.objects.all().delete()
        if form.is_valid():
            payment = form.save()
            payment = model_to_dict(payment)
            # send payment to Dispatcher
            self.dispatch_method.delay(payment)
            form = self.form_class()
            return render(request, self.template_name, {'form':form, 'tasks':tasks}, status=200)
        else:
            return render(request, self.template_name, {'form':form, 'tasks':tasks}, status=400)
    


