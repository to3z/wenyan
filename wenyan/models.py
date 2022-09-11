from django.db import models

# Create your models here.
MAXLEN=150

class Word(models.Model):
    word_text=models.CharField(max_length=MAXLEN)
    def __str__(self):
        return self.word_text

class Explanation(models.Model):
    PART_OF_SPEECH=['形容词','副词','名词','动词','介词','连词','代词','助词','数词','量词','其它']
    word=models.ForeignKey(Word,on_delete=models.CASCADE,null=True)
    explanation_text=models.CharField(max_length=MAXLEN)
    part_of_speech=models.CharField(max_length=3)
    gu_jin=models.BooleanField(default=False)
    def __str__(self):
        return self.explanation_text

class Chuchu(models.Model):
    chuchu_text=models.CharField(max_length=MAXLEN)
    def __str__(self):
        return self.chuchu_text

class Sentence(models.Model):
    JUSHI=['无特殊句式','判断句','省略句','被动句','定语后置句','宾语前置句','主谓倒装句','介词结构后置句']
    sentence_text=models.CharField(max_length=MAXLEN)
    jushi=models.CharField(max_length=7)
    # chuchu=models.CharField(max_length=MAXLEN)
    chuchu=models.ForeignKey(Chuchu,on_delete=models.CASCADE,null=True) # 这个CASCADE不会真正被触发，为了避免报错而写了CASCADE（实际上仅仅表示关联而不表示从属）
    def __str__(self):
        return self.sentence_text

class Example(models.Model):
    LIVE_USE=['无词类活用','形容词作名词','形容词作动词','意动用法','使动用法','名词作形容词','名词作状语','名词作动词','动词作名词']
    explanation=models.ForeignKey(Explanation,on_delete=models.CASCADE,null=True)
    sentence=models.ForeignKey(Sentence,on_delete=models.CASCADE,null=True) # 这个CASCADE不会真正被触发，为了避免报错而写了CASCADE（实际上仅仅表示关联而不表示从属）
    live_use=models.CharField(max_length=6)
    def __str__(self):
        return self.sentence.sentence_text+" -> "+self.explanation.word.word_text+"("+self.explanation.explanation_text+")"

class Tongjia(models.Model):
    sentence=models.ForeignKey(Sentence,on_delete=models.CASCADE,null=True)
    before=models.CharField(max_length=MAXLEN)
    after=models.CharField(max_length=MAXLEN)
    def __str__(self):
        return self.before+' 同 '+self.after

class Appear(models.Model):
    example=models.ForeignKey(Example,on_delete=models.CASCADE,null=True)
    appear_begin=models.IntegerField()
    appear_end=models.IntegerField()
    def __str__(self):
        return '['+str(self.appear_begin)+','+str(self.appear_end)+')'

class Example_live_use(models.Model):
    example=models.ForeignKey(Example,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.example.sentence.sentence_text

class Sentence_jushi(models.Model):
    sentence=models.ForeignKey(Sentence,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.sentence.sentence_text

class Visit(models.Model):
    visit_score=models.FloatField()
    def __str__(self):
        return '成绩：'+str(self.visit_score)
