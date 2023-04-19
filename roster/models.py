from django.db import models
# import django.utils.timezone as timezone
from django.core.validators import RegexValidator,MinLengthValidator
from django.conf import settings
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _lazy

import datetime
import hashlib
import uuid
from typing import Any
from .reference_list import university_pilot_list

# from model_utils import Choices

# # Create your models here.
# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#
#     def __str__(self):
#         return self.title

# class UserInput(models.Model):
#
#     university = models.CharField(max_length=50,default='na')
#     # email = models.EmailField()
#     school = models.CharField(max_length=50,default='na')
#     name = models.CharField(max_length=20)
#     st_year_mon = models.CharField(max_length=7,
#         validators=[
#             MinLengthValidator(4),
#             RegexValidator(
#                 regex=r'^[0-9]{4}(\-[0-9]{2}){0,1}$',
#                 message='Only xxxx or xxxx-xx are allowed.'
#             )
#         ],
#         default='0000') #models.CharField(max_length=50)
#     end_year_mon =  models.CharField(max_length=7,
#         validators=[
#             MinLengthValidator(4),
#             RegexValidator(
#                 regex=r'^[0-9]{4}(\-[0-9]{2}){0,1}$',
#                 message='Only xxxx or xxxx-xx are allowed.'
#             )
#         ],
#         default='0000') #models.CharField(max_length=50)
#     note = models.TextField()
#     class Meta:
#         app_label = 'roster'
#
#     def __str__(self):
#         return '-'.join([self.university,self.school,self.name])+":["+self.st_year_mon+','+self.end_year_mon+']'
# #'university','school','name', 'st_year_mon','end_year_mon', 'note'




class DeanInfo(models.Model):
    """
    have chinese translation for all the variable names
    perhaps also add a clickable info button to check the definition of the variable
    """
    #---------------------Institution info ----------------
    """ do not allow for missing in any of these fields"""
    university_choice=university_pilot_list
    university = models.CharField(max_length=50,choices=university_choice,default='na')

    """
    reminder here: english name from the official website, not chinese translation
    """
    university_en= models.CharField(max_length=50,default='na')

    #university category: 985, 211, 985&211,
    university_cls_choice=[('985','985'),
                           ('211','211'),
                           ('985&211','985&211'),
                           ('none','none')]
    university_category = models.CharField(max_length=7,choices=university_cls_choice,default='na')


    school = models.CharField(max_length=50,default='na')
    school_en= models.CharField(max_length=50,default='na')

    school_cls_choice=[
                    ('econ','economics'),
                    ('life','life_science'),
                    ('chem','chemistry'),
                    ('phys','physics'),
                    ('macs','math&computer_science'),
                    ('soci','sociology'),
                    ('pol','poliscience'),
                    ('gov','govmanagement')]
    school_category = models.CharField(max_length=4,choices=school_cls_choice,default='na')


    #---------------------name and tenure period ----------------
    """ do not allow for missing in any of these fields"""
    name_first = models.CharField(max_length=20)
    name_last = models.CharField(max_length=20)

    gender_choice=[('female','女'),
                   ('male','男')]
    gender = models.CharField(max_length=6,choices=gender_choice)
    is_name_common= models.CharField(max_length=20,choices=[("1","是"),("0","否")]) #true or false

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

    #---------------------graduation---------------
    institution_phd_graduation=models.CharField(max_length=20)#allow for missing value
    country_phd_graduation=models.CharField(max_length=20)#allow for missing value
    whether_oversea_phd=models.CharField(max_length=3,choices=[("1",'是'),("0",'否')],default='na')
    year_phd_graduation=models.CharField(max_length=4,
            validators=[
        MinLengthValidator(4),
        RegexValidator(
            regex=r'^[0-9]{4}$',
            message='Only xxxx are allowed.'
        )
        ],
            default='0000')#allow for missing value
    year_phd_graduation_info_url=models.URLField() #allow for missing value


    #---------------------scopus info ----------------
    scopus_auid=models.CharField() # allow to have multiple or missing at all
    scopus_auprofile_url=models.URLField()
    scopus_h_index_till_2022=models.CharField(max_length=20)


    #---------------------OCRID ----------------
    OCRID=models.CharField(max_length=20)#allow for missing value

    #---------------------wanfang ----------------
    WF_scholar_id=models.CharField(max_length=20)#allow for missing value
    WF_h_index_till_2022=models.CharField(max_length=20)#allow for missing value

    #---------------------CV ----------------
    """do not allow for missing"""
    edu_background_string = models.TextField()
    edu_background_url= models.URLField()
    CV_string = models.TextField()
    CV_string_url= models.URLField()


    class Meta:
        app_label = 'roster'

    def __str__(self):
        return '-'.join([self.university,self.school,self.name_last,self.name_first])+":["+self.st_year_mon+','+self.end_year_mon+']'


