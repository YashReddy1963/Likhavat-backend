# Generated by Django 5.2 on 2025-05-15 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0013_alter_blogview_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='blogview',
            unique_together=set(),
        ),
    ]
