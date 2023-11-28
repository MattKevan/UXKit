# Generated by Django 4.2.5 on 2023-11-28 13:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_persona_frustrations_persona_goals_persona_needs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='unique_hash',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
