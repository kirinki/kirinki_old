from rstr.models import *
from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('user', {'fields': ['username',  'name',  'surname'], 'classes': ['collapse']})
        ]
    #    (None,               {'fields': ['question']}),
    #    ('Date information', {'fields': ['pub_date']}),
    #    ]

admin.site.register(usr,UserAdmin)
admin.site.register(usrType)
admin.site.register(video)
admin.site.register(configs)
