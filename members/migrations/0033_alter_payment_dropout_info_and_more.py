# Generated by Django 4.2.7 on 2024-06-16 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0032_course_available_date_course_school_year_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='dropout_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.dropout', verbose_name='Related dropout'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('NA', 'NOT_AVAILABLE'), ('CA', 'CASH'), ('CH', 'Check'), ('EL', 'Electronic')], default='NA', max_length=2),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(choices=[('FP', 'FullPayment'), ('PP', 'PartialPayment'), ('FR', 'FullRefund'), ('PR', 'PartialRefund'), ('NP', 'NotPaid')], default='NP', max_length=2),
        ),
    ]
