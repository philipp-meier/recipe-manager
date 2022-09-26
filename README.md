# Recipe Manager
Simple, responsive and secure Django CRUD application for recipes with additional features.

![Preview](https://repository-images.githubusercontent.com/541568387/cd040f1d-e94b-4b65-8701-d9b084373a8d)

## Goal
Create my first Django Web Application, which is ready to be (self-)hosted with the knowledge gained in [CS50's Web Programming with Python and JavaScript](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript) and beyond.  

**Note:** This is a learning project I set up to familiarize myself with the Django Web Framework and its features.

## Features
- Works with the Django files/media API to upload and store images.
- Offers a pagination feature, that also accepts a "contains" text filter.
- Makes use of [Bootstrap Icons](https://icons.getbootstrap.com/).
- Is fully responsive by using Bootstrap and media queries.
- Uses some CSS animations for a better user experience.
- Contains API unit tests, that will be extended as this project evolves.
- Is ready to be hosted in a Docker environment and comes with a deployment script (`deploy.sh`) which integrates the currently available unit tests.
- Extends the user login by a simple password validator.
- Is fully available in German and English by making use of [i18n](https://docs.djangoproject.com/en/4.1/topics/i18n/) in the Django templates, the Python backend as well as in the JavaScript files.
- Has a 1:n-association control (`ingredientControl.ts`) which transforms client-side user input to post data on submit.
- Allows users to get random recipe suggestions by using the Python random-functions.
- Uses TypeScript and SCSS for a type-safe and more convenient development experience.
- Is designed to be publicly hosted on GitHub and therefore contains relevant files (e.g. LICENSE).
- Makes use of environment files, that hide secrets and keys from the public GitHub-repository.

## How to run the project
I created a SQLite3 database called `dev.sqlite3`, which contains some demo data, but no media-files / images.  

To run the application, the following commands must be entered:
- `python3 -m pip install -r requirements.txt`: Installs the required Python packages.
- `python3 manage.py compilemessages`: Compiles the localization files.
- `python3 manage.py runserver`: Starts the application.  

The username and password for the demo user is `admin`.

## Required Python packages
All required python packages are documented in the `requirements.txt` file and can be installed with the following command `python3 -m pip install -r requirements.txt`.

## File descriptions
This section describes the files I have created, which are not part of the Django standard setup.
- `deploy.sh`: Deploys this application to my ("production") server after successfully running the unit tests.
- `ssh_host`: File that only contains the ssh host (e.g. "user@ip-address") for `deploy.sh`, so that this information is hidden from the GitHub-repository.
- `requirements.txt`: Contains all python packages that are needed to run this application.
- `prod.env` / `prod-template.env`: Contains the environment variables for the production server and is therefore not in this repository.
- `LICENSE`: Contains the license of this project for the GitHub repository.
- `Dockerfile`: Contains instructions to build a basic Django docker image, that is being used by the docker compose file.
- `docker-compose.yml`: Describes the production environment (NGINX for static file serving and the Django app).
- `dev.sqlite3`: Database with demo data.
- `media`: Contains images, that are being uploaded by the user. This folder will be served by NGINX in a production environment.
- `nginx`: Contains the configuration for the NGINX of the docker-compose.yml.
- `data`: Contains SQLite3 databases.
- `recipes/locale`: Folder that contains the translations for English and German (i18n).
- `recipes/static/recipes/libs`: Contains included libraries/frameworks such as bootstrap-5.2.1.
- `recipes/static/admin`: Contains the static files for the django admin-page.
- `recipes/static/recipes/favicon.ico`: Simple favicon for the recipe manager.
- `recipes/static/recipes/ingredientsControl.ts`: Custom TypeScript-control for adding ingredients (1:n assoc) to a recipe with UI/UX features.
- `recipes/static/recipes/recipeList.ts`: Recipe list control with pagination features.
- `recipes/static/recipes/styles.scss`: Contains custom styles to complement bootstrap.
- `recipes/templates/recipes/index.html`: Start page that shows a specific amount of random recipe suggestions.
- `recipes/templates/recipes/layout.html`: Project layout containing the nav-bar and the search-bar.
- `recipes/templates/recipes/login.html`: Login page template.
- `recipes/templates/recipes/register.html`: Register page template.
- `recipes/templates/recipes/recipe.html`: Form to view, add and edit a specific recipe.
- `recipes/templates/recipes/recipelist.html`: Form that shows all recipes in a list with pagination features.
- `recipes/helper.py`: Contains helper functions such as transforming django objects to data transfer objects (DTOs).
- `recipe_manager/settings.py`: Was strongly modified for production (Database, ALLOWED_HOSTS, SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE, SECRET_KEY,...).

## Project setup
This section describes the relevant steps of the project setup.
- Created a django project in PyCharm Professional.
- Run migrations with `python3 manage.py migrate`.
- Started the django app with `python3 manage.py runserver`.
- Created the recipes-app with `python3 manage.py startapp recipes`.
- Created a `urls.py`-file in the recipes folder.
- Added `recipes/urls.py` to the recipe_manager urls.py.
- Added `recipes` to INSTALLED_APPS in `settings.py`.
- Added `templates/recipes` and `static/recipes` folder and started with `layout.html`.
- Added bootstrap 5.2.1 to the static files (`recipes\static\recipes\libs`).
- Added user auth (settings.py - `AUTH_USER_MODEL = "recipes.User"`).
- Created a super user with `python3 manage.py createsuperuser`.
- Added needed models to `admin.py`.
- Installed "gettext" for i18n with `sudo apt install gettext`.
- Created locals with `django-admin makemessages -l de` and ` python3 manage.py makemessages -l en`. To compile the messages, run the following command: `python3 manage.py compilemessages`.
- Moved the static files of django-admin with `python3 manage.py collectstatic` to the new static root.
- Introduced env-variables to `settings.py`.
- Added docker support.

## Further ideas / goals
- Rate recipes
- Print recipes
- Find recipes by ingredient(s)
- Filter recipe categories
- User permissions ("Viewer", "Administrator")
- Normalizing the ingredient table, *if* beneficial in the future
- Login "throttling" against bruteforce attacks
- Two-factor authentication
- Keycloak integration/support
- Release notes and [SemVer](https://semver.org/)

## Useful scripts
### Generate SECRET_KEY
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
