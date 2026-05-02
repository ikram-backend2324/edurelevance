from django.db import models
from django.contrib.auth.models import User
from apps.subjects.models import Topic


class Resource(models.Model):
    TYPE_PDF = 'pdf'
    TYPE_URL = 'url'
    TYPE_TEXT = 'text'

    TYPE_CHOICES = [
        (TYPE_PDF, 'PDF Fayl'),
        (TYPE_URL, 'URL Havola'),
        (TYPE_TEXT, 'Matn'),
    ]

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='resources',
        verbose_name="Mavzu"
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='resources',
        verbose_name="Yuklagan foydalanuvchi"
    )
    title = models.CharField(max_length=300, verbose_name="Sarlavha")
    resource_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name="Tur"
    )
    file = models.FileField(
        upload_to='resources/pdfs/',
        null=True,
        blank=True,
        verbose_name="PDF Fayl"
    )
    url = models.URLField(
        null=True,
        blank=True,
        verbose_name="URL Havola"
    )
    text_content = models.TextField(
        null=True,
        blank=True,
        verbose_name="Matn"
    )
    raw_text = models.TextField(
        blank=True,
        verbose_name="Ajratilgan matn"
    )
    is_evaluated = models.BooleanField(default=False, verbose_name="Baholandi")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Resurs"
        verbose_name_plural = "Resurslar"
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    def get_score(self):
        try:
            return self.score
        except RelevanceScore.DoesNotExist:
            return None


class RelevanceScore(models.Model):
    LABEL_HIGH = 'high'
    LABEL_MEDIUM = 'medium'
    LABEL_LOW = 'low'

    LABEL_CHOICES = [
        (LABEL_HIGH, 'Yuqori'),
        (LABEL_MEDIUM, "O'rta"),
        (LABEL_LOW, 'Past'),
    ]

    resource = models.OneToOneField(
        Resource,
        on_delete=models.CASCADE,
        related_name='score',
        verbose_name="Resurs"
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='scores',
        verbose_name="Mavzu"
    )
    score = models.FloatField(verbose_name="Ball (0.0 - 1.0)")
    label = models.CharField(
        max_length=10,
        choices=LABEL_CHOICES,
        verbose_name="Daraja"
    )
    reason = models.TextField(verbose_name="Sabab")
    key_matches = models.JSONField(default=list, verbose_name="Mos kalit so'zlar")
    missing_topics = models.JSONField(default=list, verbose_name="Yetishmayotgan mavzular")
    evaluated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dolzarblik bali"
        verbose_name_plural = "Dolzarblik ballari"
        ordering = ['-score']

    def __str__(self):
        return f"{self.resource.title} → {self.score:.2f} ({self.get_label_display()})"

    def score_percent(self):
        return int(self.score * 100)
