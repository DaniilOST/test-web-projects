# Generated by Django 4.2.7 on 2023-11-29 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='auchor',
            new_name='author',
        ),
    ]