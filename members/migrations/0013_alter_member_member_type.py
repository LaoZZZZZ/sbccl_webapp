# Generated by Django 4.2.7 on 2024-03-16 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0012_alter_student_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='member_type',
            field=models.CharField(choices=[('P', 'Parent'), ('B', 'BoardMember'), ('V', 'Volunteer'), ('T', 'Teacher')], max_length=1, null=True),
        ),
    ]
