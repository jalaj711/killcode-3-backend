# Generated by Django 2.2.4 on 2023-03-31 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0013_clue'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClueRedirect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clue_id', models.CharField(max_length=30, verbose_name='Unique ID of the clue')),
                ('redirect_to', models.CharField(max_length=50, verbose_name='Redirect URI for the clue')),
            ],
        ),
    ]
