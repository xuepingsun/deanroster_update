from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from django.db import models
from django.forms import TextInput, Textarea,CheckboxSelectMultiple
from django.contrib.contenttypes.models import ContentType
from django.forms import  NumberInput, URLInput, Select, DateInput

from django import forms

from django.utils.html import format_html

# from .utils import get_completeness_percentage

# Register your models here.
from .models import (XiInstitute,SchoolInfo #,SchoolCategory,
                    ,DepartmentInfo,DeanBasic,
                    SchoolSiteMapName,
                     DeanID,DeanCV,Deanedu)#,UserVisit #Post,UserInput,
from .forms import DeanBasicForm
from .reference_list import university_pilot_list
# from .models import DeanInfo


current_university_names=[uni[1] for uni in university_pilot_list]

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

    class Meta:
        # help_text='如果该院长在此数据库中的学者ID有一个以上，请逐个填写\n 该院长在此数据库中的第一篇发表时间(包含硕士以上论文)'
        help_texts = {
        'auid': '该院长在此数据库中的学者ID。如果有一个以上，请分行填写',
        'auid_firstyear_in_database': '该院长在此数据库中的第一篇发表时间(包含硕士以上论文)',
        }
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


class DeanBasicAdmin(NestedModelAdmin, admin.ModelAdmin):
    # change_list_template = 'admin/roster/deanbasic/change_list.html'  # Replace 'your_app_name' with your actual app name

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "university_school":
            kwargs['queryset'] = SchoolInfo.objects.filter(university__in=current_university_names)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Restrict to a specific school_category, e.g., "Public Universities"
        return queryset.filter(university_school__university__in=current_university_names)


    def cv_count(self, obj):
        """
        Count the number of CV lines related to this DeanBasic instance.
        """
        return DeanCV.objects.filter(dean_info=obj).exclude(
                        job_st_year_mon__isnull=True
                    ).exclude(
                        job_st_year_mon=''
                    ).exclude(
                        job_st_year_mon='0000'
                    ).count()
    cv_count.short_description = 'valid CV records'

    def edu_count(self, obj):
        """
        Count the number of education lines related to this DeanBasic instance.
        """
        return Deanedu.objects.filter(dean_info=obj, edu_degree='phd').count()
    edu_count.short_description = 'has phd records'

    list_display = ('university_school', 'full_name', 'tenure_period','cv_count','edu_count')

    inlines = [DeanIDInline, DeanCVInline, DeaneduInline]
    form = DeanBasicForm

    def full_name(self, obj):
        return f"{obj.name_last} {obj.name_first}"
    full_name.short_description = 'Dean Name'

    def tenure_period(self, obj):
        return f"{obj.st_year_mon} - {obj.end_year_mon}"
    tenure_period.short_description = 'Tenure Period'




class DepartmentInfoInline(NestedTabularInline):
    model = DepartmentInfo
#     extra=1
    def get_extra(self, request, obj=None, **kwargs):
        # if the parent object already exists, don't show any extra rows
        if obj:
            return 0
        # otherwise, show one extra row
        return 1

class SchoolSiteMapNameInline(NestedTabularInline):
    model = SchoolSiteMapName
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
          'school_category': admin.widgets.FilteredSelectMultiple('学科大类', is_stacked=False),
             }
    def num_deans(self, obj):
        return obj.deanbasic_set.count()
    num_deans.short_description = 'Number of Deans'

    def dean_info_progress(self, obj):
        """
        Display a progress bar showing which years (2000–2024) have dean data.
        """
        # Query DeanBasic records associated with the current SchoolInfo object
        dean_records = DeanBasic.objects.filter(university_school=obj)

        # Initialize a set to track all years with data
        years_with_data = set()

        # Loop through dean records to calculate years covered
        for record in dean_records:
            try:
                start_year = int(record.st_year_mon[:4]) if record.st_year_mon != '0000' else 2025
                 # Extract the year part
                end_year = int(record.end_year_mon[:4]) if record.end_year_mon != '0000' else 2024
                years_with_data.update(range(start_year, end_year + 1))
            except ValueError:
                continue  # Skip if data is invalid

        # Generate progress bar for years 2000–2024
        progress_bar = '<div style="display: flex; gap: 2px; align-items: center;">'
        for year in range(2000, 2025):
            if year in years_with_data:
                progress_bar += (
                    f'<div title="{year}" style="width: 4%; background-color: green; height: 20px; border: 1px solid black;"></div>'
                )
            else:
                progress_bar += (
                    f'<div title="{year}" style="width: 4%; background-color: lightgray; height: 20px; border: 1px solid black;"></div>'
                )
        progress_bar += '</div>'

        return format_html(progress_bar)

    dean_info_progress.short_description = 'Dean Info Coverage'


    # filter_horizontal = ('school_category',)
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Restrict to a specific school_category, e.g., "Public Universities"
        current_university_names=[uni[1] for uni in university_pilot_list]
        return queryset.filter(university__in=current_university_names)

    list_display = ('university', 'school', 'num_deans','dean_info_progress')
    search_fields = ('university', 'school', 'school_en')

    inlines = [DepartmentInfoInline,SchoolSiteMapNameInline] #,DeanBasicInLine

    # list_display = ['university','school', 'num_deans']#'university_school',
    def save_model(self, request, obj, form, change):
        print(f"Cleaned data: {form.cleaned_data.get('school_category')}")  # Log the categories
        super().save_model(request, obj, form, change)




admin.site.register(SchoolInfo,SchoolInfoAdmin)
# admin.site.register(SchoolCategory)
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


    # def data_completeness(self, obj):
    #     percentage = get_completeness_percentage()
    #     return format_html(
    #         '<div style="width: 100px; background: #e0e0e0;">'
    #         '<div style="width: {}%; background: #76ce60;">&nbsp;</div>'
    #         '</div>'
    #         '<span>{}% Complete</span>',
    #         percentage, percentage
    #     )
    # data_completeness.short_description = 'Data Completeness'
