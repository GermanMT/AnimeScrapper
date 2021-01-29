Por favor lea este fichero antes de empezar a ver el código:

1. El sistema se ha desarrollado desde una distribución de Linux, en concreto Ubuntu 20.04 LTS, por 
lo cual se recomienda trabajar desde esa distribución.

2. Este proyecto se puede desplegar desde un entorno virtual, si no se quiere utilizar el entorno 
propio de su pc, por evitar instalar dependencias innecesarias en él. Este se puede 
crear con el comando "python3 (Ubuntu) / python (Windows) -m venv nombre" y activar con el comando 
"source nombre/bin/activate" en Ubuntu o "source nombre/Scripts/activate" en Windows.
en la carpeta donde se haya creado. Luego en la carpeta del proyecto se puede desplegar 
con el comando "./manage.py runserver".

3. Antes de comenzar, instalar las dependencias del fichero de requisitos con el comando 
"pip install -r requirements.txt".

4. La base de datos y el indexado han sido cargados scrapeando las 140 páginas de la web donde se han 
estraído los datos y el dataset con las puntuaciones, en total son unos 3200 animes aprox. y unas 
500.000 puntuaciones aprox. Por lo cual recomiendo probar las funcionalidades antes de probar el 
populate, porque cargar tal cantidad de información puede ser tedioso.

5. El anterior punto también puede ser considerado a la hora de cargar el sistema de recomendación.