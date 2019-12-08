from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import *

class GeneralAdmin(admin.ModelAdmin):
    pass 

admin.site.register(Article, GeneralAdmin)
admin.site.register(Tag, GeneralAdmin)
admin.site.register(Benchmark, GeneralAdmin)
admin.site.register(Comment, GeneralAdmin)
admin.site.register(Library, GeneralAdmin)