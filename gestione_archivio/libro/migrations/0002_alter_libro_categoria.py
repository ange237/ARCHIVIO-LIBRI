# Generated by Django 5.2.1 on 2025-05-16 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='categoria',
            field=models.CharField(choices=[('ROMANZO', 'romanzo'), ('FANTASCIENZA', 'fantascienza'), ('BD', 'bd'), ('HOROR', 'horor'), ('ALTRO', 'altro')], default='', max_length=12),
        ),
    ]
