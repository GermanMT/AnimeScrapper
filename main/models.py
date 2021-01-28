from django.db import models

class Anime(models.Model):
    titulo = models.CharField(max_length=100, verbose_name='Título')
    tipo_anime = models.CharField(max_length=10, verbose_name='Tipo Anime')
    rating = models.FloatField(verbose_name='Rating')
    num_votos = models.IntegerField(verbose_name='Número de Votos')
    estado = models.CharField(max_length=10, verbose_name='Estado')
    seguidores = models.IntegerField(verbose_name='Seguidores')
    generos = models.CharField(max_length=100, verbose_name='Género')
    indice = models.IntegerField(verbose_name='Índice')

class Puntuacion(models.Model):
    username = models.CharField(max_length=30, verbose_name='Username')
    puntuacion = models.IntegerField(verbose_name='Puntuación')
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)