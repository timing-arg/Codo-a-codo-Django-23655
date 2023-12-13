# Generated by Django 4.2.4 on 2023-10-19 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_docente_delete_persona_alter_estudiante_legajo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docente',
            name='dni',
            field=models.IntegerField(unique=True, verbose_name='Dni'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='dni',
            field=models.IntegerField(unique=True, verbose_name='Dni'),
        ),
    ]
