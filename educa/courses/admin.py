from pyexpat import model
from xml.etree.ElementInclude import include
from django.contrib import admin
from .models import Content, Subject,Course,Module,Image,Text,Video,File
from adminManager.admin import admin_site
# Register your models here.

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id','title']
    prepopulated_fields = {'slug':('title',)}

class ModuleInline(admin.StackedInline):
    model = Module

class CousrseAdmin(admin.ModelAdmin):
    list_display = ['title','subject','created']
    list_filter = ['created','subject']
    search_fields = ['title','overview']
    prepopulated_fields = {'slug':('title',)}
    inlines = [ModuleInline]

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['id','title','created']

admin_site.register(Subject,SubjectAdmin)
admin_site.register(Course,CousrseAdmin)
admin_site.register(Module,ModuleAdmin)
admin_site.register(Content)
admin_site.register(Image)
admin_site.register(Text)
admin_site.register(Video)
admin_site.register(File)

