from django.db import models
from django.contrib.auth.models import User


class AIEvaluation(models.Model):
    LABEL_HIGH = 'high'
    LABEL_MEDIUM = 'medium'
    LABEL_LOW = 'low'
    LABEL_CHOICES = [
        (LABEL_HIGH, 'High'),
        (LABEL_MEDIUM, 'Medium'),
        (LABEL_LOW, 'Low'),
    ]

    TYPE_TEXT = 'text'
    TYPE_URL = 'url'
    TYPE_PDF = 'pdf'
    TYPE_CHOICES = [
        (TYPE_TEXT, 'Text'),
        (TYPE_URL, 'URL'),
        (TYPE_PDF, 'PDF'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_evaluations')
    subject_name = models.CharField(max_length=200)
    topic_name = models.CharField(max_length=200)
    topic_description = models.TextField()
    resource_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_TEXT)
    resource_title = models.CharField(max_length=300)
    resource_url = models.URLField(blank=True, null=True)
    resource_text = models.TextField(blank=True)
    raw_text = models.TextField(blank=True)

    # AI result
    score = models.FloatField(null=True, blank=True)
    label = models.CharField(max_length=10, choices=LABEL_CHOICES, blank=True)
    reason = models.TextField(blank=True)
    key_matches = models.JSONField(default=list)
    missing_topics = models.JSONField(default=list)
    language = models.CharField(max_length=5, default='uz')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'AI Baholash'
        verbose_name_plural = 'AI Baholashlar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} — {self.topic_name} ({self.score_percent()}%)"

    def score_percent(self):
        if self.score is not None:
            return int(self.score * 100)
        return 0