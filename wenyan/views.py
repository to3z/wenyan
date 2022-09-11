# Create your views here.
import json
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.urls import reverse

from .models import *

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
    word_stored=get_object_or_404(Word,pk=word_id)
    word_stored.explanation_set.create(
        explanation_text=request.POST['explanation_text'],
        part_of_speech=request.POST['part_of_speech'],
        gu_jin=(request.POST.get('gu_jin')=='gu_jin'),
    )
    return HttpResponseRedirect(reverse('wenyan:edit_explanation',args=(word_stored.word_text,)))

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

    # 是否已经存储了该chuchu
    POST_chuchu=request.POST.get('chuchu')
    chuchu=None
    try:
        chuchu=Chuchu.objects.get(chuchu_text=POST_chuchu)
    except Chuchu.DoesNotExist:
        chuchu=Chuchu(chuchu_text=POST_chuchu)
        chuchu.save()

    # 是否已经存储了该sentence
    sentence_stored=None
    original_jushi=None
    current_jushi=request.POST.get('jushi')
    POST_sentence_text=request.POST.get('sentence_text')
    try:
        sentence_stored=Sentence.objects.get(sentence_text=POST_sentence_text)
        original_jushi=sentence_stored.jushi
    except Sentence.DoesNotExist:
        sentence_stored=Sentence()

    # 更新sentence
    sentence_stored.sentence_text=POST_sentence_text
    sentence_stored.jushi=current_jushi
    sentence_stored.chuchu=chuchu
    sentence_stored.save()

    # 更新sentence_jushi
    if ((not original_jushi) or original_jushi=="无特殊句式") and current_jushi!="无特殊句式":
        # 1. original_jushi=None
        #    这是一句新加入的例句，并且有特殊句式
        # 2. original_jushi="无特殊句式"
        #    原先错误地判断为无特殊句式，现在经过更改，有特殊句式
        sentence_stored.sentence_jushi_set.create()
    elif original_jushi!="无特殊句式" and current_jushi=="无特殊句式":
        # 原先错误地判断为有特殊句式，现在经过更改，无特殊句式
        for sentence_jushi in sentence_stored.sentence_jushi_set.all(): # 实际上应该只循环一次
            sentence_jushi.delete()

    # 更新tongjia
    for tongjia in sentence_stored.tongjia_set.all():
        tongjia.delete()
    POST_before,POST_after=request.POST.getlist('before'),request.POST.getlist('after')
    for i in range(int(request.POST['tongjia_count'])):
        sentence_stored.tongjia_set.create(before=POST_before[i],after=POST_after[i])
    
    # 添加example
    POST_live_use=request.POST.get('live_use')
    example=explanation_stored.example_set.create(
        sentence=sentence_stored,
        live_use=POST_live_use,
    )

    # 添加example_live_use
    if POST_live_use!="无词类活用":
        example.example_live_use_set.create()
    
    # 为example添加appear
    for begin_end in request.POST.getlist('appear_pos'):
        tmp_pair=begin_end.split('-')
        example.appear_set.create(appear_begin=int(tmp_pair[0]),appear_end=int(tmp_pair[1]))
    
    return HttpResponseRedirect(reverse('wenyan:edit_sentence',args=(explanation_id,)))

def index_tips(request):
    part=request.POST.get('search_part')
    tips=[word.word_text for word in Word.objects.filter(word_text__contains=part)]
    return JsonResponse({"data":tips[-5:],"code":200,},json_dumps_params={'ensure_ascii':False})

def sentence_tips(request):
    part=request.POST.get('sentence_part')
    tips=[{"text":sentence.sentence_text,"id":sentence.id} for sentence in Sentence.objects.filter(sentence_text__contains=part)]
    return JsonResponse({"data":tips[-5:],"code":200,},json_dumps_params={'ensure_ascii':False})

def id2info(request):
    """
    通过sentence_tips的<li>元素的id找到对应的sentence
    并将它的信息填入表单
    """
    sentence_id=request.POST.get('sentence_id') # 这里不需要转换成int
    sentence=Sentence.objects.get(id=sentence_id)
    tips={
        "jushi":sentence.jushi,
        "chuchu":sentence.chuchu.chuchu_text,
        "tongjia":[{"before":tj.before,"after":tj.after} for tj in sentence.tongjia_set.all()],
    }
    print("Encounter: ",sentence.sentence_text)
    return JsonResponse({"data":tips,"code":200,},json_dumps_params={'ensure_ascii':False})

def chuchu_tips(request):
    part=request.POST.get('chuchu_part')
    tips=[chuchu.chuchu_text for chuchu in Chuchu.objects.filter(chuchu_text__contains=part)]
    return JsonResponse({"data":tips[-5:],"code":200,},json_dumps_params={'ensure_ascii':False})

def delete_example(request):
    example=get_object_or_404(Example,id=request.POST.get('example_id'))
    explanation_id=example.explanation.id
    example.delete()
    return HttpResponseRedirect(reverse('wenyan:edit_sentence',args=(explanation_id,)))

def delete_explanation(request):
    explanation=get_object_or_404(Explanation,id=request.POST.get('explanation_id'))
    word=explanation.word.word_text
    explanation.delete()
    return HttpResponseRedirect(reverse('wenyan:edit_explanation',args=(word,)))
