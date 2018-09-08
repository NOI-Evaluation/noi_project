# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-09-08 03:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='分类名称')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_num', models.IntegerField(verbose_name='题目编号')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('score', models.SmallIntegerField(default=0, verbose_name='得分')),
                ('code_length', models.IntegerField(verbose_name='代码长度')),
                ('submit_time', models.DateTimeField(auto_now_add=True, verbose_name='提交时间')),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('runtime', models.IntegerField(verbose_name='运行时间')),
                ('memory', models.IntegerField(verbose_name='占用内存')),
                ('try_status', models.BooleanField(default=False, verbose_name='是否尝试')),
                ('self_commit_count', models.SmallIntegerField(default=0, verbose_name='提交次数')),
                ('is_access', models.SmallIntegerField(choices=[(1, '未通过'), (2, '已通过')], default=1, verbose_name='通过状态')),
                ('answer', models.CharField(blank=True, max_length=255, null=True, verbose_name='答案文件路径')),
                ('evaluations', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app01.Evaluation')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=32, unique=True, verbose_name='题目编号')),
                ('title', models.CharField(max_length=32, verbose_name='题目名称')),
                ('time_limit', models.IntegerField(verbose_name='时间限制')),
                ('memory_limit', models.IntegerField(verbose_name='内存限制')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('description', models.TextField(verbose_name='题目描述')),
                ('input_explanation', models.CharField(max_length=255, verbose_name='输入说明')),
                ('output_explanation', models.CharField(max_length=255, verbose_name='输出说明')),
                ('example_input', models.CharField(max_length=255, verbose_name='样例输入')),
                ('example_output', models.CharField(max_length=255, verbose_name='样例输出')),
                ('score', models.SmallIntegerField(default=10, verbose_name='分数')),
                ('commit_count', models.IntegerField(default=0, verbose_name='提交次数')),
                ('auth_status', models.SmallIntegerField(choices=[(1, '未审核'), (2, '审核中'), (3, '已审核')], default=1, verbose_name='审核')),
                ('try_count', models.IntegerField(default=0, verbose_name='尝试人数')),
                ('access_count', models.IntegerField(default=0, verbose_name='通过人数')),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Category')),
            ],
            options={
                'verbose_name_plural': '题目表',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=32, null=True, verbose_name='用户名')),
                ('password', models.CharField(blank=True, max_length=64, null=True, verbose_name='密码')),
                ('email', models.CharField(blank=True, max_length=32, null=True, verbose_name='邮箱')),
                ('level', models.SmallIntegerField(choices=[(1, '青铜'), (2, '白银'), (3, '黄金'), (4, '钻石'), (5, '王者')], default=1, verbose_name='等级')),
                ('avatar', models.CharField(max_length=64, verbose_name='头像')),
                ('roles', models.ManyToManyField(blank=True, to='rbac.Role', verbose_name='拥有的所有角色')),
                ('topics', models.ManyToManyField(through='app01.Evaluation', to='app01.Topic')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Userdetailed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('real_name', models.CharField(blank=True, max_length=12, null=True, verbose_name='真实姓名')),
                ('introduction', models.TextField(blank=True, null=True, verbose_name='自我介绍')),
                ('gender', models.SmallIntegerField(choices=[(0, 'unknown'), (1, '女'), (2, '男')], default=0, verbose_name='性别')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='联系方式')),
                ('birthday', models.DateField(blank=True, help_text='请输入yyyy-mm-dd格式的日期', null=True, verbose_name='出生日期')),
                ('city', models.CharField(blank=True, max_length=12, null=True, verbose_name='城市')),
                ('school', models.CharField(blank=True, max_length=64, null=True, verbose_name='学校')),
                ('qq', models.CharField(blank=True, max_length=32, null=True, verbose_name='QQ号')),
                ('registry_time', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('postal', models.CharField(blank=True, max_length=6, null=True, verbose_name='邮政编码')),
                ('address', models.CharField(blank=True, max_length=64, null=True, verbose_name='邮寄地址')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app01.Userdetailed'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Topic', verbose_name='题目'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.User', verbose_name='做题人'),
        ),
    ]