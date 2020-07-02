# Generated by Django 3.0.7 on 2020-07-02 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'carts',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=0, max_digits=12)),
                ('final_price', models.DecimalField(decimal_places=0, max_digits=12)),
                ('size', models.CharField(max_length=30)),
                ('product_image', models.URLField(max_length=1000)),
                ('quantity', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
    ]
