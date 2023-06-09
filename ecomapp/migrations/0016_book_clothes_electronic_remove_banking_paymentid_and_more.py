# Generated by Django 4.1.7 on 2023-04-07 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0015_product_codeproduct_alter_product_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('numpage', models.IntegerField(blank=True, db_column='Page', null=True)),
                ('author', models.CharField(blank=True, db_column='Author', max_length=255, null=True)),
                ('productid', models.OneToOneField(db_column='ProductID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='ecomapp.product')),
                ('genre', models.CharField(blank=True, db_column='Genre', max_length=255, null=True)),
            ],
            options={
                'db_table': 'book',
            },
        ),
        migrations.CreateModel(
            name='Clothes',
            fields=[
                ('clothtype', models.CharField(blank=True, db_column='ClothType', max_length=255, null=True)),
                ('color', models.CharField(blank=True, db_column='Color', max_length=255, null=True)),
                ('gender', models.CharField(blank=True, db_column='Gender', max_length=255, null=True)),
                ('brand', models.CharField(blank=True, db_column='Brand', max_length=255, null=True)),
                ('material', models.CharField(blank=True, db_column='Material', max_length=255, null=True)),
                ('productid', models.OneToOneField(db_column='ProductID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='ecomapp.product')),
            ],
            options={
                'db_table': 'clothes',
            },
        ),
        migrations.CreateModel(
            name='Electronic',
            fields=[
                ('devicetype', models.CharField(blank=True, db_column='DeviceType', max_length=255, null=True)),
                ('color', models.CharField(blank=True, db_column='Color', max_length=255, null=True)),
                ('brand', models.CharField(blank=True, db_column='Brand', max_length=255, null=True)),
                ('weight', models.CharField(blank=True, db_column='Weight', max_length=255, null=True)),
                ('power', models.CharField(blank=True, db_column='Power', max_length=255, null=True)),
                ('size', models.CharField(blank=True, db_column='Size', max_length=255, null=True)),
                ('productid', models.OneToOneField(db_column='ProductID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='ecomapp.product')),
            ],
            options={
                'db_table': 'electronic',
            },
        ),
        migrations.RemoveField(
            model_name='banking',
            name='paymentid',
        ),
        migrations.RemoveField(
            model_name='cash',
            name='paymentid',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.RemoveField(
            model_name='membershiptype',
            name='customerid',
        ),
        migrations.RemoveField(
            model_name='message',
            name='messagesessionid',
        ),
        migrations.RemoveField(
            model_name='messagesession',
            name='customerid',
        ),
        migrations.RemoveField(
            model_name='messagesession',
            name='salesstaffuserid',
        ),
        migrations.RemoveField(
            model_name='prodimage',
            name='productid',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='itemid',
        ),
        migrations.RemoveField(
            model_name='qrcode',
            name='paymentid',
        ),
        migrations.RemoveField(
            model_name='shippinginfo',
            name='orderid',
        ),
        migrations.RemoveField(
            model_name='order',
            name='taxid',
        ),
        migrations.RemoveField(
            model_name='order',
            name='voucherid',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='note',
        ),
        migrations.AddField(
            model_name='customer',
            name='typecustomer',
            field=models.CharField(blank=True, db_column='TypeCustomer', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='date_shipping',
            field=models.DateField(blank=True, db_column='DateShipping', null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='delayshipnote',
            field=models.CharField(blank=True, db_column='DelayShipNote', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='shippingaddressid',
            field=models.ForeignKey(blank=True, db_column='ShippingAddressID', null=True, on_delete=django.db.models.deletion.CASCADE, to='ecomapp.shippingaddress'),
        ),
        migrations.AddField(
            model_name='order',
            name='shippingmethod',
            field=models.CharField(blank=True, db_column='ShippingMethod', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='phonenumber_receive',
            field=models.CharField(blank=True, db_column='PhoneNumberReceive', max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='Banking',
        ),
        migrations.DeleteModel(
            name='Cash',
        ),
        migrations.DeleteModel(
            name='Membershiptype',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Messagesession',
        ),
        migrations.DeleteModel(
            name='Prodimage',
        ),
        migrations.DeleteModel(
            name='Promotion',
        ),
        migrations.DeleteModel(
            name='Qrcode',
        ),
        migrations.DeleteModel(
            name='Shippinginfo',
        ),
        migrations.DeleteModel(
            name='Tax',
        ),
        migrations.DeleteModel(
            name='Voucher',
        ),
    ]
