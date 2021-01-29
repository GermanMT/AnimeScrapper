from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from main.populate import populateDatabase
from main.models import *
from main.forms import *
from main.recommendations import cargaDict_items,transformPrefs,calculateSimilarItems,getRecommendations,topMatches
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
import shelve
from random import randrange

def inicio(request):
    num_animes=Anime.objects.all().count()
    num_puntuaciones=Puntuacion.objects.all().count()
    return render(request,'inicio.html',{'num_animes':num_animes,'num_puntuaciones':num_puntuaciones})

def carga(request):
    formulario = NumeroDePaginasForm()

    if request.method=='POST':
        formulario = NumeroDePaginasForm(request.POST)
        if formulario.is_valid():      
            populateDatabase(formulario.cleaned_data['numero'])
            return render(request, 'cargaBD.html')
    return render(request, 'confirmacionBD.html', {'formulario':formulario})

def cargaRS(request):
    if request.method=='POST':
        if request.POST.get("Aceptar"):
            cargaDict_items()
            return render(request, 'cargaRS.html')
    return render(request, 'confirmacionRS.html')

def buscar_sinopsis_fordb(indice):
    ix=open_dir("Index")
    with ix.searcher() as searcher:
        query = QueryParser("indice", ix.schema).parse(str(indice))
        results = searcher.search(query)
        for r in results:
            sinopsis = r['sinopsis']
    return sinopsis

def buscar_titulo(request):
    formulario = BusquedaPorTituloForm()
    animes = None
    result = {}

    if request.method=='POST':
        formulario = BusquedaPorTituloForm(request.POST)      
        if formulario.is_valid():
            animes = Anime.objects.filter(titulo__icontains=formulario.cleaned_data['titulo'])
            num=len(animes)
            if num > 31:
                random = randrange(num-31)
                animes = animes[random:random+30]
            elif num == 31:
                animes = animes[0:30]
            for anime in animes:
                result[anime] = buscar_sinopsis_fordb(anime.indice)
    return render(request, 'animespor.html', {'formulario':formulario, 'result':result})

def buscar_tipo(request):
    formulario = BusquedaPorTipoForm()
    animes = None
    result = {}
    
    if request.method=='POST':
        formulario = BusquedaPorTipoForm(request.POST)      
        if formulario.is_valid():
            animes = Anime.objects.filter(tipo_anime__exact=formulario.cleaned_data['tipo'])
            #Cogemos 30 animes random del tipo para que el usuario pueda probar a conocer uno
            #de ese tipo, sin cargar todos para reducir tiempos
            num=len(animes)
            if num > 31:
                random = randrange(num-31)
                animes = animes[random:random+30]
            elif num == 31:
                animes = animes[0:30]
            for anime in animes:
                result[anime] = buscar_sinopsis_fordb(anime.indice)
    return render(request, 'animespor.html', {'formulario':formulario, 'result':result})

def buscar_sinopsis(request):
    formulario = BusquedaPorSinopsisForm()
    animes = None
    result = {}

    if request.method=='POST':
        formulario = BusquedaPorSinopsisForm(request.POST)      
        if formulario.is_valid():
            ix=open_dir("Index")
            with ix.searcher() as searcher:
                query = QueryParser("sinopsis", ix.schema).parse(formulario.cleaned_data['sinopsis'])
                results = searcher.search(query)
                for r in results:
                    anime = Anime.objects.get(indice__exact=r['indice'])
                    result[anime] = r['sinopsis']
    return render(request, 'animespor.html', {'formulario':formulario, 'result':result})

def buscar_genero(request):
    formulario = BusquedaPorGenerosForm()
    animes = Anime.objects.all()
    result = {}
    
    if request.method=='POST':
        formulario = BusquedaPorGenerosForm(request.POST)      
        if formulario.is_valid():
            for genero_in in formulario.cleaned_data['genero']:
                animes = animes & Anime.objects.filter(generos__icontains=genero_in)
            num=len(animes)
            print(num)
            if num > 31:
                random = randrange(num-31)
                animes = animes[random:random+30]
            elif num == 31:
                animes = animes[0:30]
            for anime in animes:
                result[anime] = buscar_sinopsis_fordb(anime.indice)
    return render(request, 'animespor.html', {'formulario':formulario, 'result':result})

def animes_parecidos(request):
    mensaje = "En esta sección te recomendamos animes en base a lo parecidos que sean al anime que quieras."
    anime = None
    formulario = BusquedaPorTituloForm()

    if request.method=='POST':
        formulario = BusquedaPorTituloForm(request.POST)
        if formulario.is_valid():
            titulo = formulario.cleaned_data['titulo']
            try:
                anime = get_object_or_404(Anime, titulo=titulo)
            except:
                mensaje_error = "El título introducido no corresponde a ningún anime. Vuelva a intentarlo de nuevo."
                return render(request,'animes_recomendados.html', {'formulario': formulario,'mensaje':mensaje,"mensaje_error":mensaje_error})
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, anime.id,n=5)
            libros = []
            similar = []
            for re in recommended:
                libros.append(Anime.objects.get(id=re[1]))
                similar.append(re[0])
            items= zip(libros,similar)
            return render(request,'animes_recomendados.html', {'formulario': formulario,'items': items,'mensaje':mensaje})
    return render(request,'animes_recomendados.html', {'formulario': formulario,'mensaje':mensaje})

def animes_recomendados_puntuacion(request):
    mensaje = "En esta sección te recomendamos animes en base a las puntuaciones que han dado a los animes de esta web."
    formulario = FormularioUsername()

    if request.method=='POST':
        formulario = FormularioUsername(request.POST)
        if formulario.is_valid():
            username = formulario.cleaned_data['username']
            try:
                user = get_list_or_404(Puntuacion, username=username)
            except:
                mensaje_error = "El usuario introducido es invalido. Vuelva a intentarlo de nuevo."
                return render(request,'animes_recomendados.html', {'formulario': formulario,'mensaje':mensaje,"mensaje_error":mensaje_error})
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            shelf.close()
            rankings = getRecommendations(Prefs,username)
            recommended = rankings[:5]
            animes = []
            scores = []
            for re in recommended:
                animes.append(Anime.objects.get(id=re[1]))
                scores.append(re[0])
            items= zip(animes,scores)
            return render(request,'animes_recomendados.html', {'formulario': formulario,'items': items,'mensaje':mensaje})
    return render(request,'animes_recomendados.html', {'formulario': formulario,'mensaje':mensaje})