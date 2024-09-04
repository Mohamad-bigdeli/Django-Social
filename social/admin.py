from django.contrib import admin
from .models import *

# Register your models here.

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

def make_deactivation(modeladmin, request, queryset):
    result = queryset.update(active=False)
    modeladmin.message_user(request, f"{result} Post rejected")

make_deactivation.short_description = 'deactivation'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'created']
    ordering = ['created']
    search_fields =  ['caption']
    inlines = [ImageInline]
    actions = [make_deactivation]
    

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'created']
