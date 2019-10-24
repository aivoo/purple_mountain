from django.db import models
from tinymce.models import HTMLField


class Article(models.Model):
    title = models.CharField('标题', max_length=100, default='')
    abstract = models.TextField('摘要', null=True, blank=True)
    content = HTMLField('内容', null=True, blank=True)
    source = models.CharField('原文地址', max_length=300, null=True, blank=True)
    codeurl = models.TextField('代码地址', null=True, blank=True)
    image = models.TextField('图片地址', null=True, blank=True)
    keyword = models.CharField('公众号关键词', max_length=20, null=True, blank=True)
    exist = models.BooleanField('是否存在', default=True)
    readcount = models.IntegerField('阅读人数', default=0)
    likecount = models.IntegerField('喜欢人数', default=0)
    commentcount = models.IntegerField('评论人数', default=0)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return '%d，%s' % (self.id, self.title)


class Tutorial(models.Model):
    title = models.CharField('标题', max_length=100, default='')
    index = models.IntegerField('序号', unique=True)
    content = HTMLField('内容')
    readcount = models.IntegerField('阅读人数', default=0)
    likecount = models.IntegerField('喜欢人数', default=0)
    commentcount = models.IntegerField('评论人数', default=0)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    exist = models.BooleanField('是否存在', default=True)

    def __str__(self):
        return '%d，%s' % (self.index, self.title)

    class Meta:
        ordering = ['index']


class HostInfo(models.Model):
    LOCK_STATUS = (
        (0, '未锁定'),
        (1, '锁定')
    )
    host = models.CharField('主机ip', max_length=32, unique=True)
    count = models.IntegerField('请求次数', default=1)
    start_time = models.DateTimeField('请求开始时间', auto_now_add=True)
    last_active_time = models.DateTimeField('最近请求时间', auto_now_add=True)
    is_lock = models.IntegerField('ip状态', choices=LOCK_STATUS, default=0)


class TaskList(models.Model):
    title = models.CharField('标题', max_length=100)
    index = models.IntegerField('序号', unique=True)
    content = models.TextField('内容')
    url = models.CharField('url', max_length=100)
    exist = models.BooleanField('是否存在', default=True)

    class Meta:
        ordering = ['index']
