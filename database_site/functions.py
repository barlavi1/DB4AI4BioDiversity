from PIL import Image
import PIL.ExifTags


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


