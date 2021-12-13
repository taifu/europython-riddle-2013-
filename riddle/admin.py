# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Answer

class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'is_right',
        'level',
        'timestamp',
        'email',
        'answer',
        'ip',
        'attempts',
    )
    list_filter = ['is_right', 'level']
    #ordering = ['-level', 'timestamp', 'attempts']
    ordering = ['-timestamp']
    search_fields = ['ip', 'email']
    readonly_fields = tuple(list_display) + ('notes',)

admin.site.register(Answer, AnswerAdmin)
