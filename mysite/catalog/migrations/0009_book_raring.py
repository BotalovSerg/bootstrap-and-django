# Generated by Django 5.0.7 on 2024-08-16 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_userbookrelation_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='raring',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
            preserve_default=False,
        ),
    ]
