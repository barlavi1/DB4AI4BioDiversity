# DB4AI4BD

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
- query by a range of dates, taxa, and camera na

## Prerequisites
- MySQL or similar
- ###todo: a local_settings.py to fill setting.py file 

## TO DO - maybe?
- add a filter - a user can **query - get** only his data
- UI (tkinter or similar) for data transformation.
- WEB UI

  
