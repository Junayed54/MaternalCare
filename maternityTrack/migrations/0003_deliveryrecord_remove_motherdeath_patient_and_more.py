# Generated by Django 5.1.5 on 2025-02-06 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maternityTrack', '0002_rename_patient_ancschedule_pregnancy_record'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_phone', models.CharField(help_text='Phone number of the mother', max_length=15, unique=True)),
                ('mother_status', models.CharField(choices=[('Alive', 'Alive'), ('Deceased', 'Deceased'), ('Stillborn', 'Stillborn')], default='Alive', help_text="Mother's status", max_length=10)),
                ('delivery_date', models.DateField(help_text='Date of delivery')),
                ('baby_name', models.CharField(blank=True, help_text='Full name of the baby', max_length=100, null=True)),
                ('baby_gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True)),
                ('baby_status', models.CharField(choices=[('Alive', 'Alive'), ('Deceased', 'Deceased'), ('Stillborn', 'Stillborn')], default='Alive', help_text="Baby's status", max_length=10)),
                ('mother_death_date', models.DateField(blank=True, help_text="Date of mother's death", null=True)),
                ('cause_of_mother_death', models.TextField(blank=True, help_text="Cause of mother's death", null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='motherdeath',
            name='patient',
        ),
        migrations.DeleteModel(
            name='ChildBirth',
        ),
        migrations.DeleteModel(
            name='MotherDeath',
        ),
    ]
