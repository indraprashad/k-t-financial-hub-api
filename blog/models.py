from django.db import models
from django.utils.text import slugify
from common.models import BaseModel
from blog_categories.models import BlogCategory


class BlogPost(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    excerpt = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    category = models.ForeignKey(
        BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts'
    )
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
