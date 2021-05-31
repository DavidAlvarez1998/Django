from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template
import pymongo
from PIL import Image
import base64
import os

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
    return buscar['nombre']

def index(request):
    mensaje=root() 
    return render(request,'index.html',{"mensaje":mensaje}) 

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
        con=0
        autor=[]
        for documento in libros.find({'Titulo':mensaje}):
            autor.append(documento['Autor'])
            DIR = os.path.dirname(os.path.realpath(r'__file__'))
            DIR=DIR.replace('\\','/')
            imagen=documento['Portada']
            imagen=base64.b64decode(imagen)
            archivo=open(DIR+"/proyecto1/plantillas/static/temporal/"+str(con)+".jpg","wb")
            archivo.write(imagen)
            archivo.close()
            con=con+1
            
        cliente.close()
        return render(request,'busqueda.html',{"autor0":autor[0],"autor1":autor[1],"autor2":autor[2],"autor3":autor[3],"autor4":autor[4]})

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
    if correo=="root":                          #saber si el usuario que ingresa es el root
        usuarioRoot = db['root']
        root=usuarioRoot.find_one({'nombre':'root'})
        contraseñaroot=root['contraseña']
        if contraseña!=contraseñaroot:
            cliente.close()
            return HttpResponse("ERROR: contraseña incorrecta")
        cliente.close()
        return render(request,'agregar-libro.html') 
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
    portada=request.GET["Portada"]
    direccionportada=request.GET[r"direccionportada"]
    direccionportada=direccionportada.replace('\\', '/')
    libros=db['libro']
    buscar=libros.find_one({'Titulo':Titulo})
    if buscar!=None:
        if buscar['Autor']==Autor:
            con=[]
            for documento in libros.find({'Titulo':Titulo},{'Autor':Autor}):
                con.append(documento)
            con=len(con)+1
            libros.update_many({'Titulo':Titulo},{"$set":{'Ejemplares':con}})
            if portada!='':
                portada=direccionportada+"/"+portada
                image = portada
                Image.open(image)
                with open(image, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
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
                    'Portada':encoded_string,
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

    if portada!='':
        portada=direccionportada+"/"+portada
        image = portada
        Image.open(image)
        with open(image, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
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
            'Portada':encoded_string,
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