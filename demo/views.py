from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse

from hello_celery.celery import app
from django_celery_results.models import TaskResult
from celery.result import AsyncResult
from .tasks import increment

from .forms import *
from .models import *

import json
import pdb

from trader_python.botvariables import botVariables


def index(request):
    return render(request, 'demo/index.html')


def dynamic(request):
    context = {}
    content = {}
    if request.session.get('initialised', False):
        request.session['initialised']=true
        request.session['recipe_name']='undefined'

    if request.session['recipe_name'] == 'moving_averages':
        print ('recipe burger')
        new_fields = {
            'cheese': forms.IntegerField(),
            'ham'   : forms.IntegerField(),
            'onion' : forms.IntegerField(),
            'bread' : forms.IntegerField(),
            'ketchup': forms.IntegerField()}
    elif request.session['recipe_name'] == 'bollinger_bands':
        print ('recipe pancake')
        new_fields = {
            'milk'  : forms.IntegerField(),
            'butter': forms.IntegerField(),
            'honey' : forms.IntegerField(),
            'eggs'  : forms.IntegerField()}
    else:
        request.session['recipe_name']='undefined'
        new_fields = {
            }

    if request.method == 'POST':
        if 'recipe_name' in request.POST:
            request.session['recipe_name'] = str(request.POST['recipe_name'])
            default=request.session['recipe_name']+'_default'
            vars=botVariables()
            deff=vars.type_backtest_variables[default]
            ckb = BacktestType.objects.create(backtest_type = request.session['recipe_name'], backtest_details =deff )
            print ('recipe name')
        else:
            for key in request.POST.keys():
                if key != 'csrfmiddlewaretoken':
                    content[key] = request.POST[key]
            ckb = BacktestType.objects.create(backtest_type = request.session['recipe_name'], backtest_details = json.dumps(content))

    DynamicDetailsForm = type('DynamicDetailsForm',
            (BacktestDetailsForm,),
            new_fields)

    DetailForm = DynamicDetailsForm(content)
    context['ingridients_form'] = DetailForm
    context['cookbook_form']    = BacktestType(request.POST or None)
    return render(request, "demo/dynamic.html", context)
