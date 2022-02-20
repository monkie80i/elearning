from django.contrib import admin
from .models import User,Profile

# Register your models here.
class EducaAdminSite(admin.AdminSite):
	site_header = 'Ecom Admin Interface'
	site_title = 'Ecom Administration'
	index_title = 'Ecom Administration'
	site_url = None

admin_site = EducaAdminSite(name="EducaAdmin")

admin_site.register(User)
admin_site.register(Profile)
