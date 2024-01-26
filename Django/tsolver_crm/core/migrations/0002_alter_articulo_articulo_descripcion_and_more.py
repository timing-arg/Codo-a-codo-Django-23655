# Generated by Django 4.2.6 on 2024-01-25 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='articulo_descripcion',
            field=models.CharField(max_length=250, unique=True, verbose_name='Descripción del artículo'),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='familia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.familia'),
        ),
        migrations.AlterField(
            model_name='familia',
            name='nombre',
            field=models.CharField(max_length=250, unique=True, verbose_name='Descripción de la familia'),
        ),
        migrations.AlterField(
            model_name='material',
            name='articulo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.articulo'),
        ),
        migrations.AlterField(
            model_name='material',
            name='material',
            field=models.CharField(max_length=250, unique=True, verbose_name='Descripción del material'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='articulo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.articulo'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=models.CharField(max_length=250, unique=True, verbose_name='Descripción del producto'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='idcliente',
            field=models.IntegerField(null=True, verbose_name='IdCliente'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.material'),
        ),
    ]
