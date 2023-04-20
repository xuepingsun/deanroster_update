from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from django.db import models
from django.forms import TextInput, Textarea


# Register your models here.
from .models import XiInstitute,DeanBasic, DeanID,DeanCV,Deanedu#,UserVisit #Post,UserInput,
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

class DeanBasicAdmin(NestedModelAdmin):
    # fieldsets = (
    #     (("Basic Info"), {'fields': ("user", "website")}),
    #     (("Phones"), {'fields': (
    #         (("Primary"), {'fields': (("primary_phone_country", "primary_phone_area", "primary_phone_number"),)}),
    #         (("Secondary"), {'fields': (("secondary_phone_country", "secondary_phone_area", "secondary_phone_number"),)}),
    #         )}),
    #     )
    inlines = [DeanIDInline,DeanCVInline,DeaneduInline]

# @admin.site.register(DeanBasicAdmin)
# class AllModelAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.CharField: {'widget': TextInput(attrs={'size':'20'})},
#         models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
#     }


admin.site.register(DeanBasic,DeanBasicAdmin)
admin.site.register(XiInstitute)
