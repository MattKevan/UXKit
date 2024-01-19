# Generated by Django 4.2.7 on 2023-12-06 20:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0013_rename_outcomes_leanuxcanvas_user_outcomes_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="leanuxcanvas",
            old_name="assumptions",
            new_name="lean_assumptions",
        ),
        migrations.RenameField(
            model_name="leanuxcanvas",
            old_name="experiment_method",
            new_name="lean_experiments",
        ),
        migrations.RenameField(
            model_name="leanuxcanvas",
            old_name="experiment_success_metrics",
            new_name="lean_hypotheses",
        ),
        migrations.RenameField(
            model_name="leanuxcanvas",
            old_name="experiment_what_to_test",
            new_name="lean_outcomes",
        ),
        migrations.RenameField(
            model_name="leanuxcanvas",
            old_name="problem",
            new_name="lean_problem",
        ),
        migrations.RenameField(
            model_name="leanuxcanvas",
            old_name="hypotheses",
            new_name="lean_solutions",
        ),
        migrations.RenameField(
            model_name="leanuxcanvas",
            old_name="learning_metrics_tracking",
            new_name="lean_users",
        ),
        migrations.RemoveField(
            model_name="leanuxcanvas",
            name="mvp_actions",
        ),
        migrations.RemoveField(
            model_name="leanuxcanvas",
            name="primary_outcome",
        ),
        migrations.RemoveField(
            model_name="leanuxcanvas",
            name="primary_users",
        ),
        migrations.RemoveField(
            model_name="leanuxcanvas",
            name="secondary_outcomes",
        ),
        migrations.RemoveField(
            model_name="leanuxcanvas",
            name="secondary_users",
        ),
        migrations.RemoveField(
            model_name="leanuxcanvas",
            name="solution_ideas",
        ),
        migrations.RemoveField(
            model_name="leanuxcanvas",
            name="user_outcomes",
        ),
        migrations.RemoveField(
            model_name="leanuxcanvas",
            name="user_problems",
        ),
        migrations.AlterField(
            model_name="leanuxcanvas",
            name="name",
            field=models.CharField(max_length=200),
        ),
    ]