# Generated by Django 4.2.7 on 2024-09-21 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0036_alter_coupon_percentage_alter_course_book_cost_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='percentage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_description',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name='member',
            name='verification_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='chinese_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='joined_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='middle_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]