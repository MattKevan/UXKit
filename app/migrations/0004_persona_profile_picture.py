# Generated by Django 4.2.5 on 2023-11-24 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_persona_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
