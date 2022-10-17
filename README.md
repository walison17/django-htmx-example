# Projeto HTMX

Para popular o banco com as músicas e artistas

Entre no shell:
````
python manage.py shell
````
faça o import:
````
from django.core.management import call_command
````
e depois o comando:
````
call_command("import_songs", "songs.csv")
````
aparecendo a msg abaixo:
````
2229 músicas de 475 artistas foram importadas.
````
deu tudo certo!!!