#-----------track user visit-----------------------------

# def parse_remote_addr(request: HttpRequest) -> str:
#     """Extract client IP from request."""
#     x_forwarded_for = request.headers.get("X-Forwarded-For", "")
#     if x_forwarded_for:
#         return x_forwarded_for.split(",")[0]
#     return request.META.get("REMOTE_ADDR", "")
#
#
# def parse_ua_string(request: HttpRequest) -> str:
#     """Extract client user-agent from request."""
#     return request.headers.get("User-Agent", "")
#
#
# class UserVisitManager(models.Manager):
#     """Custom model manager for UserVisit objects."""
#
#     def build(self, request: HttpRequest, timestamp: datetime.datetime):
#         """Build a new UserVisit object from a request, without saving it."""
#         uv = UserVisit(
#             user=request.user,
#             timestamp=timestamp,
#             session_key=request.session.session_key,
#             remote_addr=parse_remote_addr(request),
#             ua_string=parse_ua_string(request),
#             context=REQUEST_CONTEXT_EXTRACTOR(request),
#         )
#         uv.hash = uv.md5().hexdigest()
#         return uv

# class UserVisit(models.Model):
#     """
#     Record of a user visiting the site on a given day.
#     This is used for tracking and reporting - knowing the volume of visitors
#     to the site, and being able to report on someone's interaction with the site.
#     We record minimal info required to identify user sessions, plus changes in
#     IP and device. This is useful in identifying suspicious activity (multiple
#     logins from different locations).
#     Also helpful in identifying support issues (as getting useful browser data
#     out of users can be very difficult over live chat).
#     """
#
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, related_name="user_visits", on_delete=models.CASCADE
#     )
#     timestamp = models.DateTimeField(
#         help_text="The time at which the first visit of the day was recorded",
#         default=timezone.now,
#     )
#     session_key = models.CharField(help_text="Django session identifier", max_length=40)
#     remote_addr = models.CharField(
#         help_text=(
#             "Client IP address (from X-Forwarded-For HTTP header, "
#             "or REMOTE_ADDR request property)"
#         ),
#         max_length=100,
#         blank=True,
#     )
#     ua_string = models.TextField(
#         "User agent (raw)", help_text="Client User-Agent HTTP header", blank=True,
#     )
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     hash = models.CharField(
#         max_length=32,
#         help_text="MD5 hash generated from request properties",
#         unique=True,
#     )
#     created_at = models.DateTimeField(
#         help_text="The time at which the database record was created (!=timestamp)",
#         auto_now_add=True,
#     )
#
#     objects = UserVisitManager()
#
#     class Meta:
#         get_latest_by = "timestamp"
#
#     def __str__(self) -> str:
#         return f"{self.user} visited the site on {self.timestamp}"
#
#     def __repr__(self) -> str:
#         return f"<UserVisit id={self.id} user_id={self.user_id} date='{self.date}'>"
#
#     def save(self, *args: Any, **kwargs: Any) -> None:
#         """Set hash property and save object."""
#         self.hash = self.md5().hexdigest()
#         super().save(*args, **kwargs)
#
#     @property
#     def user_agent(self):# -> user_agents.parsers.UserAgent:
#         """Return UserAgent object from the raw user_agent string."""
#         return user_agents.parsers.parse(self.ua_string)
#
#     @property
#     def date(self) -> datetime.date:
#         """Extract the date of the visit from the timestamp."""
#         return self.timestamp.date()
#
#     # see https://github.com/python/typeshed/issues/2928 re. return type
#     def md5(self):# -> hashlib._Hash:
#         """Generate MD5 hash used to identify duplicate visits."""
#         h = hashlib.md5(str(self.user.id).encode())  # noqa: S303
#         h.update(self.date.isoformat().encode())
#         h.update(self.session_key.encode())
#         h.update(self.remote_addr.encode())
#         h.update(self.ua_string.encode())
#         return h
