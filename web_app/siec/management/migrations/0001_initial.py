# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EquipoDeComputo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('marca', models.CharField(max_length=100)),
                ('modelo', models.CharField(max_length=100)),
                ('estado', models.PositiveSmallIntegerField(verbose_name=b'estado')),
                ('ubicacion', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(verbose_name=b'fecha de publicacion')),
                ('estado', models.PositiveSmallIntegerField(verbose_name=b'estado')),
                ('equipodecomputo', models.ForeignKey(to='management.EquipoDeComputo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reparacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(verbose_name=b'fecha de publicacion')),
                ('motivo', models.CharField(max_length=800)),
                ('descipcion', models.CharField(max_length=800)),
                ('equipodecomputo', models.ForeignKey(to='management.EquipoDeComputo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='equipodecomputo',
            name='tipo',
            field=models.ForeignKey(to='management.Tipo'),
            preserve_default=True,
        ),
    ]
