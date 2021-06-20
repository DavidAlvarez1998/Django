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
from bson.objectid import ObjectId

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
        return render(request,'editar-perfil-root.html',{'mensaje':'ERROR: ingrese la contraseña actual'})
    if '' in aux:
        cliente.close()
        return render(request,'editar-perfil-root.html',{'mensaje':'ERROR: no se permiten espacios en blanco'})
    if len(aux)<4:
        cliente.close()
        return render(request,'editar-perfil-root.html',{'mensaje':'ERROR: la contraseña nueva debe tener por lo menos de 4 caracteres'})
    if buscar['contraseña']!=contraActual:
        cliente.close()
        return render(request,'editar-perfil-root.html',{'mensaje':'ERROR: contraseña actual incorrecta'})
    if contraNueva!=confContra:
        cliente.close()
        return render(request,'editar-perfil-root.html',{'mensaje':'ERROR: contraseñas no coinciden'})
    usuarioroot.update_one({
        'nombre':"root"
        },{
        "$set":{
            'contraseña':contraNueva,
        }
        })

    cliente.close()
    return render(request,'editar-perfil-root.html',{'mensaje':'informacion actualizada'})

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

def index(request):
    root()
    return render(request,'index.html') 

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
            cliente.close()
            return render(request,'home-client.html',{'mensaje':'ERROR: no se encuetran libros ni autores con el nombre '+mensaje})       
        autor=buscar['Autor']
        librosAutor=''
        for documento in libros.find({'Autor':autor}):
            librosAutor=librosAutor+documento['Titulo']+", "
        return render(request,'home-client.html',{'mensaje':librosAutor+'  :  son los libros que tenemos del autor '+autor})
    else:
        titulo=[]
        autor=[]
        imagen=[]
        id=[]
        for documento in libros.find({'Titulo':mensaje}):
            titulo.append(documento['Titulo'])
            autor.append(documento['Autor'])
            imagen.append(documento['Portada'])
            id.append(documento['_id'])
        while len(imagen)<8:
            titulo.append('')
            autor.append('')
            imagen.append('')
            id.append('')
        cliente.close()
        return render(request,'home-client.html',{"titulo0":titulo[0],"autor0":autor[0],"imagen0":imagen[0],"id0":id[0],"titulo1":titulo[1],"autor1":autor[1],"imagen1":imagen[1],"id1":id[1],"titulo2":titulo[2],"autor2":autor[2],"imagen2":imagen[2],"id2":id[2],"titulo3":titulo[3],"autor3":autor[3],"imagen3":imagen[3],"id3":id[3],"titulo4":titulo[4],"autor4":autor[4],"imagen4":imagen[4],"id4":id[4],"titulo5":titulo[5],"autor5":autor[5],"imagen5":imagen[5],"id5":id[5],"titulo6":titulo[6],"autor6":autor[6],"imagen6":imagen[6],"id6":id[6],"titulo7":titulo[7],"autor7":autor[7],"imagen7":imagen[7],"id7":id[7]})

