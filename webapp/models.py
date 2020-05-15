from django.db import models


# Create your models here.


class CourseVideos(models.Model):
    VideoId= models.AutoField(primary_key=True)
    fileTitle= models.CharField(max_length=100 , default="keywords")
    imageFile=models.FileField(upload_to="excelList/", default="Video.mp4")
    graphImage=models.ImageField(upload_to="data/", default='image.png')
    
    def __str__(self):
        return self.fileTitle

