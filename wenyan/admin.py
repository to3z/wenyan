from django.contrib import admin

# Register your models here.
from .models import Word,Explanation,Example,Sentence,Tongjia,Appear,Chuchu

admin.site.register(Word)
admin.site.register(Explanation)
admin.site.register(Example)
admin.site.register(Sentence)
admin.site.register(Tongjia)
admin.site.register(Appear)
admin.site.register(Chuchu)