# Generated by Django 5.2.1 on 2025-05-18 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libro', '0004_alter_libro_anno_pubblicazione'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='descrizione',
            field=models.TextField(blank=True, null=True),
        ),
    ]
