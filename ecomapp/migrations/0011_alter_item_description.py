# Generated by Django 4.1.7 on 2023-04-02 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0010_alter_product_manufacturingyear'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.CharField(blank=True, db_column='Description', max_length=2000, null=True),
        ),
    ]
