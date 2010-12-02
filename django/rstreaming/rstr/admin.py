# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

from rstr.models import *
from django.contrib import admin

# class UserAdmin(admin.ModelAdmin):
    # fieldsets = [
        # ('user', {'fields': ['username',  'name',  'surname'], 'classes': ['collapse']})
        # ]
    #    (None,               {'fields': ['question']}),
    #    ('Date information', {'fields': ['pub_date']}),
    #    ]

# admin.site.register(usr,UserAdmin)
# admin.site.register(usrType)
admin.site.register(configs)
admin.site.register(video)
