# Generated by Django 2.2.4 on 2022-01-30 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='round',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Round'),
        ),
    ]
