# AI4Biodiversity django backend
This backend server was build to help ecologists monitor animals activity.

## Functionalities
* Upload images.
* Upload annotations (taxonomy, sex, lifestage, behavior).
* Upload videos.
* Object detection over the image to create bounding boxes around animals (not included in this repository).
* User input of each object.
* Handle a database for future queries.
* Download CSV files and zip of images in [Zooniverse](https://www.zooniverse.org/) format.
* Permission system for group work and isolated each data collection project management.
* A Sherable flag to mark videos as sherable for view.
* Communicate using JWT only

## Prerequisites
### Missing Parts
There are a few files missing from this repository, to make it fully functional:
local_settings.py: filling the missing parts at the setting.py file
```
   SECRET_KEY = '<your very secret key from environment>'
   ALLOWED_HOSTS = ['list of allowed hosts to redirect requests']
   DATABASES = {'a dictionary': 'of the databases credentials, see Django docs'}
```

### Database init
On my stack I used mySQL, but the models support any database.
Important notes:
* Create an empty database
* Create username (with password) with the permissions to read-write the crated database
* make sure the DATABASES part in the settings is following Django documentation.
* once the above are done, initiate the database. the following commands will create the tables under the designated database:
```
   python manage.py makemigrations
   python manage.py migrate
```
* Check the tables created properly

### Django Admin
* Before accessing the Admin UI, first you need to set an
```
   python manage.py createsuperuser
```
* Create the static files for the Admin UI design
```
   python manage.py collectstatic
```
admin user:

### Run Server
Make sure the DEBUG flag set to True in the setting.py, and run the server (by default, it will run on port 8080)
see further details in the Django documentation
```
   python manage.py runserver
```
* Admin UI can be found at: http:localhost:<your_port>/admin/
* Enter with the Admin credentials you have set when creating superuser

## API:
### Prolog
To send a REST request, you need a username and password on the server.
A username and password can be set only by the Admin, using the Admin UI.
Every request needs to hold in the Authorization a Bearer and a Token.
Example, a GET request:
```
curl -H 'Authorization: Bearer <access token>' -X GET <server_address>:<port>/<request_route>
```

### Routes
For further information how to use curl check the [docs](https://curl.se/docs/tutorial.html).
Django
Django REST Framework
Simple JWT

Image processing using:

OpenCV

It is tailored for animal object detection ML.
Currently, it is implemented on STARTdbi project for insects
(this is the reason you might encounter some insect-related characterizations).
# DB4AI4BioDiversity



This database was built in [Django](https://www.djangoproject.com/) with [TDWG](https://www.tdwg.org/) in mind, in order to handle camera-trap data.
Currently, the database exports data to the [Zooniverse](https://www.zooniverse.org/) format.

## Technologies
this database was tested using MySQL un ubuntu22.04, yet it can support other structures.

## Functionalities
- load videos and images (with EXIF data)
- add taxonomy
- download CSV files and zip of images

### post 
- load image (https://url-path//add-new-image)
- load videos (https://url-path//add-new-video)

### query - get
- query by polygon
- query by a range of dates, taxa, and camera name

## Prerequisites
- MySQL or similar
- Fill setting.py with your database and path. 

## TO DO
- add a filter - a user can **query - get** only his data
- UI (tkinter or similar) for data transformation.
- WEB UI
- a local_settings.py and a code to fill setting.py file 

  
