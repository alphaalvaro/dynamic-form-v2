from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
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
from .forms import BookForm, BacktestDetailsForm

def book_create(request):
    if request.method == 'POST':
        DetailForm = BacktestDetailsForm(request.POST)
    else:
        if 'backtest_type' in request.GET:
            request.session['backtest_type'] = str(request.GET['backtest_type'])
            vars=botVariables()
            new_fields=vars.type_backtest_variables[request.session['backtest_type']]
            DynamicDetailsForm = type('DynamicDetailsForm',
                    (BacktestDetailsForm,),
                    new_fields)
            DetailForm = DynamicDetailsForm()

    print ("to save_book_form")
    return save_book_form(request, DetailForm, 'demo/partial_book_create.html')

def save_book_form(request, form, template_name):
    data = dict()
    content={}
    if request.method == 'POST':
        print ("Trying to init session")
        if form.is_valid():
            print ("session init")
            for key in request.POST.keys():
                if key != 'csrfmiddlewaretoken':
                    content[key] = request.POST[key]
            request.session['initialised']=True
            data['backtest_details']=content

            data['form_is_valid'] = True
            books = Book.objects.all()
            data['html_book_list'] = render_to_string('demo/partial_backtest_list.html', {
                'books': books
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def book_list(request):
    books = Book.objects.all()
    return render(request, 'demo/booklist.html', {'books': books})

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
    else:
        form = BookForm(instance=book)
    return save_book_form(request, form, 'demo/partial_book_update.html')


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True
        books = Book.objects.all()
        data['html_book_list'] = render_to_string('demo/partial_backtest_list.html', {
            'books': books
        })
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('demo/partial_book_delete.html', context, request=request)
    return JsonResponse(data)

def index(request):
    return render(request, 'demo/index.html')


def dynamic(request):
    context = {}
    if request.session.get('initialised', False):
        print ('initializing session')
        request.session['initialised']=True
        request.session['backtest_details']='undefined'

    if request.method == "POST":
        backtest_details=request.session.get('backtest_details')
        backtestForm = BacktestForm(request.POST)
        backtestForm.save()
        # backtest= backtestForm.save(commit=False)
        # backtest.backtest_details=backtest_details
        # backtest.save()
        print ('in general')


    context['books'] = Book.objects.all()
    context['backtest_form'] = BacktestForm(request.POST or None)
    # print (context)
    return render(request, "demo/dynamic.html", context)
