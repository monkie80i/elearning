from re import template
from .models import Course
from django.views.generic.list import ListView

# Create your views here.
class ManageCourseListView(ListView):
    model = Course
    template = 'courses/manage/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)