# Generated by Django 4.2.7 on 2023-12-09 21:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0014_rename_assumptions_leanuxcanvas_lean_assumptions_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="leanuxcanvas",
            name="lean_user_outcomes",
            field=models.TextField(null=True),
        ),
    ]