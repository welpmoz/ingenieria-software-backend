# Generated by Django 4.1.6 on 2023-02-03 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horario',
            name='codigo_curso',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='horario',
            name='dia',
            field=models.CharField(max_length=20),
        ),
    ]