from django.shortcuts import render
from wenyan.models import Word,Explanation,Sentence

def index(request):
    context={
        "word_count":Word.objects.count(),
        "explanation_count":Explanation.objects.count(),
        "sentence_count":Sentence.objects.count(),
    }
    return render(request,'index.html',context)