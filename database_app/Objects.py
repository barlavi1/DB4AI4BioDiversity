

class MediaInfo:
    def __init__(self, mediaid, deploymentid, sequenceid, capturemethod, timestamp, filepath, filemediatype, exifdata, favourite,comments,field_id):
            self.mediaid=mediaid
            self.deploymentid = deploymentid
            self.sequceid=sequenceid
            self.capturemethod = capturemethod
            self.timestamp = timestamp
            self.filepath = filepath
            self.filemediatype = filemediatype
            self.exifdata = exifdata
            self.favourite = favourite
            self.comments = comments
            self.field_id = field_id

class ImgInfo:
    def __init__(self,start,end,imgType,supraeventid,cameraid,animal,imgName,locationName):
        self.start=start
        self.end=end
        self.supraeventid=supraeventid
        self.cameraid=cameraid
        self.imgType=imgType
        self.animal=animal
        self.imgName=imgName
        self.locationName = locationName




class AddImage:
    def __init__(self,image):
        self.filepath = image



class PolyInfo:
    def __init__(self, eventid, animal, deploymentid, point):
        self.eventid = eventid
        self.animal =  animal
        self.deploymentid = deploymentid
        self.point = point


