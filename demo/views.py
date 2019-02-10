from django.shortcuts import render, HttpResponse, redirect
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

from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import BookForm

def book_create(request):
    data = dict()

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = BookForm()

    context = {'form': form}
    data['html_form'] = render_to_string('demo/partial_book_create.html',
        context,
        request=request
    )
    return JsonResponse(data)


def index(request):
    return render(request, 'demo/index.html')

def book_list(request):
    books = Book.objects.all()
    return render(request, 'demo/booklist.html', {'books': books})


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
            context['display_details'] = True
            print ('in get basic')



        elif 'change_val' in request.GET:
            print ('in get button')
            vars=botVariables()
            new_fields=vars.type_backtest_variables[request.session['backtest_type']]

            context['display_details'] = True



        else:
            print ('in get beggining')
            context['display_details'] = False
            # context['display_details'] = True
            new_fields = {
                    'caca'  : forms.IntegerField(initial=123),
                    'culo': forms.IntegerField(initial=123),
                    }
    if request.method == "POST":
        for key in request.POST.keys():
            if key != 'csrfmiddlewaretoken':
                content[key] = request.POST[key]
        vars=botVariables()
        new_fields=vars.type_backtest_variables[request.session['backtest_type']]
        ckb = BacktestModel.objects.create(backtest_type = request.session['backtest_type'],pairChosen = request.session['pairChosen'],periodChosen = request.session['periodChosen'], backtest_details =new_fields)
        context['display_details'] = True

        return render(request, 'demo/dynamic.html', context)



    print ('in general')
    DynamicDetailsForm = type('DynamicDetailsForm',
            (BacktestDetailsForm,),
            new_fields)


    DetailForm = DynamicDetailsForm(content)
    context['details_form'] = DetailForm
    context['backtest_form'] = BacktestForm(request.POST or None)
    # print (context)
    return render(request, "demo/dynamic.html", context)
