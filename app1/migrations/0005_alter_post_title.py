# Generated by Django 4.1.1 on 2022-10-03 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=128),
        ),
    ]
