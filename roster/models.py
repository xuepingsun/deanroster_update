from django.db import models
# import django.utils.timezone as timezone
from django.core.validators import RegexValidator,MinLengthValidator
from django.conf import settings
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _lazy

from django.forms import Textarea

import datetime
import hashlib
import uuid
from typing import Any
from .reference_list import university_pilot_list


class XiInstitute(models.Model):
    university_choice=university_pilot_list
    university = models.CharField(max_length=50,choices=university_choice,default='na',verbose_name="大学名称")
    institute_name=models.CharField(max_length=30,verbose_name="机构名称")
    found_year_mon=models.CharField(max_length=30,verbose_name="机构创始年月")
    institute_type=models.CharField(max_length=8,choices=[("center","中心/研究所"),("college","学院")],verbose_name="机构级别")
    class Meta:
        app_label = 'roster'
        #constrain duplicates
        unique_together = (("university", "institute_name"),)
        
        verbose_name = "校级马列学院与习近平思想研究院所"
        verbose_name_plural = "校级马列学院与习近平思想研究院所"

    def __str__(self):
        return '-'.join([self.university,self.institute_name])


class SchoolInfo(models.Model):
    """
    reminder here: english name from the official website, not chinese translation
    """
    university_choice=university_pilot_list
    university = models.CharField(max_length=50,choices=university_choice,default='na',verbose_name="大学名称")
    # university_en= models.CharField(max_length=50,default='na')

    #university category: 985, 211, 985&211,
    university_cls_choice=[('985','985'),
                           ('211','211'),
                           ('985&211','985&211'),
                           ('none','none')]
    university_category = models.CharField(max_length=7,choices=university_cls_choice,default='na',verbose_name="大学985/211类别")


    school = models.CharField(max_length=50,default='na',verbose_name="学院名称")
    school_en= models.CharField(max_length=50,default='na',verbose_name="学院英文名")
    school_st_year=  models.CharField(max_length=4,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[0-9]{4}$',
                message='Only xxxx are allowed.'
            )
        ],
        default='0000',verbose_name="学院创始年份")

    school_cls_choice=[
                    ('life','生命科学'),
                    ('chem','化学'),
                    ('phys','物理'),
                    ('macs','数学与计算科学'),
                    ('econ','经济'),
                    ('soci','社会学'),
                    ('pol','政府管理与政治学'),
                    # ('gov','govmanagement')
                    ('law','法学')
                    ]
    school_category = models.CharField(max_length=4,choices=school_cls_choice,default='na',verbose_name="学科大类")

    class Meta:
        app_label = 'roster'
        #constrain duplicates
        # unique_together = (("university", "school"),)
        constraints=[
            models.UniqueConstraint(fields=['university','school'],
                                    name='university_school')
        ]
        
        verbose_name = "院系名单"
        verbose_name_plural = "院系名单"


    def __str__(self):
        return '-'.join([self.university,self.school])


class DepartmentInfo(models.Model):
    school_info = models.ForeignKey(SchoolInfo, on_delete=models.DO_NOTHING)

    #---------------------scopus info ----------------
    department_name=models.CharField(max_length=30,verbose_name="系/所名称")
    department_name_en=models.CharField(max_length=30,verbose_name="系/所名称英文")


    class Meta:
        app_label = 'roster'



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

    university_school= models.ForeignKey(SchoolInfo,on_delete=models.DO_NOTHING)#models.CharField(max_length=50,default='na')
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
    name_first = models.CharField(max_length=20, #help_text="输入名"
            verbose_name="姓"
                                )
    name_last = models.CharField(max_length=20,
            verbose_name="名"
            # help_text="输入姓"
            )

    gender_choice=[('female','女'),
                   ('male','男')]
    gender = models.CharField(max_length=6,choices=gender_choice,
            verbose_name="性别")
    is_name_common= models.CharField(max_length=20,choices=[("1","是"),("0","否")],verbose_name="是否为常见名") #true or false
    
    
    birth_year_mon = models.CharField(max_length=7,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[0-9]{4}(\-[0-9]{2}){0,1}$',
                message='Only xxxx or xxxx-xx are allowed.'
            )
        ],
        verbose_name="出生年月",
        default='0000') #models.CharField(max_length=50)
    

    # st_year_mon=models.DateTimeField(input_formats=['%Y', '%Y-%m'],help_text="任职开始年月")
    st_year_mon = models.CharField(max_length=7,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[0-9]{4}(\-[0-9]{2}){0,1}$',
                message='Only xxxx or xxxx-xx are allowed.'
            )
        ],
        verbose_name="任职开始年月",
        default='0000') #models.CharField(max_length=50)
    end_year_mon =  models.CharField(max_length=7,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[0-9]{4}(\-[0-9]{2}){0,1}$',
                message='Only xxxx or xxxx-xx are allowed.'
            )
        ],verbose_name="任职结束年月",
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
    edu_background_url= models.URLField(verbose_name="教育背景信息的网页链接")
    # CV_string = models.TextField()
    CV_string_url= models.URLField(verbose_name="履历信息的网页链接")


    class Meta:
        app_label = 'roster'
        #constrain duplicates
        # unique_together = (("university_school","name_last","name_first"),)
        constraints=[
            models.UniqueConstraint(
            fields=["university_school","name_last","name_first"], #,"st_year_mon"
            name='university_school_name_st_year_mon')
        ]
        
        
        verbose_name = "院长信息"
        verbose_name_plural = "院长信息"


    def __str__(self):
        return '-'.join([self.university_school.university,self.university_school.school,
            self.name_last,self.name_first])+":["+self.st_year_mon+','+self.end_year_mon+']'

