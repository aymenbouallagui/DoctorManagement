# Generated by Django 3.0.4 on 2021-07-04 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordannance',
            name='medicaments',
            field=models.ManyToManyField(blank=True, to='Doctor.medicaments'),
        ),
        migrations.DeleteModel(
            name='medicaments_ord',
        ),
    ]