# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddressTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=64)),
                ('addressId', models.CharField(default=b'00000', unique=True, max_length=64)),
                ('contact', models.CharField(max_length=256)),
                ('phoneNumber', models.CharField(max_length=64)),
                ('address', models.TextField()),
                ('defaults', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CollectTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=64)),
                ('collectId', models.CharField(default=b'00000', unique=True, max_length=64)),
                ('goodsId', models.CharField(default=b'00000', unique=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='GoodsTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('goodsName', models.CharField(max_length=256)),
                ('goodsId', models.CharField(default=b'00000', unique=True, max_length=64)),
                ('description', models.TextField()),
                ('price', models.CharField(default=b'00000', max_length=64)),
                ('freightCost', models.CharField(default=b'00000', max_length=64)),
                ('subClass', models.CharField(default=b'common', max_length=64, choices=[(b'common', b'\xe6\x9c\xaa\xe5\xae\x9a\xe4\xb9\x89'), (b'dropLamp', b'\xe5\x90\x8a\xe7\x81\xaf'), (b'deskLamp', b'\xe5\x8f\xb0\xe7\x81\xaf'), (b'parlorLamp', b'\xe5\xae\xa2\xe5\x8e\x85\xe7\x81\xaf'), (b'roomLamp', b'\xe5\x8d\xa7\xe5\xae\xa4\xe7\x81\xaf')])),
                ('saleCount', models.IntegerField(default=0)),
                ('inventoryCount', models.IntegerField(default=0)),
                ('descImageUrl1', models.CharField(max_length=256)),
                ('descImageUrl2', models.CharField(max_length=256)),
                ('descImageUrl3', models.CharField(max_length=256)),
                ('descImageUrl4', models.CharField(max_length=256)),
                ('descImageUrl5', models.CharField(max_length=256)),
                ('descImageUrl6', models.CharField(max_length=256)),
                ('descImageUrl7', models.CharField(max_length=256)),
                ('descImageUrl8', models.CharField(max_length=256)),
                ('descImageUrl9', models.CharField(max_length=256)),
                ('descImageUrl10', models.CharField(max_length=256)),
                ('aboutImageUrl', models.CharField(max_length=256)),
                ('remarkImageUrl', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='ManagerOrderTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=64)),
                ('orderId', models.CharField(max_length=64)),
                ('goodsId', models.CharField(default=b'00000', unique=True, max_length=64)),
                ('addressId', models.CharField(default=b'00000', unique=True, max_length=64)),
                ('count', models.IntegerField(default=0)),
                ('sumPrice', models.CharField(max_length=64)),
                ('totalPrice', models.CharField(max_length=64)),
                ('status', models.CharField(default=b'new', max_length=64, choices=[(b'new', b'\xe6\x96\xb0\xe8\xae\xa2\xe5\x8d\x95'), (b'process', b'\xe5\xb7\xb2\xe5\x8f\x91\xe8\xb4\xa7'), (b'ok', b'\xe5\xb7\xb2\xe6\x88\x90\xe4\xba\xa4'), (b'cancel', b'\xe5\xb7\xb2\xe5\x8f\x96\xe6\xb6\x88'), (b'ruturnGoods', b'\xe8\xaf\xb7\xe6\xb1\x82\xe9\x80\x80\xe8\xb4\xa7'), (b'ruturnGoodsing', b'\xe9\x80\x80\xe8\xb4\xa7\xe4\xb8\xad'), (b'ruturnGoodsed', b'\xe5\xb7\xb2\xe9\x80\x80\xe8\xb4\xa7')])),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCartTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=64)),
                ('goodsId', models.CharField(default=b'00000', unique=True, max_length=64)),
                ('count', models.IntegerField(default=0)),
                ('sumPrice', models.CharField(max_length=64)),
                ('isSelect', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserOrderTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=64)),
                ('orderId', models.CharField(max_length=64)),
                ('goodsId', models.CharField(default=b'00000', unique=True, max_length=64)),
                ('addressId', models.CharField(default=b'00000', unique=True, max_length=64)),
                ('count', models.IntegerField(default=0)),
                ('sumPrice', models.CharField(max_length=64)),
                ('totalPrice', models.CharField(max_length=64)),
                ('status', models.CharField(default=b'new', max_length=64, choices=[(b'new', b'\xe6\x96\xb0\xe8\xae\xa2\xe5\x8d\x95'), (b'process', b'\xe5\xb7\xb2\xe5\x8f\x91\xe8\xb4\xa7'), (b'ok', b'\xe5\xb7\xb2\xe6\x88\x90\xe4\xba\xa4'), (b'cancel', b'\xe5\xb7\xb2\xe5\x8f\x96\xe6\xb6\x88'), (b'ruturnGoods', b'\xe8\xaf\xb7\xe6\xb1\x82\xe9\x80\x80\xe8\xb4\xa7'), (b'ruturnGoodsing', b'\xe9\x80\x80\xe8\xb4\xa7\xe4\xb8\xad'), (b'ruturnGoodsed', b'\xe5\xb7\xb2\xe9\x80\x80\xe8\xb4\xa7')])),
            ],
        ),
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('iconUrl', models.CharField(max_length=256)),
                ('nickname', models.CharField(max_length=256)),
                ('sex', models.CharField(default=b'undefine', max_length=64, choices=[(b'undefine', b'\xe6\x9c\xaa\xe5\xae\x9a\xe4\xb9\x89'), (b'male', b'\xe7\x94\xb7'), (b'female', b'\xe5\xa5\xb3')])),
                ('vip', models.BooleanField(default=False)),
                ('level', models.IntegerField(default=0)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
