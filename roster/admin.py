from django.contrib import admin

# Register your models here.
from .models import Post,UserInput

admin.site.register(Post)
admin.site.register(UserInput)
