# Generated by Django 4.2.5 on 2023-11-24 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_persona_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='frustrations',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='goals',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='needs',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='age',
            field=models.CharField(max_length=50),
        ),
    ]