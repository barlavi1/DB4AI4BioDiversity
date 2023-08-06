# DB4AI4BD

This database was built in [Django](https://www.djangoproject.com/) with [TDWG](https://www.tdwg.org/) in mind, in order to save and transform data from camera-trap to different standards.
Currently, the database exports data to the [Zooniverse](https://www.zooniverse.org/) format.

## Technologies
I built and tested the database using MySQL un ubuntu22.04, yet it can support other structure.

## Functionalities
- load videos and images with exif data
- add object taxnomony
- download CSV files and zip of images

### post 
- load image (https://url-path//add-new-image)
- and videos (https://url-path//add-new-video)

### query - get
- query by polygon
- query by range of dates, taxa and camera

## Prerequisites
- MySQL or similar
- ###todo: a local_settings.py to fill setting.py file 
- 

