# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from enterSources.models import Sources, Categories, Cat_x_Source
from enterSources.forms import Bulletin_request, Cat_request

# Create your views here.

def home(request):
    return render(request, "index.html")

def service(request):
    if request.method == 'POST':
        form1 = Bulletin_request(request.POST)
        form2 = Cat_request(request.POST)
        if form1.is_valid() and form2.is_valid():

            source = form1.save()

            # Separate each category
            cat_text = form2.cleaned_data['category']
            cat_list = [cat.strip() for cat in cat_text.split(",")]

            for cat in cat_list:
                cat = cat.strip()
                category, created = Categories.objects.get_or_create(category=cat)
                Cat_x_Source.objects.create(source=source, category=category)

            
            messages.success(request, 'Fuente agregada exitosamente.')
            return redirect('../result_insert/')  # Redirects to exit page
        else:
            messages.error(request, 'Revisa') # Messege needs to be changed
    else:
        messages.error(request, 'mensaje') # Messege needs to be changed
        form1 = Bulletin_request()
        form2 = Cat_request()

    
    return render(request, 'insert.html', {'form': form1, 'form_cat':form2})

def result_insert(request):
    return HttpResponse("Exito al ingresar la fuente de datos.")

