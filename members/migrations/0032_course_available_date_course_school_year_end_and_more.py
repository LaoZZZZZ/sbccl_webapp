# Generated by Django 4.2.7 on 2024-05-24 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0031_schoolcalendar_remove_classgroup_last_udpate_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='available_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='school_year_end',
            field=models.IntegerField(default=2025),
        ),
        migrations.AddField(
            model_name='course',
            name='school_year_start',
            field=models.IntegerField(default=2024),
        ),
    ]
