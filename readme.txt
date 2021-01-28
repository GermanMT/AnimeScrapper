Por favor lea este fichero antes de empezar a ver el código:

1. Este proyecto se puede desplegar desde un entorno virtual, si no se quiere utilizar el entorno 
propio de su pc para usarlo, por evitar de instalar dependencias innecesarias en él. Este se puede 
crear con el comando "python3 -m venv nombre" y activar con el comando source nombre/bin/activate 
en la carpeta donde se haya creado. Luego en la carpeta del proyecto se puede desplegar 
con el comando "./manage.py runserver".

2. Antes de comenzar, instalar las dependencias del fichero de requisitos con el comando 
"pip install -r requirements.txt".

3. La base de datos y el indexado han sido cargados escrapeando las 140 páginas de la web donde he 
estraído los datos y el dataset con las puntuaciones, en total son unos 3200 animes aprox. y unas 
500.000 puntuaciones aprox. Por lo cual recomiendo probar las funcionalidades antes de probar el 
populate, porque cargar tal cantidad de información puede ser tedioso.

4. El anterior punto también puede ser considerado a la hora de cargar el sistema de recomendación.