from django.urls import path

from .views import *


urlpatterns = [
	path('', DashboardView.as_view(), name='index'),
	path('match/', get_match, name='match')
]