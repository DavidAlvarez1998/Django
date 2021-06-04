from enum import auto
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template
import pymongo
from PIL import Image
import base64
import os
from os import remove
from os import path
from datetime import date

def calculoFecha(nacimiento):
    nacimiento=nacimiento.split('-')
    nacimiento=date(int(nacimiento[0]),int(nacimiento[1]),int(nacimiento[2]))
    actual=date.today()
    resultado=actual.year - nacimiento.year
    resultado-=((actual.month,actual.day)<(nacimiento.month,nacimiento.day))
    return resultado

def editarPerfilRoot(request):
    return render(request,'editar-perfil-root.html')

def perfilRoot(request):
    return render(request,'principal-root.html')

def editarroot(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    db=cliente['Libreria']
    usuarioroot = db['root']
    buscar=usuarioroot.find_one({'nombre':'root'})
    contraActual=request.GET["contraActual"]
    contraNueva=request.GET["contraNueva"]
    confContra=request.GET["confContra"]
    aux=list(contraNueva)
    if len(aux)==0:
        cliente.close()
        return HttpResponse("ERROR: ingrese la contraseña actual")
    if '' in aux:
        cliente.close()
        return HttpResponse("ERROR: no se permiten espacios en blanco")
    if len(aux)<4:
        cliente.close()
        return HttpResponse("ERROR: la contraseña nueva debe tener por lo menos de 4 caracteres")
    if buscar['contraseña']!=contraActual:
        cliente.close()
        return HttpResponse("ERROR: contraseña actual incorrecta")
    if contraNueva!=confContra:
        cliente.close()
        return HttpResponse("ERROR: contraseñas no coinciden")
    usuarioroot.update_one({
        'nombre':"root"
        },{
        "$set":{
            'contraseña':contraNueva,
        }
        })

    cliente.close()
    return HttpResponse("informacion actualizada")

def root():
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    usuarioroot = db['root']
    buscar=usuarioroot.find_one({'nombre':'root'})
    if buscar==None:
        usuarioroot=db['root']
        usuarioroot.insert_one({
        'nombre': 'root',
        'contraseña':"0000",
    })
    cliente.close()
    return(buscar)

def index(request):
    info=root()
    nombre=info['nombre']
    contraseña=info['contraseña']
    return render(request,'index.html',{"nombre":nombre,"contra":contraseña}) 

def buscar(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    db=cliente['Libreria']
    mensaje=request.GET["buscarBD"]
    libros = db['libro']
    buscar=libros.find_one({'Titulo':mensaje})
    if buscar==None:
        buscar=libros.find_one({'Autor':mensaje})
        if buscar==None:            
            return HttpResponse("ERROR: no se encuetran libros ni autores con el nombre "+mensaje) 
        autor=buscar['Autor']
        librosAutor=''
        for documento in libros.find({'Autor':autor}):
            librosAutor=librosAutor+documento['Titulo']+", "
        return HttpResponse(librosAutor+"  :  son los libros que tenemos del autor "+autor) 
    else:
        autor=[]
        imagen=[]
        for documento in libros.find({'Titulo':mensaje}):
            autor.append(documento['Autor'])
            imagen.append(documento['Portada'])
        while len(imagen)<5:
            autor.append('')
            imagen.append('')
        cliente.close()
        return render(request,'home-client.html',{"autor0":autor[0],"imagen0":imagen[0],"autor1":autor[1],"imagen1":imagen[1],"autor2":autor[2],"imagen2":imagen[2],"autor3":autor[3],"imagen3":imagen[3],"autor4":autor[4],"imagen4":imagen[4]})

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
    admins=db['admin']
    buscar=admins.find_one({'correo':correo})
    if buscar!=None:
        return HttpResponse("ERROR: correo no disponible")
    aux=list(contraseña)
    if len(aux)==0:
        cliente.close()
        return HttpResponse("ERROR: ingrese una contraseña")
    if '' in aux:
        cliente.close()
        return HttpResponse("ERROR: no se permiten espacios en blanco")
    if len(aux)<8:
        cliente.close()
        return HttpResponse("ERROR: la contraseña debe tener por lo menos de 8 caracteres")
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
    if calculoFecha(nacimiento)<18:
        cliente.close()
        return HttpResponse("ERROR: debes de ser mayor de 18 años")
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
    if correo=="root":                          #saber si el usuario que ingresa es el root
        usuarioRoot = db['root']
        root=usuarioRoot.find_one({'nombre':'root'})
        contraseñaroot=root['contraseña']
        if contraseña!=contraseñaroot:
            cliente.close()
            return HttpResponse("ERROR: contraseña incorrecta")
        cliente.close()
        return render(request,'principal-root.html')
    
    admins=db['admin']                          #saber si el usuario es un admin
    admin=admins.find_one({'nombre usuario':correo})
    if admin!=None:
        if admin['contraseña']!=contraseña:
            cliente.close()
            return HttpResponse("ERROR: contraseña incorrecta")
        if admin['correo']=='':
            admins.delete_one({'nombre usuario':correo})
            cliente.close()
            return render(request,'registro-admin.html')
    admin=admins.find_one({'correo':correo})     #admin que ya completo el registro
    if admin!=None:
        if admin['contraseña']!=contraseña:
            cliente.close()
            return HttpResponse("ERROR: contraseña incorrecta")
        cliente.close()
        return render(request,'principal-admin.html')
        
    clientes = db['cliente']                     #inicio de secion usuario cliente
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

def paginaAgregarlibro(request):
    return render(request,'Agregar-libro.html')

def agregarLibro(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    db=cliente['Libreria']
    Titulo=request.GET["Titulo"]
    Autor=request.GET["Autor"]
    PublicA=request.GET["PublicA"]
    Genero=request.GET["Genero"]
    numeropaginas=request.GET["numeropaginas"]
    Editorial=request.GET["Editorial"]
    Idioma=request.GET["Idioma"]
    Estado=request.GET["Estado"]
    Precio=request.GET["Precio"]
    direccionportada=request.GET["direccionportada"]
    libros=db['libro']
    buscar=libros.find_one({'Titulo':Titulo})
    if buscar!=None:
        if buscar['Autor']==Autor:
            con=[]
            for documento in libros.find({'Titulo':Titulo},{'Autor':Autor}):
                con.append(documento)
            con=len(con)+1
            libros.update_many({'Titulo':Titulo},{"$set":{'Ejemplares':con}})
            if direccionportada!='':
                libros.insert_one({
                    'Titulo':Titulo,
                    'Autor':Autor,
                    'PublicA':PublicA,
                    'Genero':Genero,
                    'numeropaginas':numeropaginas,
                    'Editorial':Editorial,
                    'Idioma':Idioma,
                    'Estado':Estado,
                    'Precio':Precio,
                    'Portada':direccionportada,
                    'Ejemplares':con,
                    })
            else:
                libros.insert_one({
                    'Titulo':Titulo,
                    'Autor':Autor,
                    'PublicA':PublicA,
                    'Genero':Genero,
                    'numeropaginas':numeropaginas,
                    'Editorial':Editorial,
                    'Idioma':Idioma,
                    'Estado':Estado,
                    'Precio':Precio,
                    'Portada':'',
                    'Ejemplares':con,
                    })
            cliente.close()
            return HttpResponse("Libro Agregado")

    if direccionportada!='':
        libros.insert_one({
            'Titulo':Titulo,
            'Autor':Autor,
            'PublicA':PublicA,
            'Genero':Genero,
            'numeropaginas':numeropaginas,
            'Editorial':Editorial,
            'Idioma':Idioma,
            'Estado':Estado,
            'Precio':Precio,
            'Portada':direccionportada,
            'Ejemplares':1,
            })
    else:
        libros.insert_one({
            'Titulo':Titulo,
            'Autor':Autor,
            'PublicA':PublicA,
            'Genero':Genero,
            'numeropaginas':numeropaginas,
            'Editorial':Editorial,
            'Idioma':Idioma,
            'Estado':Estado,
            'Precio':Precio,
            'Portada':'',
            'Ejemplares':1,
            })
    cliente.close()
    return HttpResponse("Libro Agregado")

def crearAdmin(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    db=cliente['Libreria']
    nombre=request.GET["nombre"]
    contraseña=request.GET["contraseña"]
    confcontraseña=request.GET["confcontraseña"]
    aux=list(contraseña)
    if len(aux)==0:
        cliente.close()
        return HttpResponse("ERROR: ingrese una contraseña")
    if '' in aux:
        cliente.close()
        return HttpResponse("ERROR: no se permiten espacios en blanco")
    if len(aux)<4:
        cliente.close()
        return HttpResponse("ERROR: la contraseña debe tener por lo menos de 4 caracteres")
    if contraseña!=confcontraseña:
        cliente.close()
        return HttpResponse("ERROR: las contraseñas no coinciden")
    aux=list(nombre)
    if len(aux)==0:
        cliente.close()
        return HttpResponse("ERROR: ingrese un nombre de usuario")
    if '' in aux[0]:
        cliente.close()
        return HttpResponse("ERROR: no se permite iniciar el nombre de usuario con un espacios en blanco")
    admins=db['admin']
    buscar=admins.find_one({'nombre usuario':nombre})
    if buscar!=None:
        return HttpResponse("ERROR: nombre de usuario no disponible")
    admins.insert_one({
            'nombre usuario':nombre,
            'contraseña':contraseña,
            'correo':'',
            })

    cliente.close()
    return HttpResponse("admin creado")

def registroAdmin(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    db=cliente['Libreria']

    nombre=request.GET["nombre"]
    apellido=request.GET["apellido"]
    telefono=request.GET["telefono"]
    nacimiento=request.GET["fecha-nacimiento"]
    correo=request.GET["correo"]
    contraseña=request.GET["contraseña"]
    confcontraseña=request.GET["confcontraseña"]
    clientes=db['cliente']
    buscar=clientes.find_one({'correo':correo})
    if buscar!=None:
        return HttpResponse("ERROR: correo no disponible")
    aux=list(contraseña)
    if len(aux)==0:
        cliente.close()
        return HttpResponse("ERROR: ingrese una contraseña")
    if '' in aux:
        cliente.close()
        return HttpResponse("ERROR: no se permiten espacios en blanco")
    if len(aux)<8:
        cliente.close()
        return HttpResponse("ERROR: la contraseña debe tener por lo menos de 8 caracteres")
    if confcontraseña!=contraseña:
        cliente.close()
        return HttpResponse("ERROR: contraseña no coincide")
    if calculoFecha(nacimiento)<18:
        cliente.close()
        return HttpResponse("ERROR: debes de ser mayor de 18 años")
    admins=db['admin']
    buscar=admins.find_one({'correo':correo})
    if buscar!=None:
        return HttpResponse("ERROR: correo no disponible")
    admins.insert_one({
        'nombre':nombre,
        'apellido':apellido,
        'telefono':telefono,
        'fecha de nacimiento':nacimiento,
        'correo':correo,
        'contraseña':contraseña,
        })
    cliente.close()
    return render(request,'index.html') 




