from django.db import models
# import django.utils.timezone as timezone
from django.core.validators import RegexValidator,MinLengthValidator


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class UserInput(models.Model):

    university = models.CharField(max_length=50,default='na')
    # email = models.EmailField()
    school = models.CharField(max_length=50,default='na')
    name = models.CharField(max_length=20)
    st_year_mon = models.CharField(max_length=7,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[0-9]{4}(\-[0-9]{2}){0,1}$',
                message='Only xxxx or xxxx-xx are allowed.'
            )
        ],
        default='0000') #models.CharField(max_length=50)
    end_year_mon =  models.CharField(max_length=7,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[0-9]{4}(\-[0-9]{2}){0,1}$',
                message='Only xxxx or xxxx-xx are allowed.'
            )
        ],
        default='0000') #models.CharField(max_length=50)
    note = models.TextField()
    class Meta:
        app_label = 'roster'

    def __str__(self):
        return '-'.join(self.university,self.school,self.name)+":["+self.st_year_mon+','+self.end_year_mon+']'
#'university','school','name', 'st_year_mon','end_year_mon', 'note'
