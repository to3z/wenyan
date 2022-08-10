from django.contrib import admin

# Register your models here.
from .models import Word,Explanation,Sentence,Tongjia,Appear

admin.site.register(Word)
admin.site.register(Explanation)
admin.site.register(Sentence)
admin.site.register(Tongjia)
admin.site.register(Appear)