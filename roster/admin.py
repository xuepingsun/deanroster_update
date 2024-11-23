from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from django.db import models
from django.forms import TextInput, Textarea,CheckboxSelectMultiple
from django.contrib.contenttypes.models import ContentType
from django.forms import  NumberInput, URLInput, Select, DateInput

from django import forms

from django.utils.html import format_html
from .utils import get_completeness_percentage

# Register your models here.
from .models import XiInstitute,SchoolInfo,SchoolCategory, DepartmentInfo,DeanBasic, DeanID,DeanCV,Deanedu#,UserVisit #Post,UserInput,
from .forms import DeanBasicForm
# from .models import DeanInfo

# admin.site.register(Post)
# admin.site.register(UserInput)
class DeanIDInlineForm(forms.ModelForm):
    class Meta:
        model = DeanID
        fields = '__all__'
        widgets = {
            'database': Select(attrs={'style': 'width: 120px;'}),
            'auid': TextInput(attrs={'size': '15'}),
            'auid_firstyear_in_database': TextInput(attrs={'size': '5'}),
            'author_profile_url': URLInput(attrs={'size': '30'}),
            'h_index_till_2022': NumberInput(attrs={'style': 'width: 60px;'}),
        }

class DeanIDInline(NestedTabularInline):
#     extra=2
    model = DeanID
    form = DeanIDInlineForm

#     help_texts = {
#     'auid': '该院长在此数据库中的学者ID。如果有一个以上，请分行填写',
#     'auid_firstyear_in_database': '该院长在此数据库中的第一篇发表时间(包含硕士以上论文)',
# }
    # class Meta:
    #     # help_text='如果该院长在此数据库中的学者ID有一个以上，请逐个填写\n 该院长在此数据库中的第一篇发表时间(包含硕士以上论文)'
    #     help_texts = {
    #     'auid': '该院长在此数据库中的学者ID。如果有一个以上，请分行填写',
    #     'auid_firstyear_in_database': '该院长在此数据库中的第一篇发表时间(包含硕士以上论文)',
    #     }
    def get_extra(self, request, obj=None, **kwargs):
        # if the parent object already exists, don't show any extra rows
        if obj:
            return 0
        # otherwise, show one extra row
        return 2
    verbose_name = "出版数据库ID"
    verbose_name_plural = "出版数据库ID"
    fields = (
        'database',
        'auid',
        'auid_firstyear_in_database',
        'author_profile_url',
        'h_index_till_2022',
    )


class DeanCVInlineForm(forms.ModelForm):
    class Meta:
        model = DeanCV
        fields = '__all__'
        widgets = {
            'job_st_year_mon': TextInput(attrs={'size': '10'}),
            'job_end_year_mon': TextInput(attrs={'size': '10'}),
            'job_title': TextInput(attrs={'size': '30'}),
            'job_title_level': Select(attrs={'style': 'width: 120px;'}),
            'job_country': TextInput(attrs={'size': '10'}),
            'job_institution': TextInput(attrs={'size': '30'}),
            'job_location_category': Select(attrs={'style': 'width: 120px;'}),
        }

class DeanCVInline(NestedTabularInline):
    model = DeanCV
    form = DeanCVInlineForm
#     extra=1
    # inlines = [ContractSubClauseInline]
    def get_extra(self, request, obj=None, **kwargs):
        # if the parent object already exists, don't show any extra rows
        if obj:
            return 0
        # otherwise, show one extra row
        return 1
    verbose_name = "工作履历"
    verbose_name_plural = "工作履历"
    fields = (
        'job_st_year_mon',
        'job_end_year_mon',
        'job_title',
        'job_title_level',
        'job_country',
        'job_institution',
        'job_location_category',
    )

class DeaneduInlineForm(forms.ModelForm):
    class Meta:
        model = Deanedu
        fields = '__all__'
        widgets = {
            'edu_degree_year_mon': TextInput(attrs={'size': '10'}),
            'edu_degree': Select(attrs={'style': 'width: 80px;'}),
            'edu_country': TextInput(attrs={'size': '10'}),
            'edu_institution': TextInput(attrs={'size': '30'}),
            'edu_location_category': Select(attrs={'style': 'width: 120px;'}),
        }

class DeaneduInline(NestedTabularInline):
    model = Deanedu
    form = DeaneduInlineForm
#     extra=1
    def get_extra(self, request, obj=None, **kwargs):
        # if the parent object already exists, don't show any extra rows
        if obj:
            return 0
        # otherwise, show one extra row
        return 1
    verbose_name = "高等教育背景"
    verbose_name_plural = "高等教育背景"
    fields = (
        'edu_degree_year_mon',
        'edu_degree',
        'edu_country',
        'edu_institution',
        'edu_location_category',
    )

# class DeanBasicAdmin(NestedModelAdmin,admin.ModelAdmin):
#     def formfield_for_foreignkey(self,db_field,request,**kwargs):
#         if db_field.name=="university_school":
#             kwargs['queryset']=SchoolInfo.objects.all()
#         return super().formfield_for_foreignkey(db_field,request,**kwargs)
#     # fieldsets = (
#     #     (("Basic Info"), {'fields': ("user", "website")}),
#     #     (("Phones"), {'fields': (
#     #         (("Primary"), {'fields': (("primary_phone_country", "primary_phone_area", "primary_phone_number"),)}),
#     #         (("Secondary"), {'fields': (("secondary_phone_country", "secondary_phone_area", "secondary_phone_number"),)}),
#     #         )}),
#     #     )
#
#
#     inlines = [DeanIDInline,DeanCVInline,DeaneduInline]
#     form=DeanBasicForm
    # change_form_template='admin/deanbasic_university_school_form.html'

