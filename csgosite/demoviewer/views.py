from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

class DashboardView(TemplateView):
	template_name = 'demoviewer/index.html'