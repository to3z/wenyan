# Create your views here.
import json
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.urls import reverse

from .models import Word,Explanation,Sentence,Example,Tongjia,Appear

def index(request):
    return render(request,'wenyan/index.html',{})

def search_result(request):
    return HttpResponseRedirect(reverse('wenyan:word',args=(request.GET['search'],)))

def word(request,word):
    context={}
    try:
        search_word=Word.objects.get(word_text=word)
    except Word.DoesNotExist:
        context={
            'word_text':word,
        }
    else:
        context={
            'word':search_word,
            'word_text':word,
        }
    return render(request,'wenyan/word.html',context)

def edit_explanation(request,word):
    edit_word=None
    try:
        edit_word=Word.objects.get(word_text=word)
    except Word.DoesNotExist:
        edit_word=Word(word_text=word)
        edit_word.save()
    context={
        'word':edit_word,
        'part_of_speech_options':Explanation.PART_OF_SPEECH,
    }
    return render(request,'wenyan/edit_explanation.html',context)

def submit_explanation(request,word_id):
    word=get_object_or_404(Word,pk=word_id)
    word.explanation_set.create(
        explanation_text=request.POST['explanation_text'],
        part_of_speech=request.POST['part_of_speech'],
        gu_jin=(request.POST.get('gu_jin')=='gu_jin'),
    )
    return HttpResponseRedirect(reverse('wenyan:edit_explanation',args=(word.word_text,)))

def edit_sentence(request,explanation_id):
    explanation=Explanation.objects.get(pk=explanation_id)
    context={
        'word_text':explanation.word.word_text,
        'explanation':explanation,
        'live_use_options':Example.LIVE_USE,
        'jushi_options':Sentence.JUSHI,
    }
    return render(request,'wenyan/edit_sentence.html',context)

def submit_sentence(request,explanation_id):
    explanation_stored=get_object_or_404(Explanation,pk=explanation_id)
    sentence_stored=None
    POST_sentence_text=request.POST.get('sentence_text')
    try:
        sentence_stored=Sentence.objects.get(sentence_text=POST_sentence_text)
    except Sentence.DoesNotExist:
        sentence_stored=Sentence(
            sentence_text=POST_sentence_text,
            jushi=request.POST.get('jushi'),
            chuchu=request.POST.get('chuchu'),
        )
        sentence_stored.save()
    example=explanation_stored.example_set.create(
        sentence=sentence_stored,
        live_use=request.POST.get('live_use'),
    )
    # live_use
    POST_before,POST_after=request.POST.getlist('before'),request.POST.getlist('after')
    for i in range(int(request.POST['tongjia_count'])):
        sentence_stored.tongjia_set.create(before=POST_before[i],after=POST_after[i])
    for begin_end in request.POST.getlist('appear_pos'):
        tmp_pair=begin_end.split('-')
        example.appear_set.create(appear_begin=int(tmp_pair[0]),appear_end=int(tmp_pair[1]))
    return HttpResponseRedirect(reverse('wenyan:edit_sentence',args=(explanation_id,)))

def index_tips(request):
    part=request.POST.get('search_text')
    tips=[word.word_text for word in Word.objects.filter(word_text__contains=part)]
    return JsonResponse({"data":tips,"code":200,},json_dumps_params={'ensure_ascii':False})