# Generated by Django 4.1.7 on 2023-04-02 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0013_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(blank=True, db_column='Name', max_length=255, null=True, unique=True),
        ),
    ]
