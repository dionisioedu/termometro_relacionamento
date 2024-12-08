from django.contrib import admin

from django.contrib import admin
from .models import Question, Answer, AnswerOption

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(AnswerOption)
