# Generated by Django 5.2 on 2025-06-14 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulador', '0002_rename_mail_solicitudes_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=320)),
                ('celular', models.CharField(max_length=25)),
                ('mensaje', models.TextField()),
            ],
            options={
                'db_table': 'consultas',
            },
        ),
    ]
