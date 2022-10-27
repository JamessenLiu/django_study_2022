# Generated by Django 2.1.12 on 2022-10-27 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.IntegerField()),
                ('updated_at', models.IntegerField()),
                ('format_created_at', models.DateTimeField(auto_now=True)),
                ('format_updated_at', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=200, null=True)),
                ('last_name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('gender', models.SmallIntegerField(choices=[(0, 'FEMALE'), (1, 'MALE'), (2, 'LADYBOY')])),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
