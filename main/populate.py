from bs4 import BeautifulSoup
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema,TEXT,ID
import urllib.request
import lxml
import os,shutil
from main.models import *
import requests

def deleteTableIndex():
    Anime.objects.all().delete()
    Puntuacion.objects.all().delete()

    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")

    if os.path.exists("main/static/Imagenes"):
        shutil.rmtree("main/static/Imagenes")
    os.mkdir("main/static/Imagenes")

def carga_imagen(url, titulo):
    response = requests.get(url)
    file = open("main/static/Imagenes/"+titulo+".jpeg", "wb")
    file.write(response.content)
    file.close()

def extraer_animes(numero):
    lista_animes_db = []
    lista_animes_index = []
    for i in range(1,numero+1):
        try:
            lista_db,lista_index = extraer_pagina("https://www3.animeflv.net/browse?order=rating&page="+str(i))
        except:
            continue
        lista_animes_db.extend(lista_db)
        lista_animes_index.extend(lista_index)
    return lista_animes_db,lista_animes_index

def extraer_pagina(url):
    lista_db = []
    lista_index = []
    #Necesitamos identificarnos como un navegador por la propia seguridad de la página, ya que al
    #hacerlo como una librería de python esta no nos deja entrar. Una vez hecha la request
    #podemos abir la url y extraer la información como siempre.
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    f = urllib.request.urlopen(req).read()
    s = BeautifulSoup(f, "lxml")
    lista_link_peliculas = s.find("ul", class_="ListAnimes AX Rows A03 C02 D02").find_all("li")
    for link_pelicula in lista_link_peliculas:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request("https://www3.animeflv.net"+link_pelicula.a['href'], headers=headers)
        f = urllib.request.urlopen(req).read()
        s = BeautifulSoup(f, "lxml")
        titulo = s.find("h1", class_="Title").string.strip()
        if(s.find("span", class_="Type movie") is not None):
            tipo_anime = s.find("span", class_="Type movie").string.strip()
        elif(s.find("span", class_="Type tv") is not None):
            tipo_anime = s.find("span", class_="Type tv").string.strip()
        elif(s.find("span", class_="Type ova") is not None):
            tipo_anime = s.find("span", class_="Type ova").string.strip()
        rating = s.find("span", class_="vtprmd").string.strip()
        num_votos = s.find("span", id="votes_nmbr").string.strip()
        estado = s.find("span", class_="fa-tv").string.strip()
        seguidores = s.find("div", class_="Top").find("span").string.strip()
        datos_generos = s.find("nav", class_="Nvgnrs").find_all("a")
        generos = ""
        if datos_generos:
            generos = datos_generos[0].string.strip()
            for dato in datos_generos[1:]:
                generos = generos + "," + dato.string.strip()
        url_imagen = "https://www3.animeflv.net" + s.find("div", class_="Image").find("figure").find("img")["src"]
        sinopsis = "No tiene sipnosis." if s.find("div", class_="Description").find("p").string is None else s.find("div", class_="Description").find("p").string
        lista_db.append((titulo,tipo_anime,rating,num_votos,estado,seguidores,generos,url_imagen))
        lista_index.append((sinopsis))
    return lista_db,lista_index

def almacenar_animes(numero):
    indice = 0
    animes = []
    lista_animes_db,lista_animes_index = extraer_animes(numero)

    schem = Schema(indice=ID(stored=True), sinopsis=TEXT(stored=True))
    ix = create_in("Index", schema=schem)
    writer = ix.writer()

    for anime_db,anime_index in zip(lista_animes_db,lista_animes_index):
        indice += 1
        carga_imagen(anime_db[7],anime_db[0].replace("/"," "))
        a = Anime(titulo=anime_db[0].replace("/"," "),tipo_anime=anime_db[1],rating=anime_db[2],num_votos=anime_db[3],estado=anime_db[4],seguidores=anime_db[5],generos=anime_db[6],indice=indice)
        animes.append(a)
        writer.add_document(indice=str(indice),sinopsis=anime_index)
    writer.commit()
    Anime.objects.bulk_create(animes)

def almacenar_puntuaciones():
    puntuaciones=[]

    file = open('AnimeData/UserAnimeList.csv', 'r')
    for line in file.readlines()[1:-1]:
        line = line.strip().split(',')
        try:
            anime = Anime.objects.get(titulo=line[1])
            puntuaciones.append(Puntuacion(username=line[0],puntuacion=line[2],anime=anime))
        except:
            continue
    file.close()
    Puntuacion.objects.bulk_create(puntuaciones)

def populateDatabase(numero):
    deleteTableIndex()
    almacenar_animes(numero)
    almacenar_puntuaciones()