from django.shortcuts import render
from django.db.models import Q
from .models import Word,Explanation,Sentence,Example,Tongjia,Appear,Chuchu,Example_live_use,Sentence_jushi,Visit
import random,pickle

def Mainpage(request):
    return render(request,'wenyan/frontpage.html',{});

def Mainpage_hy(request):
    return render(request,'wenyan/frontpage_hy.html',{});

def ExercisePage(request):
    exercise_type=['请解释加点词含义','请判断加点词词类活用类型','请判断句子的句式']
    num=[Example.objects.count(),Example_live_use.objects.count(),Sentence_jushi.objects.count()]
    for i in range(3):
        num.append(num[0])
    if request.POST.get(key='fuckit'):
        nowdelta=int(request.POST['fuckit'])
        if request.POST.get('indicate')=="上一题":
            nowall=int(request.POST['fuckhim'])-nowdelta
            if nowall<0:
                nowall+=nowdelta
            nowtype=int(request.POST['fuckher'])-nowdelta
            if nowtype<0:
                nowtype+=nowdelta
            choice_type=nowtype%6
            choice=nowall%num[choice_type]
            highlight=choice_type%6-2
        else:
            nowall=int(request.POST['fuckhim'])+nowdelta
            nowtype=int(request.POST['fuckher'])+nowdelta
            choice_type=nowtype%6
            choice=nowall%num[choice_type]
            highlight=choice_type%6-2
    else:
        sushu=[1226959, 1635947, 2181271, 2908361, 3877817, 5170427, 6893911, 9191891,122777, 163729, 218357, 291143, 388211, 517619, 690163, 999983,12255871, 16341163, 21788233, 29050993]
        nowdelta=random.randint(0,19)
        nowdelta=sushu[nowdelta]
        nowtype=choice_type=random.randint(0,5)
        nowall=choice=random.randint(0,num[choice_type]-1)
        highlight=nowtype-2
    if choice_type==0 or choice_type>2:
        fuck=Example.objects.all()[choice]
        answer=fuck.explanation
        choice_type=0
    elif choice_type==1:
        fuck=Example_live_use.objects.all()[choice].example
        answer=fuck.live_use
    elif choice_type==2:
        fuck=Sentence_jushi.objects.all()[choice].sentence
        answer=fuck.jushi
    context={
	    "example":fuck,
	    "answer":answer,
            "etype":exercise_type[choice_type],
            "delta":str(nowdelta),
            "nowall":str(nowall),
            "nowtype":str(nowtype),
            "hilight":highlight
	}
    return render(request,'wenyan/ExercisePage.html',context)

