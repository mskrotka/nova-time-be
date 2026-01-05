# [NAZWA APLIKACJI]

## Uruchamianie aplikacji

1. Utwórz plik `.env`: `make env`
2. Uruchom kontenery: `make up`
3. Wykonaj istniejące migracje: `make migrate`
4. Wgraj dane początkowe: `make fix`
5. Aplikacja jest dostępna pod adresem `localhost:80`

## Komendy Make

### OGÓLNE
| KOMENDA | OPIS |
|-----------|-----------|
|**env**|`cp .env_example .env`|
|**app_shell**|`docker exec -it fimas-app bash`|
|**shell_plus**|`docker exec -it fimas-app python manage.py shell`|
|**fix**|`docker exec -it fimas-app python manage.py loaddata core/fixtures/admin_user.json`|
|**migrate**|`docker exec -it fimas-app python manage.py migrate`|
|**migrations**|`docker exec -it fimas-app python manage.py makemigrations`|
|**test**|`docker exec -it fimas-app python manage.py test`|
|**logs**|`docker logs -f $(container)`|

### WERSJA DEV
| KOMENDA | OPIS |
|-----------|-----------|
|**up**|`docker compose -f docker-compose.dev.yaml up -d`|
|**stop**|`docker compose -f docker-compose.dev.yaml stop`|
|**build**|`docker compose -f docker-compose.dev.yaml up --force-recreate --build`|
|**clean-migrations**|`find . -path "*/migrations/*.py" -not -name "__init__.py" -delete`|
|**clean-migrations**|`find . -path "*/migrations/*.pyc" -delete`|
|**startapp**|`docker exec -it fimas-app python manage.py startapp $(name)`|

### WERSJA PROD
| KOMENDA | OPIS |
|-----------|-----------|
|**up-prod**|`docker compose -f docker-compose.prod.yaml up -d`|
|**stop-prod**|`docker compose -f docker-compose.prod.yaml stop`|
|**build-prod**|`docker compose -f docker-compose.prod.yaml up -d --force-recreate --build`|

## Informacje ogólne
* Daty podawane w bazie są w milisekundach od 1970-01-01 00:00:00.000 (timestamp).
* Loginem jest adres email.

## Tworzenie logów
* Logi systemowe są tworzone w katalogu `app/logs/`.
* Logi są podzielone na dwa pliki: `debug.log` i `error.log`.
* Logi są tworzone w czasie rzeczywistym.
* Logi można wykorzystać w dowolnym miejscu w kodzie.

```python
import logging

logger = logging.getLogger(__name__)
logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical message')
```

## Rozwój projektu

### Hooki pre-commit

[Pre-commit](https://pre-commit.com/) automatycznie uruchamia narzędzia takie jak mypy, black, isort aby zapewnić jakość kodu i zgodność z regułami PEP8.

Po sklonowaniu repozytorium, uruchom `pre-commit install` aby zainstalować hooki.

Po wysłaniu zmian do repozytorium, uruchom `pre-commit run` aby sprawdzić wszystko.

### Makefile

> Upewnij się, że masz zainstalowane make.
>
> Ubuntu/Debian: `$ sudo apt-get install build-essential`
>
> Mac: `$ brew install make`
>
> Windows (jak zawsze, bardziej skomplikowane) https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows

Makefile został stworzony dla wygodnego używania wszystkich rodzajów komend związanych z projektem. Możesz dodać więcej, ale pamiętaj o aktualizacji README.

### Dane początkowe

Zaktualizuj uprawnienia administratora do panelu admina w `core/fixtures/admin_user.json`, obecnie są domyślne:

* login: admin@email.pl
* hasło: admin

> Jak wygenerować nowe zahaszowane hasło? Upewnij się, że uruchomiłeś kontener `$ make up`
>
> 1. Wejdź do powłoki django w kontenerze: `$ make shell_plus`
>
> 2. Zaimportuj generator haseł: `$ from django.contrib.auth.hashers import make_password`
>
> 3. Zakoduj swoje nowe hasło: `$ make_password('test')`
> 4. Skopiuj zahaszowane hasło i wklej w pliku fixtures.
> 5. Wpisz `$ exit()` aby wyjść.



## CI/CD

| ZMIENNA | WARTOŚĆ |
|-----------|-----------|
|**DEV_DESTINATION**|`[użytkownik]@[adres IP]:/[użytkownik]/[projekt]`|
|**DEV_KEY**|`Klucz prywatny z serwera` W authorized_keys powinien znajdować się klucz publiczny .pub z serwera|
|**DEV_HOST**|`IP serwera`|
|**DEV_USER**|`root` dla hostingera|

W pliku ci_cd.yml ustaw brancha oraz komendy do wykonania i nazwę joba.
