from PIL import Image
import PIL.ExifTags
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from django.core.exceptions import ValidationError
from .models import *
def GetImageExif(filepath):
    image = Image.open(filepath)
    exif_data = image._getexif()
    exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in image._getexif().items()
            if k in PIL.ExifTags.TAGS
    }
    #image.close()
    return exif

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name , max_length=None):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def GetVideoExif(vid):
    ti_m = os.path.getmtime(vid)
    datetimeObj = datetime.datetime.fromtimestamp(ti_m)
    # = datetime.datetime.fromtimestamp(ti_m).isoformat().replace("T"," ")
    return datetimeObj



def GetData(request):
    #print(request.data)
    filePath = request.data['File']
    locationid = Location.objects.get(locationid = request.data['locationid'])
    samplingProtocol = request.data['sampling_protocol'] if 'sampling_protocol' in request.data else "unknown"
    eventRemarks = request.data['comments'] if 'comments' in request.data else ""
    sequnece = request.data['sequenceid'] if 'sequenceid' in request.data else None
    cameraid = request.data['cameraid'] if 'cameraid' in request.data else None
   
    ImgData = {'filepath' : filePath, 'samplingProtocol': samplingProtocol, 'eventRemarks' : eventRemarks, 'locationid' : locationid, 'sequenceid' : sequnece, 'cameraid' : cameraid, 'eventDate' : request.data['date_time']}
    return(ImgData)

def ValidateData(request):
    if 'File' not in request.data: raise ValidationError("No file was uploaded")
    if 'locationid' not in request.data: raise ValidationError("No locationid was provided")
    elif  len(Location.objects.filter(locationid = request.data['locationid'])) == 0: raise ValidationError("No such location_id")
    if 'date_time' not in request.data: raise ValidationError("No date_time was provided")
    return GetData(request)


def ValidateDateTime(exif):
    try:
        timestamp = datetime.strptime(exif['DateTimeOriginal'],'%Y:%m:%d %H:%M:%S')
    except:
        try:
            timestamp = datetime.strptime(exif['DateTimeOriginal'],'%Y-%m-%d %H:%M:%S' )
        except:
            raise ValidationError("datetime is in a wrong format")
    return(exif['DateTimeOriginal'])



def ConvertVideo(NewVideo):
    """
    convet videos to sherable format
    """
    Directory = os.path.dirname(NewVideo.filepath.path)
    FileName = os.path.basename(NewVideo.filepath.path)+".ogg"
    NewDir = Directory.replace('media/videos', 'media/videos_to_share', 1)
    NewPath = os.path.join(NewDir,FileName)
    os.makedirs(NewDir, exist_ok=True)
    cmd = "ffmpeg -i " + NewVideo.filepath.path + " -c:a libvorbis -c:v libtheora " + os.path.join(Directory,FileName) +" -map 1 -c copy"
    output = subprocess.run(cmd, shell = True)
    shutil.move(os.path.join(Directory,FileName), NewDir)
    f = open(os.path.join(NewDir,FileName),'rb')
    newSharedVideo = SharedVideo(
        videoid = NewVideo,
        filepath = File(f)
    )
    newSharedVideo.save()
    f.close()






