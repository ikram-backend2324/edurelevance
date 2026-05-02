from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    name = models.CharField(max_length=200, verbose_name="Fan nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='subjects',
        verbose_name="Yaratgan"
    )
    is_public = models.BooleanField(default=False, verbose_name="Ommaviy (admin)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"
        ordering = ['name']

    def __str__(self):
        return self.name

    def topic_count(self):
        return self.topics.count()


class Topic(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE,
        related_name='topics', verbose_name="Fan"
    )
    name = models.CharField(max_length=200, verbose_name="Mavzu nomi")
    description = models.TextField(verbose_name="Mavzu tavsifi")
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='topics',
        verbose_name="Yaratgan"
    )
    is_public = models.BooleanField(default=False, verbose_name="Ommaviy (admin)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mavzu"
        verbose_name_plural = "Mavzular"
        ordering = ['name']

    def __str__(self):
        return f"{self.subject.name} → {self.name}"

    def resource_count(self):
        return self.resources.count()