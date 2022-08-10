from django.db import models

# Create your models here.
MAXLEN=150

class Word(models.Model):
    word_text=models.CharField(max_length=MAXLEN)
    def __str__(self):
        return self.word_text

class Explanation(models.Model):
    PART_OF_SPEECH=['形容词','副词','名词','动词','介词','连词','代词','助词','数词','量词','其它']
    LIVE_USE=['无词类活用','形容词作名词','形容词作动词','意动用法','使动用法','名词作形容词','名词作状语','名词作动词','动词作名词']
    word=models.ForeignKey(Word,on_delete=models.CASCADE)
    explanation_text=models.CharField(max_length=MAXLEN)
    part_of_speech=models.CharField(max_length=3)
    live_use=models.CharField(max_length=6)
    gu_jin=models.BooleanField(default=False)
    def __str__(self):
        return self.explanation_text

class Sentence(models.Model):
    JUSHI=['无特殊句式','判断句','省略句','被动句','定语后置句','宾语前置句','主谓倒装句','介词结构后置句']
    explanation=models.ForeignKey(Explanation,on_delete=models.CASCADE)
    sentence_text=models.CharField(max_length=MAXLEN)
    jushi=models.CharField(max_length=7)
    chuchu=models.CharField(max_length=MAXLEN)
    def __str__(self):
        return self.sentence_text

class Tongjia(models.Model):
    sentence=models.ForeignKey(Sentence,on_delete=models.CASCADE)
    before=models.CharField(max_length=MAXLEN)
    after=models.CharField(max_length=MAXLEN)
    def __str__(self):
        return self.before+' 通 '+self.after

class Appear(models.Model):
    sentence=models.ForeignKey(Sentence,on_delete=models.CASCADE)
    appear_begin=models.IntegerField()
    appear_end=models.IntegerField()
    def __str__(self):
        return '['+str(self.appear_begin)+','+str(self.appear_end)+')'