# Generated by Django 4.1.1 on 2022-09-24 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='postType',
            new_name='categoryType',
        ),
    ]