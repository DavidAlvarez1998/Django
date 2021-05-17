from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template
import datetime 
import pymongo

def saludo(request):
    hora=datetime.datetime.now()
    return render(request,'paginaweb.html',{"hora":hora}) 

def busquedaLibro(request):
     return render(request,'paginaweb.html') 

def buscar(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria

    db=cliente['Libreria']

    mensaje=request.GET["buscarBD"]

    libro = db['libro']
    buscar=libro.find_one({'titulo':mensaje})
    buscar=buscar['autor']
    cliente.close()

    return HttpResponse(buscar) 

