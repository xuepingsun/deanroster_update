from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from django.db import models
from django.forms import TextInput, Textarea
from django.contrib.contenttypes.models import ContentType



# Register your models here.
from .models import XiInstitute,SchoolInfo, DepartmentInfo,DeanBasic, DeanID,DeanCV,Deanedu#,UserVisit #Post,UserInput,
from .forms import DeanBasicForm
# from .models import DeanInfo

# admin.site.register(Post)
# admin.site.register(UserInput)
class DeanIDInline(NestedTabularInline):
    model = DeanID

class DeanCVInline(NestedTabularInline):
    model = DeanCV
    # inlines = [ContractSubClauseInline]

class DeaneduInline(NestedTabularInline):
    model = Deanedu

class DeanBasicAdmin(NestedModelAdmin,admin.ModelAdmin):
    def formfield_for_foreignkey(self,db_field,request,**kwargs):
        if db_field.name=="university_school":
            kwargs['queryset']=SchoolInfo.objects.all()
        return super().formfield_for_foreignkey(db_field,request,**kwargs)
    # fieldsets = (
    #     (("Basic Info"), {'fields': ("user", "website")}),
    #     (("Phones"), {'fields': (
    #         (("Primary"), {'fields': (("primary_phone_country", "primary_phone_area", "primary_phone_number"),)}),
    #         (("Secondary"), {'fields': (("secondary_phone_country", "secondary_phone_area", "secondary_phone_number"),)}),
    #         )}),
    #     )


    inlines = [DeanIDInline,DeanCVInline,DeaneduInline]
    form=DeanBasicForm
    # change_form_template='admin/deanbasic_university_school_form.html'

# @admin.site.register(DeanBasicAdmin)
# class AllModelAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.CharField: {'widget': TextInput(attrs={'size':'20'})},
#         models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
#     }



class DepartmentInfoInline(NestedTabularInline):
    model = DepartmentInfo


class DeanBasicInLine(admin.TabularInline):
    model = DeanBasic
    extra = 0

class SchoolInfoAdmin(NestedModelAdmin,admin.ModelAdmin):
    inlines = [DepartmentInfoInline] #,DeanBasicInLine

    # list_display = ['university','school', 'num_deans']#'university_school',
    #
    # def num_deans(self, obj):
    #     return obj.deanbasic_set.count()
    # num_deans.short_description = 'Number of Deans'
    #
    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.annotate(num_deans=models.Count('deanbasic'))
    #     return queryset
    # def num_deans_display(self, obj):
    #     return obj.num_deans
    # num_deans_display.short_description = 'Number of deans'
    #





admin.site.register(SchoolInfo,SchoolInfoAdmin)
admin.site.register(DeanBasic,DeanBasicAdmin)
admin.site.register(XiInstitute)

admin.site.index_template = 'admin_index.html'
def get_schools_with_dean_counts():
    schools = SchoolInfo.objects.annotate(num_deans=models.Count('deanbasic'))
    return schools

def get_model_info(model):
    content_type = ContentType.objects.get_for_model(model)
    app_label = content_type.app_label
    model_name = content_type.model
    return app_label, model_name

@admin.display(description='Number of Deans')
def num_deans(self, obj):
    return obj.num_deans

admin.site.site_header = f"{get_model_info(SchoolInfo)[1].title()} Administration"
admin.site.site_title = f"{get_model_info(SchoolInfo)[1].title()} Admin Portal"
admin.site.index_title = f"{get_model_info(SchoolInfo)[1].title()} Dashboard"
admin.site.schools = get_schools_with_dean_counts()
