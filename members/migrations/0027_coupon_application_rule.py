# Generated by Django 4.2.7 on 2024-05-03 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0026_rename_dolloar_amount_coupon_dollar_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='application_rule',
            field=models.CharField(choices=[('PR', 'PER_REGISTRATION'), ('PA', 'PER_ACCOUNT')], default='PR', max_length=2),
            preserve_default=False,
        ),
    ]