class DeanID(models.Model):
    dean_info = models.ForeignKey(DeanBasic, on_delete=models.DO_NOTHING)

    #---------------------scopus info ----------------
    database=models.CharField(max_length=10,choices=[("scopus","scopus"),
                                                        #("CNKI","CNKI"),
                                                        ("wanfang","wanfang"),
                                                        # ("OCRID","OCRID")
                                                        ],verbose_name="学术发表数据库名称",
                                                        help_text="自然科学范畴内不应该缺失scopus ID，社会科学范畴内不应该缺失 wanfang；大部分情况下应该二者兼有")
    auid=models.CharField(max_length=20,verbose_name="学者ID",help_text="该院长在此数据库中的学者ID如果有一个以上，请分行填写") # allow to have multiple or missing at all
    auid_firstyear_in_database= models.CharField(max_length=4,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[0-9]{4}$',
                message='Only xxxx is allowed.'
            )
        ],
        default='0000',verbose_name="该院长在此数据库中的第一篇发表时间(包含硕士以上论文)")
    author_profile_url=models.URLField(verbose_name="该院长在此数据库中的学者页面链接")
    h_index_till_2022=models.IntegerField(max_length=20,default=-99,verbose_name="该院长在此数据库中的截止目前的h-index")


    class Meta:
        app_label = 'roster'
        verbose_name = "出版数据库ID"
        verbose_name_plural = "出版数据库ID"

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
        ],verbose_name="该职位的开始年份(xxxx)或者年月(xxxx-xx)",
        default='0000') #models.CharField(max_length=50)
    job_end_year_mon =  models.CharField(max_length=7,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[0-9]{4}(\-[0-9]{2}){0,1}$',
                message='Only xxxx or xxxx-xx are allowed.'
            )
        ],verbose_name="该职位的结束年份(xxxx)或者年月(xxxx-xx)",
        default='0000') #models.CharField(max_length=50)
    # job_content= models.TextField()

    job_title= models.CharField(max_length=100,verbose_name="该职位的具体名称")
    job_title_level= models.CharField(max_length=20,
            choices=[("dean","院长"),("vice-dean","副院长"),
                    ("prof","教授"),("associate-prof","副教授")
                    ,("assistant-prof","助理教授/讲师")
                    ,("postdoc","博士后")
                    ,("other","其它")],
                    default='other',verbose_name="职位级别")
    job_country= models.CharField(max_length=10,verbose_name="该职位所在地区与国家")
    job_institution=models.CharField(max_length=20,verbose_name="任职单位(具体到大学-学院或者研究所-实验室)")
    job_location_category=models.CharField(max_length=10,
            choices=[("within-uni","本校"),("within","本院"),("china","国内其他院所"),
                    ("oversea","海外")],
                    default='other',verbose_name="任职单位类型(不能确定的情况下选择other)")


    class Meta:
        app_label = 'roster'
        
        verbose_name = "工作履历"
        verbose_name_plural = "工作履历"

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
        default='0000',verbose_name="该教育经历的开始年份(xxxx)或者年月(xxxx-xx)") #models.CharField(max_length=50)
    edu_end_year_mon =  models.CharField(max_length=7,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[0-9]{4}(\-[0-9]{2}){0,1}$',
                message='Only xxxx or xxxx-xx are allowed.'
            )
        ],
        default='0000',verbose_name="该教育经历的结束年份(xxxx)或者年月(xxxx-xx)") #models.CharField(max_length=50)
    edu_degree=  models.CharField(max_length=10,choices=[("phd","博士"),("ma","硕士"),("ba","学士")],verbose_name="学位")
    # edu_location= models.CharField(max_length=20)
    edu_country= models.CharField(max_length=10,verbose_name="学位授予国家或地区")
    edu_institution=models.CharField(max_length=20,verbose_name="学位授予机构(具体到大学-学院或者研究所)")
    edu_location_category=models.CharField(max_length=10,
            choices=[("within-uni","本校"),("within","本院"),("china","国内其他院所"),
                    ("oversea","海外")],
                    default='other',verbose_name="学位授予单位类型(不能确定的情况下选择other)")

    class Meta:
        app_label = 'roster'
        verbose_name = "高等教育背景"
        verbose_name_plural = "高等教育背景"

    # def __str__(self):
    #     return '-'.join([self.university,self.school,self.name_last,self.name_first])+":["+self.st_year_mon+','+self.end_year_mon+']'
