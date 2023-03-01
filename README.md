### Image API

The project was created in the scope of a probation task for the Backend (Python + Django) Engineer position. The goal of the project is to show technical skills and knowledge of the candidate - Denis Vasin

The original task was described as:
_______________________________________________________
Using Django REST Framework, write an API that allows any user to upload an image in PNG or JPG format.

You are allowed to use any libraries or base projects / cookie cutters you want (but using DRF is a hard requirement).

Skip the registration part, assume users are created via the admin panel.

Requirements:
it should be possible to easily run the project. docker-compose is a plus
users should be able to upload images via HTTP request
users should be able to list their images
there are three bultin account tiers: Basic, Premium and Enterprise:
users that have "Basic" plan after uploading an image get: 
a link to a thumbnail that's 200px in height
users that have "Premium" plan get:
a link to a thumbnail that's 200px in height
a link to a thumbnail that's 400px in height
a link to the originally uploaded image
users that have "Enterprise" plan get
a link to a thumbnail that's 200px in height
a link to a thumbnail that's 400px in height
a link to the originally uploaded image
ability to fetch a link to the (binary) image that expires after a number of seconds (user can specify any number between 300 and 30000)
apart from the builtin tiers, admins should be able to create arbitrary tiers with the following things configurable:
arbitrary thumbnail sizes
presence of the link to the originally uploaded file
ability to generate expiring links
admin UI should be done via django-admin
there should be no custom user UI (just browsable API from Django Rest Framework)
remember about:
tests
validation
performance considerations (assume there can be a lot of images and the API is frequently accessed)


Please focus on code cleanliness and quality.
_______________________________________________________

So, the solution is presented in the form of a Django project, based on the Django Rest Framework and available on GitHub with supportive details in the README file.

###How to install and run the project

The project can be cloned\copied for the GitHub repo and deployed to a local machine or remote server. Because of testing purpose and limited time, the project can not be considered as a "product ready product" and will require some additional tweaks and configuration if it should be moved to the real production mode.

***Here is the list of important parts of the project:***
(accounts/) : folder with application for customized management of users thru the django-admin panel
(django_project/) : main configuration for the projec`t
(images/) : main application for the Image API
(media/) : folder for the uploaded images
.gitignore: file with exceptions for Git
db.sqlite3: file with DB (contains the initial plans)
manage.py: Django management tool
requirements.txt: file with the list of required packages
README: file with the description

***The instructions:***
* Clone\copy the folder from GitHub repo
* (Optional) configure and run VEnv (for the local development)
* Install all the required packages `pip install -r requirements.txt`
* Run `python manage.py runserver`
* Access API by provided URL (http://127.0.0.1) by default
* Create admin `python manage.py createsuperuser`

### Description of Image API
Based on the requirements, API have support for the image upload and return information about all users images or about the one identified by ID
The full schema provided by the Spectacular module is available in file `schema.yml` or by web through the route (api/schema/). Also there is access for the auto-generated documentation by route (api/schema/redoc/).

### Trade-offs
Because of limited time and shortage of description within the requirements, author decided to limit some functionality. 
* Project is not production ready
* Because it's not clear - how time-limited access should work, author assumed that can be just a time since the image creation moment
* Access is based on the basic authentication (provided by Django+DRF)
* Each thumbnail is generated only after the 1st request: that allows to save some space if nobody will request it and decrease time for initial creation of the image, but it will require additional cleanup in the future if the user plan doesn't allow some sizes anymore. Also, it could lead to some difficulties with scalability: it would require an additional efforts to keep distributed file storages in sync.
* Requirements don't contain the part about access to the files (they describes just the links), so this part has limited functionality and shows ability to implement more functionality if needed

### Next steps
Of course, project can be improved in many ways:
Configurable list of supported formats
Better management for users and plans
More options for the each plan: formats, restrictions, ability to download any thumbnail 
