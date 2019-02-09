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
    if request.method == 'GET':
        if 'backtest_type' in request.GET:
            request.session['backtest_type'] = str(request.GET['backtest_type'])
            request.session['pairChosen'] = str(request.GET['pairChosen'])
            request.session['periodChosen'] = str(request.GET['periodChosen'])
            vars=botVariables()
            new_fields=vars.type_backtest_variables[request.session['backtest_type']]

            print ('in get')

        else:
            new_fields = {
                    'caca'  : forms.IntegerField(initial=123),
                    'culo': forms.IntegerField(initial=123),
                    }
    else:
        new_fields = {
                'milk'  : forms.IntegerField(),
                'butter': forms.IntegerField(),
                'honey' : forms.IntegerField(),
                'eggs'  : forms.IntegerField()}
    # if request.method == 'POST':
    #     if 'backtest_type' in request.POST:
    #         request.session['backtest_type'] = str(request.POST['backtest_type'])
    #         default=request.session['backtest_type']+'_default'
    #         vars=botVariables()
    #         deff=vars.type_backtest_variables[default]
    #         ckb = BacktestModel.objects.create(backtest_type = request.session['backtest_type'], backtest_details =deff )
    #         print ('recipe name')
    #     else:
    #         for key in request.POST.keys():
    #             if key != 'csrfmiddlewaretoken':
    #                 content[key] = request.POST[key]
    #
    # if request.session.get('initialised', False):
    #     request.session['initialised']=True
    #     request.session['backtest_type']='undefined'
    #
    # if request.session['backtest_type'] == 'moving_averages':
    #     print ('recipe burger')
    #     new_fields = {
    #         'cheese': forms.IntegerField(),
    #         'ham'   : forms.IntegerField(),
    #         'onion' : forms.IntegerField(),
    #         'bread' : forms.IntegerField(),
    #         'ketchup': forms.IntegerField()}
    # elif request.session['backtest_type'] == 'bollinger_bands':
    #     print ('recipe pancake')
    #     new_fields = {
    #         'milk'  : forms.IntegerField(),
    #         'butter': forms.IntegerField(),
    #         'honey' : forms.IntegerField(),
    #         'eggs'  : forms.IntegerField()}
    # else:
    #     request.session['backtest_type']='undefined'
    #     new_fields = {
    #         }

    print ('in general')
    DynamicDetailsForm = type('DynamicDetailsForm',
            (BacktestDetailsForm,),
            new_fields)


    DetailForm = DynamicDetailsForm(content)
    context['details_form'] = DetailForm

    context['backtest_form']    = BacktestForm(request.GET or None)
    return render(request, "demo/dynamic.html", context)
