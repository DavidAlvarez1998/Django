from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template
import pymongo

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
    return render(request,'index.html')


def iniciarSecion(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    db=cliente['Libreria']
    
    correo=request.GET["correo"]
    contraseña=request.GET["contraseña"]

    clientes = db['cliente']
    usuario=clientes.find_one({'correo':correo})
    if usuario==None:
        cliente.close()
        return HttpResponse("ERROR: no existe ninguna cuenta con esa direccion de correo") 
    contraseñaInfo=usuario['contraseña']
    if contraseña!=contraseñaInfo:
        cliente.close()
        return HttpResponse("ERROR: contraseña incorrecta") 

    cliente.close()
    return render(request,'home-client.html') 

def perfil(request):
    return render(request,'editar-perfil.html') 


def editarPerfil(request):
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
    correoActual=request.GET["correoActual"]
    correoNuevo=request.GET["correoNuevo"]
    contraseñaActual=request.GET["contraseñaActual"]
    contraseñaNueva=request.GET["contraseñaNueva"]
    confimarContraseña=request.GET["confimarContraseña"]

    clientes = db['cliente']
    buscar=clientes.find_one({'correo':correoActual})

    if buscar==None:
        cliente.close()
        return HttpResponse("ERROR: Correo actual no encotrado") 
    
    buscar1=clientes.find_one({'correo':correoNuevo})
    if buscar1!=None:
        cliente.close()
        return HttpResponse("ERROR: Correo nuevo no disponible") 

    if contraseñaActual!=buscar['contraseña']:
        cliente.close()
        return HttpResponse("ERROR: contraseña actual es incorrecta") 

    if contraseñaNueva!=confimarContraseña:
        cliente.close()
        return HttpResponse("ERROR: las contraseñas no coinciden") 

    if nombre=="":
        nombre=buscar['nombre']
    if apellido=="":
        apellido=buscar['apellido']
    if telefono=="":
        telefono=buscar['telefono']
    if nacimiento=="":
        nacimiento=buscar['fecha-nacimiento']
    if pais=="":
        pais=buscar['pais']
    if ciudad=="":
        ciudad=buscar['ciudad']
    if direccion=="":
        direccion=buscar['direccion']
    if codigopos=="":
        codigopos=buscar['codigopos']
    if usuario=="":
        usuario=buscar['usuario']

    clientes.update_one({
        'correo':correoActual
        },{
            "$set":{
                'nombre':nombre,
                'apellido':apellido,
                'telefono':telefono,
                'fecha de nacimiento':nacimiento,
                'pais':pais,
                'ciudad':ciudad,
                'direccion':direccion,
                'codigopostal':codigopos,
                'usuario':usuario,
                'correo':correoNuevo,
                'contraseña':contraseñaNueva,
            }
        })




    cliente.close()
    return HttpResponse("Informacion actulizada") 

