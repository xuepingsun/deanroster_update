from django.urls import path

from . import views
from .views import school_completeness_view

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('', views.admin_index, name='admin_index'),
# ]
urlpatterns = [
    path('', school_completeness_view, name='school-completeness'),
]