def TestPage(request):
    if request.POST.get(key='ques'):
        now=allnum=int(request.POST['cnt'])
        score=int(request.POST['score'])
        lianxu=int(request.POST['lianxu'])
        userip=request.META.get('REMOTE_ADDR')
        filename=userip+'.pickle'
        f=open(filename,'rb')
        list_b=pickle.load(f)
        nowlist=pickle.loads(list_b)
        f.close()
        nowlist[now-1].append(request.POST.get(key='ques'))
        nowlist[now-1].append(request.POST.get(key='ques')==nowlist[now-1][3])
        if nowlist[now-1][7]:
            lianxu+=1
            score+=lianxu
        else:
            lianxu=0
        nowlist[now-1].append(lianxu)
        f=open(filename,'wb')
        newlist=pickle.dumps(nowlist)
        pickle.dump(newlist,f)
        f.close()
        context={
            "now":now,
            "allnum":allnum,
            "score":score,
            "avr":round(float(score)/allnum,2),
            "lianxu":lianxu,
            "nowtype":nowlist[now-1][0],
            "defen":nowlist[now-1][8],
            "question":nowlist[now-1][1],
            "text":nowlist[now-1][2],
            "choice":nowlist[now-1][4],
            "correct":nowlist[now-1][7],
            "reason":nowlist[now-1][5],
            "choose":nowlist[now-1][6],
            "ans":nowlist[now-1][3],
        }
        return render(request,'wenyan/AnswerPage.html',context)
    elif request.POST.get('indicate')=="上一题":
        now=int(request.POST['cnt'])-1
        lianxu=int(request.POST['lianxu'])
        score=int(request.POST['score'])
        userip=request.META.get('REMOTE_ADDR')
        filename=userip+'.pickle'
        if now==0:
            now=1
        allnum=int(request.POST['mx'])
        f=open(filename,'rb')
        list_b=pickle.load(f)
        nowlist=pickle.loads(list_b)
        f.close()
        context={
            "now":now,
            "allnum":allnum,
            "score":score,
            "avr":round(float(score)/allnum,2),
            "lianxu":lianxu,
            "defen":nowlist[now-1][8],
            "nowtype":nowlist[now-1][0],
            "question":nowlist[now-1][1],
            "text":nowlist[now-1][2],
            "choice":nowlist[now-1][4],
            "correct":nowlist[now-1][7],
            "reason":nowlist[now-1][5],
            "choose":nowlist[now-1][6],
            "ans":nowlist[now-1][3],
        }
        return render(request,'wenyan/AnswerPage.html',context)
    elif request.POST.get('indicate')=="结束测试":
        allnum=int(request.POST['mx'])
        score=int(request.POST['score'])
        avr=round(float(score)/allnum,2)
        Visit.objects.create(visit_score=avr)
        baifenwei=Visit.objects.filter(visit_score__gt=avr).count()
        baifenwei=round(float(baifenwei)/Visit.objects.count(),4)
        baifenwei=(1-baifenwei)*100
        context={
            "allnum":allnum,
            "score":score,
            "avr":avr,
            "baifenwei":baifenwei,
        }
        return render(request,'wenyan/ScorePage.html',context)
    else:
        if request.POST.get("indicate")=="下一题":
            now=int(request.POST['cnt'])+1
            allnum=int(request.POST['mx'])
            lianxu=int(request.POST['lianxu'])
            score=int(request.POST['score'])
        else:
            now=1
            allnum=0
            lianxu=0
            score=0
        userip=request.META.get('REMOTE_ADDR')
        filename=userip+'.pickle'
        if now>allnum:
            num=Sentence.objects.count()
            nowtype=random.randint(0,4)
            question=["请问下列句子中共含有多少个通假字","请问下列句子中共含有几类特殊句式","请问下列句子中有几句属于特殊句式","请问下列句子中含有词类活用的有几句","请问下列句子的加点字中共含有几类词类活用"]
            text=[]
            for i in range(8):
                t=random.randint(0,num-1)
                while t in text:
                    t=random.randint(0,num-1)
                text.append(t)
            if nowtype==0:
                ans=0
                reason=[]
                for i in range(8):
                    allans=Sentence.objects.all()[text[i]].tongjia_set
                    ansnum=allans.count()
                    nowreason=[]
                    ans+=ansnum
                    if ansnum==0:
                        nowreason.append('无通假')
                    else:
                        for j in range(ansnum):
                            nowreason.append(allans.all()[j].__str__())
                    reason.append(nowreason)
                    text[i]=Sentence.objects.all()[text[i]].sentence_text
                choicedelta=random.randint(0,min(3,ans))
                choice=[ans-choicedelta,ans-choicedelta+1,ans-choicedelta+2,ans-choicedelta+3]
                ans=chr(ord('A')+choicedelta)
            elif nowtype==1:
                ans=0
                reason=[]
                nowjushi=[]
                for i in range(8):
                    ju_shi=Sentence.objects.all()[text[i]].jushi
                    if ju_shi!='无特殊句式':
                        if ju_shi not in nowjushi:
                            ans+=1
                            nowjushi.append(ju_shi)
                    nowreason=[]
                    nowreason.append(ju_shi)
                    reason.append(nowreason)
                    text[i]=Sentence.objects.all()[text[i]].sentence_text
                choicedelta=random.randint(0,min(3,ans))
                choice=[ans-choicedelta,ans-choicedelta+1,ans-choicedelta+2,ans-choicedelta+3]
                ans=chr(ord('A')+choicedelta)
            elif nowtype==2:
                ans=0
                reason=[]
                for i in range(8):
                    ju_shi=Sentence.objects.all()[text[i]].jushi
                    if ju_shi!='无特殊句式':
                        ans+=1
                    nowreason=[]
                    nowreason.append(ju_shi)
                    reason.append(nowreason)
                    text[i]=Sentence.objects.all()[text[i]].sentence_text
                choicedelta=random.randint(0,min(3,ans))
                choice=[ans-choicedelta,ans-choicedelta+1,ans-choicedelta+2,ans-choicedelta+3]
                ans=chr(ord('A')+choicedelta)
            elif nowtype==3:
                ans=0
                reason=[]
                for i in range(8):
                    allans=Sentence.objects.all()[text[i]].example_set
                    nowreason=[]
                    ansnum=0
                    for example in allans.all():
                        if example.live_use!='无词类活用':
                            ansnum+=1
                            nowreason.append(example.live_use)
                    if ansnum==0:
                        nowreason.append('无词类活用')
                    ans+=ansnum
                    reason.append(nowreason)
                    text[i]=Sentence.objects.all()[text[i]].sentence_text
                choicedelta=random.randint(0,min(3,ans))
                choice=[ans-choicedelta,ans-choicedelta+1,ans-choicedelta+2,ans-choicedelta+3]
                ans=chr(ord('A')+choicedelta)
            elif nowtype==4:
                ans=0
                reason=[]
                nowhuoyong=[]
                for i in range(8):
                    allans=Sentence.objects.all()[text[i]].example_set
                    examplenum=allans.count()
                    nowexample=allans.all()[random.randint(0,examplenum-1)]
                    nowreason=[]
                    ansnum=0
                    if nowexample.live_use!='无词类活用':
                        if nowexample.live_use not in nowhuoyong:
                            ansnum+=1
                            nowhuoyong.append(nowexample.live_use)
                    nowreason.append(nowexample.live_use)
                    ans+=ansnum
                    reason.append(nowreason)
                    text[i]=nowexample
                choicedelta=random.randint(0,min(3,ans))
                choice=[ans-choicedelta,ans-choicedelta+1,ans-choicedelta+2,ans-choicedelta+3]
                ans=chr(ord('A')+choicedelta)
            questionall=[]
            questionall.append(nowtype)
            questionall.append(question[nowtype])
            questionall.append(text)
            questionall.append(ans)
            questionall.append(choice)
            questionall.append(reason)
            if now==1:
                nowlist=[]
            else:
                f=open(filename,'rb')
                list_b=pickle.load(f)
                nowlist=pickle.loads(list_b)
                f.close()
            nowlist.append(questionall)
            if allnum==0:
                avr=0.0
            else:
                avr=float(score)/allnum
            list_b=pickle.dumps(nowlist)
            f=open(filename,'wb')
            pickle.dump(list_b,f)
            f.close()
            context={
                "now":now,
                "allnum":allnum+1,
                "score":score,
                "avr":round(avr,2),
                "lianxu":lianxu,
                "nowtype":nowtype,
                "question":question[nowtype],
                "text":text,
                "choice":choice,
            }
            return render(request,'wenyan/TestPage.html',context)
        else:
            f=open(filename,'rb')
            list_b=pickle.load(f)
            nowlist=pickle.loads(list_b)
            f.close()
            context={
                "now":now,
                "allnum":allnum,
                "score":score,
                "avr":round(float(score)/allnum,2),
                "lianxu":lianxu,
                "nowtype":nowlist[now-1][0],
                "defen":nowlist[now-1][8],
                "question":nowlist[now-1][1],
                "text":nowlist[now-1][2],
                "choice":nowlist[now-1][4],
                "correct":nowlist[now-1][7],
                "reason":nowlist[now-1][5],
                "choose":nowlist[now-1][6],
                "ans":nowlist[now-1][3],
            }
            return render(request,'wenyan/AnswerPage.html',context)

