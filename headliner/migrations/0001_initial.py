# Generated by Django 5.0.1 on 2024-03-18 01:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_description', models.CharField(blank=True, max_length=500, verbose_name='New Post')),
                ('creation_time', models.DateTimeField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='entry_creators', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
