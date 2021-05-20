from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template
import datetime 
import pymongo

def saludo(request):
    hora=datetime.datetime.now()
    return render(request,'paginaweb.html',{"hora":hora}) 

def index(request):
     return render(request,'index.html') 

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



def registro(request):
    return render(request,'register.html') 


def registrarCliente(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    db=cliente['Libreria']
    

    nombre=request.GET["nombre"]
    apellido=request.GET["apellido"]
    telefono=request.GET["telefono"]
    nacimiento=request.GET["fecha-nacimiento"]
    pais=request.GET["pais"]
    ciudad=request.GET["ciudad"]
    direccion=request.GET["direccion"]
    codigopos=request.GET["codigopos"]
    usuario=request.GET["usuario"]
    correo=request.GET["correo"]
    contraseña=request.GET["contraseña"]
    confcontraseña=request.GET["confcontraseña"]

    clientes = db['cliente']
    buscar=clientes.find_one({'correo':correo})
    if buscar!=None:
        buscar=buscar['correo']
    if buscar==correo:
        cliente.close()
        return HttpResponse("ERROR: correo ya registrado")
    if confcontraseña!=contraseña:
        cliente.close()
        return HttpResponse("ERROR: contraseña no coincide")



    clientes=db['cliente']
    clientes.insert_one({
        'nombre':nombre,
        'apellido':apellido,
        'telefono':telefono,
        'fecha de nacimiento':nacimiento,
        'pais':pais,
        'ciudad':ciudad,
        'direccion':direccion,
        'codigopostal':codigopos,
        'usuario':usuario,
        'correo':correo,
        'contraseña':contraseña,
        })
    cliente.close()
    return HttpResponse("listo pai") 
    
    