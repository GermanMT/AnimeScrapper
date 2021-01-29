from django import forms

class NumeroDePaginasForm(forms.Form):
    numero = forms.IntegerField(min_value=1, max_value=140, label="Introduzca el número de paginas que quiere cargar ", required=True)

class BusquedaPorTituloForm(forms.Form):
    titulo = forms.CharField(label="Introduzca el título ", required=True)

class BusquedaPorTipoForm(forms.Form):
    choices = (('Anime', 'Anime'),('OVA', 'OVA'),('Película', 'Película'))
    tipo = forms.ChoiceField(label="Tipo ",choices=choices, required=True)

class BusquedaPorSinopsisForm(forms.Form):
    sinopsis = forms.CharField(label="Introduzca la sinopsis ", required=True)

class BusquedaPorGenerosForm(forms.Form):
    choices = (("Acción", "Acción"),("Ciencia Ficción", "Ciencia Ficción"),
        ("Deportes", "Deportes"),("Espacial", "Espacial"),("Infantil", "Infantil"),
        ("Mecha", "Mecha"),("Parodia", "Parodia"),("Romance", "Romance"),("Shounen", "Shounen"),
        ("Terror", "Terror"),("Artes Marciales", "Artes Marciales"),("Comedia", "Comedia"),
        ("Drama", "Drama"),("Fantasía", "Fantasía"),("Josei", "Josei"),("Militar", "Militar"),
        ("Policía", "Policía"),("Samurai", "Samurai"),("Sobrenatural", "Sobrenatural"),
        ("Vampiros", "Vampiros"),("Aventuras", "Aventuras"),("Demencia", "Demencia"),("Ecchi", "Ecchi"),
        ("Harem", "Harem"),("Juegos", "Juegos"),("Misterio", "Misterio"),("Psicológico", "Psicológico"),
        ("Seinen", "Seinen"),("Superpoderes", "Superpoderes"),("Yaoi", "Yaoi"),("Carreras", "Carreras"),
        ("Demonios", "Demonios"),("Escolares", "Escolares"),("Historico", "Historico"),
        ("Magia", "Magia"),("Música", "Música"),("Recuentos de la vida", "Recuentos de la vida"),
        ("Shoujo", "Shoujo"),("Suspenso", "Suspenso"),("Yuri", "Yuri"))
    genero = forms.MultipleChoiceField(label="Genero ", widget=forms.CheckboxSelectMultiple(attrs={"class": "select_generos"}), choices=choices)

class FormularioUsername(forms.Form):
    username = forms.CharField(label="Introduzca su usuario ", required=True)