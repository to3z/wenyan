from django.shortcuts import render
from .models import Word,Explanation,Sentence,Example,Tongjia,Appear,Chuchu
import random

def Mainpage(request):
    return render(request,'wenyan/frontpage.html',{});

def ExercisePage(request):
    num = Example.objects.count()
    if request.POST.get(key='fuckit'):
        nowdelta=int(request.POST['fuckit'])
        if request.POST.get('indicate')=="上一题":
            choice=(((int(request.POST['fuckyou'])-nowdelta)%num)+num)%num
        else:
            choice=(int(request.POST['fuckyou'])+nowdelta)%num
    else:
        sushu=[1226959, 1635947, 2181271, 2908361, 3877817, 5170427, 6893911, 9191891,122777, 163729, 218357, 291143, 388211, 517619, 690163, 999983,12255871, 16341163, 21788233, 29050993]
        nowdelta=random.randint(0,20)
        nowdelta=sushu[nowdelta]
        choice=random.randint(0,num)
    fuck = Example.objects.all()[choice]
    context={
	    "example":fuck,
	    "answer":fuck.explanation,
	    "delta":str(nowdelta),
	    "now":str(choice)
	}
    return render(request,'wenyan/ExercisePage.html',context);
