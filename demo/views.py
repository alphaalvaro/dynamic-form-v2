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


def index(request):
    return render(request, 'demo/index.html')

def test_page(request):
    try:
        currentProcess = TaskResult.objects.last()
        if currentProcess.status == 'PROGRESS':
            return HttpResponseRedirect(reverse('demo:start_test') + '?job=' + currentProcess.task_id)
        else:
            return render(request, 'demo/test.html')
    except:
        return render(request, 'demo/test.html')

def start_test(request):
    if 'job' in request.GET:
        job_id = request.GET['job']
        job = AsyncResult(job_id)
        data = job.result
        context = {
                'check_status': 1,
                'data': "",
                'state': 'STARTING...',
                'task_id': job_id
		}
        return render(request, 'demo/test.html', context)
    else:
        job = increment.delay(120)
        print ("Celery job ID:  {}.".format(job))
        return HttpResponseRedirect(reverse('demo:start_test') + '?job=' + job.id)

def update_status(request):
    print ("Update on: {}.".format(request.GET))
    if 'task_id' in request.GET.keys():
        task_id = request.GET['task_id']
        task = AsyncResult(task_id)
        result = task.result
        status = task.status
    else:
        status = 'UNDEFINED!'
        result = 'UNDEFINED!'
    try:
        json_data = {
            'status': status,
            'state': result['status'],
            'iter' : result['iteration']
            }
    except TypeError:
        json_data = {
            'status': status,
            'state': 'FINISHED',
            'iter' : -1
            }
    return JsonResponse(json_data)

def abort_test(request):
    try:
        currentProcess = TaskResult.objects.last()
        task_id = currentProcess.task_id
        app.control.revoke(task_id, terminate=True)
        return HttpResponseRedirect(reverse('demo:start_test') + '?job=' + currentProcess.task_id)
    except:
        return HttpResponseRedirect(reverse('demo:start_test'))


## Dynamic forms demo
def nondynamic(request):
    context = {}

    ing = Ingridients.objects.last()
    if ing == None:
        ing = Ingridients.objects.create()

    ckb = CookBook.objects.last()
    if ckb == None:
        ckb = CookBook.objects.create(ingridients=ing)

    if 'recipe_name' in request.POST.keys():
        ckb.recipe_name = int(request.POST['recipe_name'])
        ckb.save()

        if request.POST['recipe_name'] == '0':
            ing_form = HamburgerForm(request.POST, instance=ing)
        elif request.POST['recipe_name'] == '1':
            ing_form = PancakeForm(request.POST, instance=ing)
        context['ingridients_form'] = ing_form
    else:
        recipe = ckb.recipe_name
        if recipe == 0:
            ing_form = HamburgerForm(request.POST, instance=ing)
        elif recipe == 1:
            ing_form = PancakeForm(request.POST, instance=ing)
        ing_form.save()

    context['ingridients_form'] = ing_form
    context['cookbook_form'] = CookBookForm(request.POST or None)
    return render(request, 'demo/nondynamic.html', context)

def dynamic(request):
    context = {}
    content = {}
    if request.session.get('initialised', False):
        request.session['initialised']=true
        request.session['recipe_name']=99

    if request.method == 'POST':
        if 'recipe_name' in request.POST:
            request.session['recipe_name'] = int(request.POST['recipe_name'])
        else:
            for key in request.POST.keys():
                if key != 'csrfmiddlewaretoken':
                    content[key] = request.POST[key]
            ckb = CookBook.objects.create(recipe_name = request.session['recipe_name'], ingridients = json.dumps(content))


    if request.session['recipe_name'] == 0:
        new_fields = {
            'cheese': forms.IntegerField(),
            'ham'   : forms.IntegerField(),
            'onion' : forms.IntegerField(),
            'bread' : forms.IntegerField(),
            'ketchup': forms.IntegerField()}
    elif request.session['recipe_name'] == 1:
        new_fields = {
            'milk'  : forms.IntegerField(),
            'butter': forms.IntegerField(),
            'honey' : forms.IntegerField(),
            'eggs'  : forms.IntegerField()}
    else:
        request.session['recipe_name']=99
        new_fields = {
            }

    DynamicIngridientsForm = type('DynamicIngridientsForm',
            (IngridientsForm,),
            new_fields)

    IngForm = DynamicIngridientsForm(content)
    context['ingridients_form'] = IngForm
    context['cookbook_form']    = CookBookForm(request.POST or None)
    return render(request, "demo/dynamic.html", context)
