from django.contrib import admin
from .models import Question, Choice

# Register your models here.
admin.site.site_header = "Poll Admin"
admin.site.site_title = "Poll Admin Area"
admin.site.index_header = "Welcome to the Poll Admin Area"

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3 

class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [(None, {'fields': ['question_text']}),]
	inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)

