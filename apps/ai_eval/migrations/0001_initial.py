from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AIEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=200)),
                ('topic_name', models.CharField(max_length=200)),
                ('topic_description', models.TextField()),
                ('resource_type', models.CharField(choices=[('text', 'Text'), ('url', 'URL'), ('pdf', 'PDF')], default='text', max_length=10)),
                ('resource_title', models.CharField(max_length=300)),
                ('resource_url', models.URLField(blank=True, null=True)),
                ('resource_text', models.TextField(blank=True)),
                ('raw_text', models.TextField(blank=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('label', models.CharField(blank=True, choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], max_length=10)),
                ('reason', models.TextField(blank=True)),
                ('key_matches', models.JSONField(default=list)),
                ('missing_topics', models.JSONField(default=list)),
                ('language', models.CharField(default='uz', max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ai_evaluations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'AI Baholash',
                'verbose_name_plural': 'AI Baholashlar',
                'ordering': ['-created_at'],
            },
        ),
    ]