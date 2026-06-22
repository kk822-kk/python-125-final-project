from django.contrib import admin
from .models import Post, Tag, Comment, Profile, Notification

admin.site.site_header = "Geo-Pop Admin"

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'updated_at', 'published')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at', 'tags', 'published')
    inlines = [CommentInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'notification_type', 'created_at')
    list_filter = ('notification_type', 'created_at')