# @admin.site.register(DeanBasicAdmin)
# class AllModelAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.CharField: {'widget': TextInput(attrs={'size':'20'})},
#         models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
#     }


# admin.py

class DeanBasicAdmin(NestedModelAdmin, admin.ModelAdmin):
    change_list_template = 'admin/roster/deanbasic/change_list.html'  # Replace 'your_app_name' with your actual app name

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "university_school":
            kwargs['queryset'] = SchoolInfo.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ('university_school', 'full_name', 'tenure_period')

    inlines = [DeanIDInline, DeanCVInline, DeaneduInline]
    form = DeanBasicForm

    def full_name(self, obj):
        return f"{obj.name_last} {obj.name_first}"
    full_name.short_description = 'Dean Name'

    def tenure_period(self, obj):
        return f"{obj.st_year_mon} - {obj.end_year_mon}"
    tenure_period.short_description = 'Tenure Period'

# admin.site.register(DeanBasic, DeanBasicAdmin)



class DepartmentInfoInline(NestedTabularInline):
    model = DepartmentInfo
#     extra=1
    def get_extra(self, request, obj=None, **kwargs):
        # if the parent object already exists, don't show any extra rows
        if obj:
            return 0
        # otherwise, show one extra row
        return 1


class DeanBasicInLine(admin.TabularInline):
    model = DeanBasic
    extra = 1

class SchoolInfoAdmin(NestedModelAdmin,admin.ModelAdmin):
    class Meta:
        model = SchoolInfo
        fields = '__all__'
        widgets = {
            'school_category': CheckboxSelectMultiple(),
        }

    list_display = ('university', 'school', 'school_en')
    search_fields = ('university', 'school', 'school_en')
    # filter_horizontal = ('school_category',)

    inlines = [DepartmentInfoInline] #,DeanBasicInLine

    # list_display = ['university','school', 'num_deans']#'university_school',
    #
    def num_deans(self, obj):
        return obj.deanbasic_set.count()
    num_deans.short_description = 'Number of Deans'
    #
    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.annotate(num_deans=models.Count('deanbasic'))
    #     return queryset
    # def num_deans_display(self, obj):
    #     return obj.num_deans
    # num_deans_display.short_description = 'Number of deans'
    #


# admin.py
# from django.contrib import admin
# from django.contrib.contenttypes.models import ContentType
# from django.db import models
# from django.template.response import TemplateResponse

# from .models import SchoolInfo, DeanBasic


# class SchoolInfoAdmin(admin.ModelAdmin):
#     list_display = ('name', 'num_deans')
#     ordering = ('name',)
#
#     def num_deans(self, obj):
#         return obj.deanbasic_set.count()
#
#     num_deans.short_description = 'Number of Deans'
# def get_model_info(model):
#     content_type = ContentType.objects.get_for_model(model)
#     app_label = content_type.app_label
#     model_name = content_type.model
#     return app_label, model_name
#
#
# class SchoolInfoDashboard(admin.AdminSite):
#     site_header = f"{get_model_info(SchoolInfo)[1].title()} Administration"
#     site_title = f"{get_model_info(SchoolInfo)[1].title()} Admin Portal"
#     index_title = f"{get_model_info(SchoolInfo)[1].title()} Dashboard"
#     index_template = 'admin/admin_index.html'
#
#     def get_urls(self):
#         from django.urls import path
#         urls = super().get_urls()
#         urls += [
#             path('', self.admin_view(self.dashboard_view), name='index'),
#         ]
#         return urls
#
#     def dashboard_view(self, request):
#         schools = SchoolInfo.objects.annotate(num_deans=models.Count('deanbasic'))
#         context = {
#             'schools': schools,
#         }
#         return TemplateResponse(request, self.index_template, context)
#
#
# admin_site = SchoolInfoDashboard(name='schoolinfoadmin')


admin.site.register(SchoolInfo,SchoolInfoAdmin)
admin.site.register(SchoolCategory)
admin.site.register(DeanBasic,DeanBasicAdmin)
admin.site.register(XiInstitute)

admin.site.index_template = 'admin/admin_index.html'
def get_schools_with_dean_counts():
    schools = SchoolInfo.objects.annotate(num_deans=models.Count('deanbasic'))
    return schools

def get_model_info(model):
    content_type = ContentType.objects.get_for_model(model)
    app_label = content_type.app_label
    model_name = content_type.model
    return app_label, model_name
#
@admin.display(description='Number of Deans')
def num_deans(self, obj):
    return obj.num_deans
#
admin.site.site_header = f"{get_model_info(SchoolInfo)[1].title()} Administration"
admin.site.site_title = f"{get_model_info(SchoolInfo)[1].title()} Admin Portal"
admin.site.index_title = f"{get_model_info(SchoolInfo)[1].title()} Dashboard"
admin.site.schools = get_schools_with_dean_counts()
