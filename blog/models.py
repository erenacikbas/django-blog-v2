# Necessary Imports
from django.db import models
from datetime import date
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User  # Blog author or commenter
from ckeditor.fields import RichTextField


# Create your models here.
class BlogAuthor(models.Model):
    """
    Model representing a blogger.
    """
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(max_length=400,
                           help_text="Enter your bio details here.")

    class Meta:
        ordering = ["user", "bio"]

    def get_absolute_url(self):
        """
        Return the url to access a particular blog-author instance.
        """
        return reverse('posts-by-author', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.user.username


class Post(models.Model):
    """
    Model representing a blog post.
    """
    title = models.CharField(max_length=200)
    header_image = models.ImageField(null=True, blank=True)
    subtitle = models.CharField(max_length=200)
    author = models.ForeignKey(BlogAuthor,
                               on_delete=models.SET_NULL,
                               null=True)
    # Foreign Key used because blog can only have one author(User), but bloggers can have multiple blog posts.
    body = RichTextField(blank=True, null=True)
    post_date = models.DateField(default=date.today)

    class Meta:
        ordering = ["-post_date"]

    def get_absolute_url(self):
        """
        Returns the url to access a particular blog instance.
        """
        return reverse('post-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title


class PostComment(models.Model):
    """
    Model representing a comment against a blog post.
    """
    comment = models.CharField(max_length=400)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # Foreign Key used because BlogComment can only have one author(User), but users can have multiple comments
    post_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ["post_date"]

    def __str__(self):
        """
        String for representing the Model object.
        """
        len_title = 75
        if len(self.description) > len_title:
            titlestring = self.description[:len_title] + '...'
        else:
            titlestring = self.description
        return titlestring


# Configurations for blog Application
class Configuration(models.Model):
    """
    Model representing Site Configurations
    """
    name = "Configurations"
    index_title = models.CharField(max_length=100)
    index_subtitle = models.CharField(max_length=250)
    index_header_image = models.ImageField(null=True, blank=True)
    index_body = RichTextField(blank=True, null=True)
    about_title = models.CharField(max_length=100)
    about_subtitle = models.CharField(max_length=250)
    about_header_image = models.ImageField(null=True, blank=True)
    about_body = RichTextField(blank=True, null=True)
    contact_title = models.CharField(max_length=100)
    contact_subtitle = models.CharField(max_length=250)
    contact_header_image = models.ImageField(null=True, blank=True)
    contact_body = RichTextField(blank=True, null=True)
    login_background = models.ImageField(null=True, blank=True)
    register_background = models.ImageField(null=True, blank=True)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name
