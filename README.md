# AI4Biodiversity django backend
This backend server was built to help ecologists monitor animal activity through camera-trap images and videos.

## Functionalities
* Upload images.
* Upload annotations (taxonomy, sex, lifestage, behavior).
* Upload videos.
* Object detection over the image to create bounding boxes around animals (not included in this repository).
* User input of each object.
* Handle a database for future queries.
* Download CSV files and zip of images in [Zooniverse](https://www.zooniverse.org/) format.
* Permission system for group work and isolated each data collection project management.
* A Sherable flag to mark videos as shareable for viewing.
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
* Auth directory should be provided (you can address me for help with auth dict).

### Database init
On my app I used mySQL, but the models support any database.
Important notes:
* Create an empty database
* Create username (with password) with the permissions to read-write the crated database
* make sure the DATABASES part in the settings is following Django documentation.
* once the above is done, initiate the database. the following commands will create the tables under the designated database:
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

### Run Server
Make sure the DEBUG flag is set to True in the setting.py, and run the server (by default, it will run on port 8080)
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

| Route | Request Type Allowed | Payload | Details |
| ----- | -------------------- | ------- | ------- |
| /auth/get_token/ | POST | {username: str, password: str} | get access token and refresh token |
| /auth/token_refresh | POST | { refresh: str } | refresh expired access token |
| /auth/logout/ | POST | | blacklist the access token and the refresh token | 
| /api/add-new-image/ | POST | { File : full_path_to_image, cameraid : str (optional), date_time : str (optional), locationid : str (optional), count : int (optional), taxon : FK (optional), sex : FK (optional), lifestage : FK (optional), behavior : FK (optional) } | Add new image. date_time and camera id should be provided via exif or request. image can be uploaded with annotation or without annotation |
| /api/add-new-video/ | POST | { File : full_path_to_video, cameraid : str, locationid : FK (optional), Sherable : boolean} | Add new video. a valid datetime should be provided via exif | 
| api/Zooniverse/ | GET | { cameraid : str, start : str, end : str, taxonid : FK , interval : int} | query database according to camera, daterange and taxon. calculate events according to time interval and export data in zooniverse format to a csv together with a zipped folder of the relevant images and videos|
| api/QueryByPolygon/ | GET | {polygon : str } | query data by polygon and return an histogram (as dict) |





  