def buscarInvitado(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    db=cliente['Libreria']
    mensaje=request.GET["buscarBD"]
    libros = db['libro']
    buscar=libros.find_one({'Titulo':mensaje})
    if buscar==None:
        buscar=libros.find_one({'Autor':mensaje})
        if buscar==None:  
            cliente.close()          
            return render(request,'mostrar-libro.html',{'mensaje':'ERROR: no se encuetran libros ni autores con el nombre '+mensaje})  
        autor=buscar['Autor']
        librosAutor=''
        for documento in libros.find({'Autor':autor}):
            librosAutor=librosAutor+documento['Titulo']+", "
        return render(request,'mostrar-libro.html',{'mensaje':librosAutor+'  :  son los libros que tenemos del autor '+autor})
    else:
        autor=[]
        imagen=[]
        for documento in libros.find({'Titulo':mensaje}):
            autor.append(documento['Autor'])
            imagen.append(documento['Portada'])
        while len(imagen)<8:
            autor.append('')
            imagen.append('')
        cliente.close()
        return render(request,'mostrar-libro.html',{"autor0":autor[0],"imagen0":imagen[0],"autor1":autor[1],"imagen1":imagen[1],"autor2":autor[2],"imagen2":imagen[2],"autor3":autor[3],"imagen3":imagen[3],"autor4":autor[4],"imagen4":imagen[4],"autor5":autor[5],"imagen5":imagen[5],"autor6":autor[6],"imagen6":imagen[6],"autor7":autor[7],"imagen7":imagen[7]})

def registro(request):
    return render(request,'register.html') 

def registrarCliente(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    db=cliente['Libreria']
    nombre=request.GET["nombre"]
    apellido=request.GET["apellido"]
    telefono=request.GET["telefono"]
    nacimiento=request.GET["nacimiento"]
    pais=request.GET["pais"]
    direccion=request.GET["direccion"]
    usuario=request.GET["usuario"]
    correo=request.GET["correo"]
    contraseña=request.GET["contraseña"]
    confcontraseña=request.GET["confcontraseña"]
    if nombre=='' or apellido=='' or telefono=='' or nacimiento=='' or pais=='' or direccion=='' or usuario=='' or correo=='':
        cliente.close()
        return render(request,'register.html',{'mensaje':'ERROR: debe de completar todos los campos'})
    admins=db['admin']
    buscar=admins.find_one({'correo':correo})
    if buscar!=None:
        cliente.close()
        return render(request,'register.html',{'mensaje':'ERROR: correo no disponible'})
    aux=list(contraseña)
    if len(aux)==0:
        cliente.close()
        return render(request,'register.html',{'mensaje':'ERROR: ingrese una contraseña'})
    if '' in aux:
        cliente.close()
        return render(request,'register.html',{'mensaje':'ERROR: no se permiten espacios en blanco'})
    if len(aux)<8:
        cliente.close()
        return render(request,'register.html',{'mensaje':'ERROR: la contraseña debe tener por lo menos de 8 caracteres'})
    clientes = db['cliente']
    buscar=clientes.find_one({'correo':correo})
    if buscar!=None:
        buscar=buscar['correo']
    if buscar==correo:
        cliente.close()
        return render(request,'register.html',{'mensaje':'ERROR: correo ya registrado'})
    if confcontraseña!=contraseña:
        cliente.close()
        return render(request,'register.html',{'mensaje':'ERROR: contraseña no coincide'})
    if nacimiento!='':
        años=calculoFecha(nacimiento)
        if años<18:
            cliente.close()
            return render(request,'register.html',{'mensaje':'ERROR: debes de ser mayor de 18 años'})
        if calculoFecha(nacimiento)>90:
            cliente.close()
            return render(request,'register.html',{'mensaje':'ERROR: fecha de nacimiento no puedes tener '+años+' años'})
    clientes=db['cliente']
    clientes.insert_one({
        'nombre':nombre,
        'apellido':apellido,
        'telefono':telefono,
        'nacimiento':nacimiento,
        'pais':pais,
        'direccion':direccion,
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
    if correo=='':
        cliente.close()
        return render(request,'index.html',{'mensaje':'ERROR: digite correo'})
    if contraseña=='':
        return render(request,'index.html',{'mensaje':'ERROR: digite contraseña'})
    if correo=="root":                          #saber si el usuario que ingresa es el root
        usuarioRoot = db['root']
        root=usuarioRoot.find_one({'nombre':'root'})
        contraseñaroot=root['contraseña']
        if contraseña!=contraseñaroot:
            cliente.close()
            return render(request,'index.html',{'mensaje':'ERROR: contraseña incorrecta'})
        cliente.close()
        return render(request,'principal-root.html')
    
    admins=db['admin']                          #saber si el usuario es un admin
    admin=admins.find_one({'nombre usuario':correo})
    if admin!=None:
        if admin['contraseña']!=contraseña:
            cliente.close()
            return render(request,'index.html',{'mensaje':'ERROR: contraseña incorrecta'})
        if admin['correo']=='':
            admins.delete_one({'nombre usuario':correo})
            cliente.close()
            return render(request,'registro-admin.html')
    admin=admins.find_one({'correo':correo})     #admin que ya completo el registro
    if admin!=None:
        if admin['contraseña']!=contraseña:
            cliente.close()
            return render(request,'index.html',{'mensaje':'ERROR: contraseña incorrecta'})
        cliente.close()
        return render(request,'principal-admin.html')
        
    clientes = db['cliente']                     #inicio de secion usuario cliente
    usuario=clientes.find_one({'correo':correo})
    if usuario==None:
        cliente.close()
        return render(request,'index.html',{'mensaje':'ERROR: no existe ninguna cuenta con esa direccion de correo'})
    contraseñaInfo=usuario['contraseña']
    if contraseña!=contraseñaInfo:
        cliente.close()
        return render(request,'index.html',{'mensaje':'ERROR: contraseña incorrecta'})
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
    nacimiento=request.GET["nacimiento"]
    pais=request.GET["pais"]
    direccion=request.GET["direccion"]
    usuario=request.GET["usuario"]
    correoActual=request.GET["correoActual"]
    correoNuevo=request.GET["correoNuevo"]
    contraseñaActual=request.GET["contraseñaActual"]
    contraseñaNueva=request.GET["contraseñaNueva"]
    confimarContraseña=request.GET["confimarContraseña"]
    clientes = db['cliente']
    buscar=clientes.find_one({'correo':correoActual,'contraseña':contraseñaActual})
    if buscar==None:
        cliente.close()
        return render(request,'editar-perfil.html',{'mensaje':'ERROR: datos actuales'})
    if correoNuevo!='':
        buscar1=clientes.find_one({'correo':correoNuevo})
        if buscar1!=None:
            cliente.close()
            return render(request,'editar-perfil.html',{'mensaje':'ERROR: nuevo correo no disponible'})
    if contraseñaNueva!=confimarContraseña:
        cliente.close()
        return render(request,'editar-perfil.html',{'mensaje':'ERROR: las contraseñas no coinciden'})
    if nacimiento!='':
        if calculoFecha(nacimiento)<18:
            cliente.close()
            return render(request,'editar-perfil.html',{'mensaje':'ERROR: fecha de nacimiento'})
        if calculoFecha(nacimiento)>90:
            cliente.close()
            return render(request,'editar-perfil.html',{'mensaje':'ERROR: fechade nacimiento'})

    if nombre=="":
        nombre=buscar['nombre']
    if apellido=="":
        apellido=buscar['apellido']
    if telefono=="":
        telefono=buscar['telefono']
    if nacimiento=="":
        nacimiento=buscar['nacimiento']
    if pais=="":
        pais=buscar['pais']
    if direccion=="":
        direccion=buscar['direccion']
    if usuario=="":
        usuario=buscar['usuario']
    if contraseñaNueva=='':
        contraseñaNueva=buscar['contraseñaNueva']
    if correoNuevo=='':
        correoNuevo=buscar['correo']

    clientes.update_one({
        'correo':correoActual
        },{
            "$set":{
                'nombre':nombre,
                'apellido':apellido,
                'telefono':telefono,
                'nacimiento':nacimiento,
                'pais':pais,
                'direccion':direccion,
                'usuario':usuario,
                'correo':correoNuevo,
                'contraseña':contraseñaNueva,
            }
        })

    cliente.close()
    return render(request,'editar-perfil.html',{'mensaje':'Informacion actulizada'})

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
            return render(request,'Agregar-libro.html',{'mensaje':'Libro Agregado'})

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
    return render(request,'Agregar-libro.html',{'mensaje':'Libro Agregado'})

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
        return render(request,'principal-root.html',{'mensaje':'ERROR: ingrese una contraseña'})
    if '' in aux:
        cliente.close()
        return render(request,'principal-root.html',{'mensaje':'ERROR: contraseña no permite espacios en blanco'})
    if len(aux)<4:
        cliente.close()
        return render(request,'principal-root.html',{'mensaje':'ERROR: la contraseña debe tener por lo menos de 4 caracteres'})
    if contraseña!=confcontraseña:
        cliente.close()
        return render(request,'principal-root.html',{'mensaje':'ERROR: las contraseñas no coinciden'})
    aux=list(nombre)
    if len(aux)==0:
        cliente.close()
        return render(request,'principal-root.html',{'mensaje':'ERROR: ingrese un nombre de usuario'})
    if '' in aux:
        cliente.close()
        return render(request,'principal-root.html',{'mensaje':'ERROR: no se permite espacios en blanco para el usuario admin'})
    admins=db['admin']
    buscar=admins.find_one({'nombre usuario':nombre})
    if buscar!=None:
        return render(request,'principal-root.html',{'mensaje':'ERROR: nombre de usuario no disponible'})
    admins.insert_one({
            'nombre usuario':nombre,
            'contraseña':contraseña,
            'correo':'',
            })

    cliente.close()
    return render(request,'principal-root.html',{'mensaje':'admin creado'})

def registroAdmin(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    db=cliente['Libreria']

    nombre=request.GET["nombre"]
    apellido=request.GET["apellido"]
    telefono=request.GET["telefono"]
    nacimiento=request.GET["nacimiento"]
    correo=request.GET["correo"]
    contraseña=request.GET["contraseña"]
    confcontraseña=request.GET["confcontraseña"]
    clientes=db['cliente']
    buscar=clientes.find_one({'correo':correo})
    if buscar!=None:
        return render(request,'registro-admin.html',{'mensaje':'ERROR: correo no disponible'})
    aux=list(contraseña)
    if len(aux)==0:
        cliente.close()
        return render(request,'registro-admin.html',{'mensaje':'ERROR: ingrese una contraseña'})
    if '' in aux:
        cliente.close()
        return render(request,'registro-admin.html',{'mensaje':'ERROR: no se permiten espacios en blanco'})
    if len(aux)<8:
        cliente.close()
        return render(request,'registro-admin.html',{'mensaje':'ERROR: la contraseña debe tener por lo menos de 8 caracteres'})
    if confcontraseña!=contraseña:
        cliente.close()
        return render(request,'registro-admin.html',{'mensaje':'ERROR: contraseña no coincide'})
    if nacimiento!='':
        if calculoFecha(nacimiento)<18:
            cliente.close()
            return render(request,'registro-admin.html',{'mensaje':'ERROR: debes de ser mayor de 18 años'})
        if calculoFecha(nacimiento)>90:
            cliente.close()
            return render(request,'registro-admin.html',{'mensaje':'ERROR: fechade nacimiento'})
    admins=db['admin']
    buscar=admins.find_one({'correo':correo})
    if buscar!=None:
        cliente.close()
        return render(request,'registro-admin.html',{'mensaje':'ERROR: correo no disponible'})
    admins.insert_one({
        'nombre':nombre,
        'apellido':apellido,
        'telefono':telefono,
        'nacimiento':nacimiento,
        'correo':correo,
        'contraseña':contraseña,
        })
    cliente.close()
    return render(request,'index.html') 

def paginaEditarAdmin(request):
    return render(request,'editar-perfil-admin.html')

def paginaprincipalAdmin(request):
    return render(request,'principal-admin.html')

def editarPerfilAdmin(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    db=cliente['Libreria']
    nombre=request.GET["nombre"]
    apellido=request.GET["apellido"]
    telefono=request.GET["telefono"]
    nacimiento=request.GET["nacimiento"]
    correoac=request.GET["correoac"]
    correonu=request.GET["correonu"]
    contraAc=request.GET["contraAc"]
    contraNu=request.GET["contraNu"]
    confcontra=request.GET["confcontra"]
    admins=db['admin']
    buscar=admins.find_one({'correo':correoac})
    if buscar==None:
        cliente.close()
        return render(request,'editar-perfil-admin.html',{'mensaje':'ERROR: correo actual incorrecto'})
    if correonu!='':
        clientes = db['cliente']
        buscar1=clientes.find_one({'correo':correonu})
        if buscar1!=None:
            cliente.close()
            return render(request,'editar-perfil-admin.html',{'mensaje':'ERROR: correo no disponible'})
        buscar1=admins.find_one({'correo':correonu})
        if buscar1!=None:
            cliente.close()
            return render(request,'editar-perfil-admin.html',{'mensaje':'ERROR: correo no disponible'})
    if contraAc!=buscar['contraseña']:
        cliente.close()
        return render(request,'editar-perfil-admin.html',{'mensaje':'ERROR: contraseña actual es incorrecta'})
    if contraNu!=confcontra:
        cliente.close()
        return render(request,'editar-perfil-admin.html',{'mensaje':'ERROR: las contraseñas no coinciden'})
    if nacimiento!='':
        if calculoFecha(nacimiento)<18:
            cliente.close()
            return render(request,'editar-perfil-admin.html',{'mensaje':'ERROR: fecha de nacimiento'})
        if calculoFecha(nacimiento)>90:
            cliente.close()
            return render(request,'editar-perfil-admin.html',{'mensaje':'ERROR: fechade nacimiento'})
    if nombre=="":
        nombre=buscar['nombre']
    if apellido=="":
        apellido=buscar['apellido']
    if telefono=="":
        telefono=buscar['telefono']
    if nacimiento=="":
        nacimiento=buscar['nacimiento']
    if correonu=="":
        correonu=buscar['correo']
    if contraNu=="":
        contraNu=buscar['contraseña']
    admins.update_one({
        'correo':correoac
        },{
            "$set":{
                'nombre':nombre,
                'apellido':apellido,
                'telefono':telefono,
                'nacimiento':nacimiento,
                'correo':correonu,
                'contraseña':contraNu,
            }
        })
    cliente.close()
    return render(request,'editar-perfil-admin.html',{'mensaje':'informacion actualizada'})

def paginaEditarLibro(request):
    return render(request,'editar-libro.html')

def Rellenareditarlibro(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    db=cliente['Libreria']
    codigo=request.GET["codigo"]
    libros=db['libro']
    try:
        ObjectIdistance=ObjectId(codigo)
    except:
        cliente.close()
        return render(request,'editar-libro.html',{'mensaje':'ERROR: codigo libro no existe'})
    buscar=libros.find_one({'_id':ObjectIdistance})
    if buscar==None:
        cliente.close()
        return render(request,'editar-libro.html',{'mensaje':'ERROR: codigo libro no existe'})
    Titulo=buscar['Titulo']
    Autor=buscar['Autor']
    PublicA=buscar['PublicA']
    Genero=buscar['Genero']
    numeropaginas=buscar['numeropaginas']
    Editorial=buscar['Editorial']
    Idioma=buscar['Idioma']
    Estado=buscar['Estado']
    Precio=buscar['Precio']
    Portada=buscar['Portada']
    cliente.close()
    return render(request,'editar-libro.html',{'codigo':codigo,'Titulo':Titulo,'Autor':Autor,'PublicA':PublicA,'Genero':Genero,'numeropaginas':numeropaginas,'Editorial':Editorial,'Idioma':Idioma,'Estado':Estado,'Precio':Precio,'Portada':Portada,})

def editarlibro(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    db=cliente['Libreria']
    codigo=request.GET['codigo']
    Titulo=request.GET['Titulo']
    Autor=request.GET['Autor']
    PublicA=request.GET['PublicA']
    Genero=request.GET['Genero']
    numeropaginas=request.GET['numeropaginas']
    Editorial=request.GET['Editorial']
    Idioma=request.GET['Idioma']
    Estado=request.GET['Estado']
    Precio=request.GET['Precio']
    Portada=request.GET['Portada']
    libros=db['libro']
    if codigo=='':
        return render(request,'editar-libro.html',{'mensaje':'ERROR: primero debe de buscar un libro por su codigo libro'})
    ObjectIdistance=ObjectId(codigo)
    buscar=libros.find_one({'_id':ObjectIdistance})
    if Titulo=='':
        Titulo=buscar['Titulo']
    if Autor=='': 
        Autor=buscar['Autor']
    if PublicA=='': 
        PublicA=buscar['PublicA']
    if Genero=='': 
        Genero=buscar['Genero']
    if numeropaginas=='': 
        numeropaginas=buscar['numeropaginas']
    if Editorial=='': 
        Editorial=buscar['Editorial']
    if Idioma=='': 
        Idioma=buscar['Idioma']
    if Estado=='': 
        Estado=buscar['Estado']
    if Precio=='': 
        Precio=buscar['Precio']
    if Portada=='': 
        Portada=buscar['Portada']
    libros.update_one({
        '_id':ObjectId(codigo)
        },{
            "$set":{
                'Titulo':Titulo,
                'Autor':Autor,
                'PublicA':PublicA,
                'Genero':Genero,
                'numeropaginas':numeropaginas,
                'Editorial':Editorial,
                'Idioma':Idioma,
                'Estado':Estado,
                'Precio':Precio,
                'Portada':Portada,
            }
        })
    cliente.close()
    return render(request,'editar-libro.html',{'mensaje':'informacion actualizada'})

def paginaEliminarLibro(request):
    return render(request,'eliminar-libro.html')

def rellenarEliminarLibro(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    db=cliente['Libreria']
    codigo=request.GET["codigo"]
    if codigo=='':
        return render(request,'eliminar-libro.html',{'mensaje':'ERROR: primero debe de buscar un libro por su codigo libro'})
    try:
        ObjectIdistance=ObjectId(codigo)
    except:
        cliente.close()
        return render(request,'eliminar-libro.html',{'mensaje':'ERROR: codigo libro no existe'})
    libros=db['libro']
    buscar=libros.find_one({'_id':ObjectIdistance})
    Titulo=buscar['Titulo']
    Autor=buscar['Autor']
    PublicA=buscar['PublicA']
    Genero=buscar['Genero']
    numeropaginas=buscar['numeropaginas']
    Editorial=buscar['Editorial']
    Idioma=buscar['Idioma']
    Estado=buscar['Estado']
    Precio=buscar['Precio']
    Portada=buscar['Portada']
    Ejemplares=buscar['Ejemplares']
    cliente.close()
    return render(request,'eliminar-libro.html',{'Titulo':Titulo,'Autor':Autor,'PublicA':PublicA,'Genero':Genero,'numeropaginas':numeropaginas,'Editorial':Editorial,'Idioma':Idioma,'Estado':Estado,'Precio':Precio,'Portada':Portada,'Ejemplares':Ejemplares,'codigo':codigo})
    
def eliminarlibro(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    db=cliente['Libreria']
    codigo=request.GET["codigo"]
    ObjectIdistance=ObjectId(codigo)
    libros=db['libro']
    libros.delete_one({'_id':ObjectIdistance})
    cliente.close()
    return render(request,'eliminar-libro.html',{'mensaje':'Libro Eliminado'})

def paginaComprarLibro(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    db=cliente['Libreria']
    id=request.GET['id']
    libros=db['libro']
    ObjectIdistance=ObjectId(id)
    buscar=libros.find_one({'_id':ObjectIdistance})
    titulo=buscar['Titulo']
    autor=buscar['Autor']
    año=buscar['PublicA']
    genero=buscar['Genero']
    numeropaginas=buscar['numeropaginas']
    editorial=buscar['Editorial']
    estado=buscar['Estado']
    precio=buscar['Precio']
    idioma=buscar['Idioma']
    portada=buscar['Portada']
    cliente.close()
    return render(request,'comprar-reservar-libro.html',{'titulo':titulo,'autor':autor,'año':año,'genero':genero,'numeropaginas':numeropaginas,'estado':estado,'precio':precio,'portada':portada,'idioma':idioma,'editorial':editorial,'id':id})
    
def paginaHomeClient(request):
    return render(request,'home-client.html')

def infoIndex(request):
     return render(request,'info.html')
    
def mensajeMostrarLibro(request):
    return render(request,'mostrar-libro.html',{'mensaje':"debe iniciar secion para poder comprar un libro"})

def comprarLibro(request):
    cliente = pymongo.MongoClient("mongodb+srv://admin:33sqQMSJRct-Erz@cluster0.nfxzs.mongodb.net/Libreria?retryWrites=true&w=majority")
    db = cliente.Libreria
    db=cliente['Libreria']
    id=request.GET['id']
    libros=db['libro']
    clientes=db['cliente']
    id=request.GET['id']
    correo=request.GET["correo"]
    contraseña=request.GET["contraseña"]
    if contraseña=='' or correo=='':
        cliente.close()
        return render(request,'home-client.html',{'mensaje':"informacion incompleta"})
    buscar=clientes.find_one({'correo':correo})
    if buscar==None:
        return render(request,'home-client.html',{'mensaje':"tu informacion es incorrecta"})
    if buscar['contraseña']!=contraseña:
            return render(request,'home-client.html',{'mensaje':"tu informacion es incorrecta"})
    idcliente=buscar['_id']
    nombre=buscar['nombre']
    apellido=buscar['apellido']
    telefono=buscar['telefono']
    nacimiento=buscar['nacimiento']
    pais=buscar['pais']
    direccion=buscar['direccion']
    usuario=buscar['usuario']
    correo=buscar['correo']
    contraseña=buscar['contraseña']    
    ObjectIdistance=ObjectId(id)
    buscar=libros.find_one({'_id':ObjectIdistance})
    titulo=buscar['Titulo']
    autor=buscar['Autor']
    año=buscar['PublicA']
    genero=buscar['Genero']
    numeropaginas=buscar['numeropaginas']
    editorial=buscar['Editorial']
    estado=buscar['Estado']
    precio=buscar['Precio']
    idioma=buscar['Idioma']
    portada=buscar['Portada']
    vendidos=db['vendido']
    vendidos.insert_one({
        'Titulo':titulo,
        'Autor':autor,
        'PublicA':año,
        'Genero':genero,
        'numeropaginas':numeropaginas,
        'Editorial':editorial,
        'Idioma':idioma,
        'Estado':estado,
        'Precio':precio,
        'Portada':portada,
        'idcliente':idcliente,
        'nombre':nombre,
        'apellido':apellido,
        'telefono':telefono,
        'nacimiento':nacimiento,
        'pais':pais,
        'direccion':direccion,
        'usuario':usuario,
        'correo':correo,
        'contraseña':contraseña,
            })
    ObjectIdistance=ObjectId(id)
    libros.delete_one({'_id':ObjectIdistance})
    con=[]
    for documento in libros.find({'Titulo':titulo},{'Autor':autor}):
                con.append(documento)
    con=len(con)
    libros.update_many({'Titulo':titulo,'Autor':autor},{"$set":{'Ejemplares':con}})
    cliente.close()
    return render(request,'home-client.html',{'mensaje':"libro comprado exitosamente"})






