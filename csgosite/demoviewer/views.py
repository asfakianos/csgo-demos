from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

import json
import random

class DashboardView(TemplateView):
	template_name = 'demoviewer/index.html'


def get_match(request):
	random.seed()

	data = {
		"round 1": {
			"kills": [{"x": random.randrange(100), "y": random.randrange(100)} for _ in range(5)],
			"deaths": [{"x": random.randrange(100), "y": random.randrange(100)} for _ in range(4)],
		},
		"round 2": {
			"kills": [{"x": random.randrange(100), "y": random.randrange(100)} for _ in range(5)],
			"deaths": [{"x": random.randrange(100), "y": random.randrange(100)} for _ in range(4)],
		}
	}

	return JsonResponse(data)