def AnswerPage(request):
    if request.POST.get('indicate')=="查看题目":
        now=1
        allnum=int(request.POST['mx'])
        avr=float(request.POST['avr'])
        score=int(request.POST['score'])
        userip=request.META.get('REMOTE_ADDR')
        filename=userip+'.pickle'
        f=open(filename,'rb')
        list_b=pickle.load(f)
        nowlist=pickle.loads(list_b)
        f.close()
        context={
            "now":now,
            "allnum":allnum,
            "score":score,
            "avr":avr,
            "lianxu":0,
            "defen":nowlist[now-1][8],
            "nowtype":nowlist[now-1][0],
            "question":nowlist[now-1][1],
            "text":nowlist[now-1][2],
            "choice":nowlist[now-1][4],
            "correct":nowlist[now-1][7],
            "reason":nowlist[now-1][5],
            "choose":nowlist[now-1][6],
            "ans":nowlist[now-1][3],
        }
        return render(request,'wenyan/AnswerPage2.html',context)
    elif request.POST.get('indicate')=="上一题":
        now=int(request.POST['cnt'])-1
        lianxu=int(request.POST['lianxu'])
        score=int(request.POST['score'])
        userip=request.META.get('REMOTE_ADDR')
        filename=userip+'.pickle'
        if now==0:
            now=1
        allnum=int(request.POST['mx'])
        f=open(filename,'rb')
        list_b=pickle.load(f)
        nowlist=pickle.loads(list_b)
        f.close()
        context={
            "now":now,
            "allnum":allnum,
            "score":score,
            "avr":round(float(score)/allnum,2),
            "lianxu":lianxu,
            "defen":nowlist[now-1][8],
            "nowtype":nowlist[now-1][0],
            "question":nowlist[now-1][1],
            "text":nowlist[now-1][2],
            "choice":nowlist[now-1][4],
            "correct":nowlist[now-1][7],
            "reason":nowlist[now-1][5],
            "choose":nowlist[now-1][6],
            "ans":nowlist[now-1][3],
        }
        return render(request,'wenyan/AnswerPage2.html',context)
    elif request.POST.get('indicate')=="下一题":
        now=int(request.POST['cnt'])+1
        lianxu=int(request.POST['lianxu'])
        score=int(request.POST['score'])
        userip=request.META.get('REMOTE_ADDR')
        filename=userip+'.pickle'
        allnum=int(request.POST['mx'])
        if now>allnum:
            now=allnum
        f=open(filename,'rb')
        list_b=pickle.load(f)
        nowlist=pickle.loads(list_b)
        f.close()
        context={
            "now":now,
            "allnum":allnum,
            "score":score,
            "avr":round(float(score)/allnum,2),
            "lianxu":lianxu,
            "defen":nowlist[now-1][8],
            "nowtype":nowlist[now-1][0],
            "question":nowlist[now-1][1],
            "text":nowlist[now-1][2],
            "choice":nowlist[now-1][4],
            "correct":nowlist[now-1][7],
            "reason":nowlist[now-1][5],
            "choose":nowlist[now-1][6],
            "ans":nowlist[now-1][3],
        }
        return render(request,'wenyan/AnswerPage2.html',context)
