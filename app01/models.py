from django.db import models

# Create your models here.
from django.db import models
from rbac.models import UserInfo as RbacUserInfo
# 权限表用rbac


class Topic(models.Model):
    '''题目表'''
    # 根据ID来生成题目的编号
    number = models.CharField(max_length=32,verbose_name='题目编号', unique=True)
    title = models.CharField(max_length=32, verbose_name='题目名称')
    time_limit = models.IntegerField(verbose_name='时间限制')  # 单位为ms

    memory_limit = models.IntegerField(verbose_name='内存限制')  # 单位为kb
    # user = models.ForeignKey(to='User', verbose_name='出题人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    description = models.TextField(verbose_name='题目描述')
    input_explanation = models.CharField(max_length=255, verbose_name='输入说明')
    output_explanation = models.CharField(max_length=255, verbose_name='输出说明')
    example_input = models.CharField(max_length=255, verbose_name='样例输入')
    example_output = models.CharField(max_length=255, verbose_name='样例输出')
    score = models.SmallIntegerField(verbose_name='分数',default=10)

    # directions题目说明

    commit_count = models.IntegerField(verbose_name='提交次数', default=0)

    status_choices = (
        (1, '未审核'),
        (2, '审核中'),
        (3, '已审核'),
    )
    auth_status = models.SmallIntegerField(verbose_name='审核', default=1, choices=status_choices)

    # 用户只在第一次进来时尝试次数加一次
    try_count = models.IntegerField(verbose_name='尝试人数', default=0)
    # 用户只有在第一次(多次提交只增加提交数)通过后增加一次
    access_count = models.IntegerField(verbose_name='通过人数', default=0)

    # evaluation_source_code 测评源码

    categories = models.ForeignKey(to='Category')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '题目表'


class Category(models.Model):
    '''题目分类表'''
    title = models.CharField(max_length=32, unique=True, verbose_name='分类名称')

    def __str__(self):
        return self.title


class User(RbacUserInfo):
    '''用户'''
    # 头像图片的存储路径
    level_choices = (
        (1, '青铜'),
        (2, '白银'),
        (3, '黄金'),
        (4, '钻石'),
        (5, '王者'),
    )
    level = models.SmallIntegerField(choices=level_choices, default=1, verbose_name='等级')
    avatar = models.CharField(max_length=64, verbose_name='头像')
    user = models.OneToOneField(to='Userdetailed')
    topics = models.ManyToManyField(to='Topic', through='Evaluation',)

    def __str__(self):
        return self.user


class Userdetailed(models.Model):
    '''用户详情'''
    real_name = models.CharField(max_length=12, blank=True, null=True, verbose_name='真实姓名')
    introduction = models.TextField(blank=True, null=True, verbose_name='自我介绍')

    gender_choices = (
        (0, 'unknown'),
        (1, '女'),
        (2, '男'),
    )
    gender = models.SmallIntegerField(choices=gender_choices, default=0, verbose_name='性别')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='联系方式')

    # 已下3个字段是否做成选择项
    birthday = models.DateField(verbose_name='出生日期', blank=True, null=True, help_text='请输入yyyy-mm-dd格式的日期')
    city = models.CharField(max_length=12, blank=True, null=True, verbose_name='城市')
    school = models.CharField(max_length=64, blank=True, null=True, verbose_name='学校')

    qq = models.CharField(max_length=32, blank=True, null=True, verbose_name='QQ号')
    registry_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    postal = models.CharField(max_length=6, blank=True, null=True, verbose_name='邮政编码')
    address = models.CharField(max_length=64, blank=True, null=True, verbose_name='邮寄地址')


class Evaluation(models.Model):
    '''选手测评表'''
    # 选手测评表, 包括字段：id, 题目编号, 用户名, 得分, 代码长度, 提交时间, 选手每提交一次, 则产生一条记录。
    topic_num = models.IntegerField(verbose_name='题目编号')
    username = models.CharField(max_length=32,verbose_name='用户名')
    score = models.SmallIntegerField(verbose_name='得分', default=0)
    code_length = models.IntegerField(verbose_name='代码长度')
    submit_time = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')

    user = models.ForeignKey(to='User', verbose_name='做题人')
    topic = models.ForeignKey(to='Topic', verbose_name='题目')


class EvaluationDetail(models.Model):
    '''选手测评明细表,关联选手测评表中的id,每个id分别对应每组测试数据的测评结果'''
    evaluations = models.OneToOneField('Evaluation')
    runtime = models.IntegerField(verbose_name='运行时间')
    memory = models.IntegerField(verbose_name='占用内存')


    try_status = models.BooleanField(verbose_name='是否尝试', default=False)
    self_commit_count = models.SmallIntegerField(verbose_name='提交次数', default=0)

    status_choices = (
        (1, '未通过'),
        (2, '已通过'),
    )
    is_access = models.SmallIntegerField(choices=status_choices, default=1, verbose_name='通过状态')
    answer = models.CharField(max_length=255, verbose_name='答案文件路径', blank=True, null=True)
