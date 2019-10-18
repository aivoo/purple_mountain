from django.contrib import admin

from .models import Article, Tutorial, HostInfo, TaskList


class ArticleAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'readcount', 'likecount','commentcount', 'image', 'exist')


class TutorialAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'index', 'readcount', 'likecount','commentcount', 'create_time', 'exist')


class HostInfoAdmin(admin.ModelAdmin):

    list_display = ('id', 'host', 'count', 'start_time', 'last_active_time', 'is_lock')


class TaskListAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'index', 'content', 'url')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(HostInfo, HostInfoAdmin)
admin.site.register(TaskList, TaskListAdmin)
