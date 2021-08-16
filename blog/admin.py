from django.contrib import admin
# Importing Necessary Models
from .models import BlogAuthor, Post, Configuration, PostComment

# Register your models here.

# Minimal registration of Models.
admin.site.register(BlogAuthor)
admin.site.register(Configuration)

# Post Model Admin Registration
class PostCommentsInline(admin.TabularInline):
    """
    Used to show 'existing' blog comments inline below associated blogs
    """
    model = PostComment
    max_num=0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Administration object for Blog models.
    Defines:
     - fields to be displayed in list view (list_display)
     - orders fields in detail view (fields), grouping the date fields horizontally
     - adds inline addition of blog comments in blog view (inlines)
    """
    search_fields = ("title__startswith", )
    list_display = ('title', 'author', 'post_date')
    inlines = [PostCommentsInline]