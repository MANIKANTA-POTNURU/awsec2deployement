# Generated by Django 4.2.2 on 2023-06-27 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.CharField(max_length=30)),
                ('pid', models.IntegerField(max_length=10)),
            ],
            options={
                'db_table': 'cart_table',
            },
        ),
    ]
