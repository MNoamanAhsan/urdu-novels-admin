from django.db import models
from django.core.exceptions import ValidationError
import os

def validate_txt_file(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext != '.txt':
        raise ValidationError('Only .txt files are allowed for episode files.')

def novel_cover_upload_to(instance, filename):
    base, ext = os.path.splitext(filename)
    title = instance.title if instance.title else "novel"
    safe_title = "".join(c if c.isalnum() else "-" for c in title)[:50]
    return f"covers/{safe_title}/{base}{ext}"

def episode_file_upload_to(instance, filename):
    novel = instance.novel
    novel_title = novel.title if novel.title else "novel"
    safe_title = "".join(c if c.isalnum() else "-" for c in novel_title)[:50]
    return f"episodes/{safe_title}/ep-{instance.episode_number}-{filename}"

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Novel(models.Model):
    category=models.ForeignKey(Category,on_delete=models.PROTECT,related_name='novels')
    title=models.CharField(max_length=250)
    author=models.CharField(max_length=150,blank=False)
    summary=models.TextField(blank=False)
    about= models.TextField(
        blank=False, 
        default=""
    )
    cover_image=models.ImageField(upload_to=novel_cover_upload_to, blank=False,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['title']

    def __str__(self):
        return self.title
    


class Episode(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=250)
    episode_number = models.PositiveIntegerField(help_text="Numeric ordering for episodes")
    file = models.FileField(upload_to=episode_file_upload_to, validators=[validate_txt_file])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['episode_number']
        unique_together = (('novel', 'episode_number'),)  # ensure uniqueness per novel

    def __str__(self):
        return f"{self.novel.title} — Ep {self.episode_number}: {self.title}"