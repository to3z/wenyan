# Generated by Django 4.1 on 2022-08-09 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Explanation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('explanation_text', models.CharField(max_length=150)),
                ('part_of_speech', models.CharField(choices=[('adj', '形容词'), ('adv', '副词'), ('nou', '名词'), ('ver', '动词'), ('pre', '介词'), ('con', '连词'), ('pro', '代词'), ('aux', '助词'), ('num', '数词'), ('qua', '量词'), ('oth', '其它')], default='oth', max_length=3)),
                ('live_use', models.CharField(choices=[('non', '无词类活用'), ('a-n', '形容词作名词'), ('a-v', '形容词作动词'), ('e-v', '意动用法'), ('s-v', '使动用法'), ('n-a', '名词作形容词'), ('n-d', '名词作状语'), ('n-v', '名词作动词'), ('v-n', '动词作名词')], default='non', max_length=3)),
                ('gu_jin', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence_text', models.CharField(max_length=150)),
                ('jushi', models.CharField(choices=[('no', '无特殊句式'), ('pd', '判断句'), ('sl', '省略句'), ('bd', '被动句'), ('dh', '定语后置句'), ('bq', '宾语前置句'), ('zw', '主谓倒装句'), ('jh', '介词结构后置句')], default='no', max_length=2)),
                ('chuchu', models.CharField(max_length=150)),
                ('explanation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wenyan.explanation')),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word_text', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Tongjia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_word', models.CharField(max_length=150)),
                ('to_word', models.CharField(max_length=150)),
                ('sentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wenyan.sentence')),
            ],
        ),
        migrations.AddField(
            model_name='explanation',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wenyan.word'),
        ),
        migrations.CreateModel(
            name='Appear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appear_begin', models.IntegerField()),
                ('appear_end', models.IntegerField()),
                ('sentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wenyan.sentence')),
            ],
        ),
    ]