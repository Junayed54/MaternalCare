# Generated by Django 5.1.5 on 2025-02-05 16:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
        ('hospital', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hospital.hospital'),
        ),
    ]
