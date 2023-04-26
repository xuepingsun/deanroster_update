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


class XiInstitute(models.Model):
    university_choice=university_pilot_list
    university = models.CharField(max_length=50,choices=university_choice,default='na')
    institute_name=models.CharField(max_length=30)
    found_year_mon=models.CharField(max_length=30)
    institute_type=models.CharField(max_length=8,choices=[("center","中心"),("college","学院")])
    class Meta:
        app_label = 'roster'
        #constrain duplicates
        unique_together = (("university", "institute_name"),)

    def __str__(self):
        return '-'.join([self.university,self.institute_name])


class SchoolInfo(models.Model):
    """
    reminder here: english name from the official website, not chinese translation
    """
    university_choice=university_pilot_list
    university = models.CharField(max_length=50,choices=university_choice,default='na')
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

    class Meta:
        app_label = 'roster'
        #constrain duplicates
        # unique_together = (("university", "school"),)
        constraints=[
            models.UniqueConstraint(fields=['university','school'],
                                    name='university_school')
        ]


    def __str__(self):
        return '-'.join([self.university,self.school])




class DeanBasic(models.Model):
    """
    have chinese translation for all the variable names
    perhaps also add a clickable info button to check the definition of the variable
    """
    #---------------------Institution info ----------------
    """ do not allow for missing in any of these fields"""
    # university_choice=university_pilot_list
    # university = models.CharField(max_length=50,choices=university_choice,default='na')

    # """
    # reminder here: english name from the official website, not chinese translation
    # """
    # university_en= models.CharField(max_length=50,default='na')
    #
    # #university category: 985, 211, 985&211,
    # university_cls_choice=[('985','985'),
    #                        ('211','211'),
    #                        ('985&211','985&211'),
    #                        ('none','none')]
    # university_category = models.CharField(max_length=7,choices=university_cls_choice,default='na')
    #
    #
    # school = models.CharField(max_length=50,default='na')

    university_school= models.CharField(max_length=50,default='na')
    # school_en= models.CharField(max_length=50,default='na')
    #
    # school_cls_choice=[
    #                 ('econ','economics'),
    #                 ('life','life_science'),
    #                 ('chem','chemistry'),
    #                 ('phys','physics'),
    #                 ('macs','math&computer_science'),
    #                 ('soci','sociology'),
    #                 ('pol','poliscience'),
    #                 ('gov','govmanagement')]
    # school_category = models.CharField(max_length=4,choices=school_cls_choice,default='na')
    #

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

    # #---------------------graduation---------------
    # institution_phd_graduation=models.CharField(max_length=20)#allow for missing value
    # country_phd_graduation=models.CharField(max_length=20)#allow for missing value
    # whether_oversea_phd=models.CharField(max_length=3,choices=[("1",'是'),("0",'否')],default='na')
    # year_phd_graduation=models.CharField(max_length=4,
    #         validators=[
    #     MinLengthValidator(4),
    #     RegexValidator(
    #         regex=r'^[0-9]{4}$',
    #         message='Only xxxx are allowed.'
    #     )
    #     ],
    #         default='0000')#allow for missing value
    # year_phd_graduation_info_url=models.URLField() #allow for missing value


    # #---------------------scopus info ----------------
    # scopus_auid=models.CharField(max_length=20) # allow to have multiple or missing at all
    # scopus_auprofile_url=models.URLField()
    # scopus_h_index_till_2022=models.CharField(max_length=20)
    #
    #
    # #---------------------OCRID ----------------
    # OCRID=models.CharField(max_length=20)#allow for missing value
    #
    # #---------------------wanfang ----------------
    # WF_scholar_id=models.CharField(max_length=20)#allow for missing value
    # WF_h_index_till_2022=models.CharField(max_length=20)#allow for missing value

    # #---------------------CV ----------------
    # """do not allow for missing"""
    # edu_background_string = models.TextField()
    edu_background_url= models.URLField()
    # CV_string = models.TextField()
    CV_string_url= models.URLField()


    class Meta:
        app_label = 'roster'
        #constrain duplicates
        # unique_together = (("university_school","name_last","name_first"),)
        constraints=[
            models.UniqueConstraint(fields=["university_school","name_last","name_first","st_year_mon")],
                                    name='university_school_name_st_year_mon')
        ]


    def __str__(self):
        return '-'.join([self.university_school,self.name_last,self.name_first])+":["+self.st_year_mon+','+self.end_year_mon+']'

class DeanID(models.Model):
    dean_info = models.ForeignKey(DeanBasic, on_delete=models.DO_NOTHING)

    #---------------------scopus info ----------------
    database=models.CharField(max_length=10,choices=[("scopus","scopus"),
                                                        #("CNKI","CNKI"),
                                                        ("wanfang","wanfang"),
                                                        # ("OCRID","OCRID")
                                                        ])
    auid=models.CharField(max_length=20) # allow to have multiple or missing at all
    auid_firstyear_in_database= models.CharField(max_length=4,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[0-9]{4}$',
                message='Only xxxx is allowed.'
            )
        ],
        default='0000')
    author_profile_url=models.URLField()
    h_index_till_2022=models.IntegerField(max_length=20,default=-99)


    class Meta:
        app_label = 'roster'


class DeanCV(models.Model):

    # #---------------------CV ----------------
    # """do not allow for missing"""
    dean_info = models.ForeignKey(DeanBasic, on_delete=models.DO_NOTHING)
    job_st_year_mon = models.CharField(max_length=7,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[0-9]{4}(\-[0-9]{2}){0,1}$',
                message='Only xxxx or xxxx-xx are allowed.'
            )
        ],
        default='0000') #models.CharField(max_length=50)
    job_end_year_mon =  models.CharField(max_length=7,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[0-9]{4}(\-[0-9]{2}){0,1}$',
                message='Only xxxx or xxxx-xx are allowed.'
            )
        ],
        default='0000') #models.CharField(max_length=50)
    # job_content= models.TextField()

    job_title= models.CharField(max_length=20)
    job_title_level= models.CharField(max_length=20,
            choices=[("dean","院长"),("vice-dean","副院长"),
                    ("prof","教授"),("associate-prof","副教授")
                    ,("assistant-prof","助理教授/讲师")
                    ,("postdoc","博士后")],
                    default='other')
    job_country= models.CharField(max_length=10)
    job_institution=models.CharField(max_length=20)


    class Meta:
        app_label = 'roster'

class Deanedu(models.Model):

    # #---------------------CV ----------------
    # """do not allow for missing"""
    dean_info = models.ForeignKey(DeanBasic, on_delete=models.DO_NOTHING)
    edu_st_year_mon = models.CharField(max_length=7,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[0-9]{4}(\-[0-9]{2}){0,1}$',
                message='Only xxxx or xxxx-xx are allowed.'
            )
        ],
        default='0000') #models.CharField(max_length=50)
    edu_end_year_mon =  models.CharField(max_length=7,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[0-9]{4}(\-[0-9]{2}){0,1}$',
                message='Only xxxx or xxxx-xx are allowed.'
            )
        ],
        default='0000') #models.CharField(max_length=50)
    edu_degree=  models.CharField(max_length=10,choices=[("phd","博士"),("ma","硕士"),("ba","学士")])
    # edu_location= models.CharField(max_length=20)
    edu_country= models.CharField(max_length=10)
    edu_institution=models.CharField(max_length=20)

    class Meta:
        app_label = 'roster'

    # def __str__(self):
    #     return '-'.join([self.university,self.school,self.name_last,self.name_first])+":["+self.st_year_mon+','+self.end_year_mon+']'
