# Generated by Django 4.2.7 on 2024-05-09 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0027_coupon_application_rule'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='textbook_ordered',
            field=models.BooleanField(default=False, null=True),
        ),
    ]