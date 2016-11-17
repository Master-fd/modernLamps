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
                ('goodsId', models.CharField(default=b'00000', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='GoodsTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('goodsName', models.CharField(max_length=256)),
                ('goodsId', models.CharField(default=b'00000', unique=True, max_length=64)),
                ('goodsDescUrl', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('price', models.CharField(default=b'0', max_length=64)),
                ('freightCost', models.CharField(default=b'0', max_length=64)),
                ('subClass', models.CharField(default=b'undefine', max_length=64, choices=[(b'undefine', '\u672a\u5b9a\u4e49'), (b'dropLamp', '\u540a\u706f'), (b'deskLamp', '\u53f0\u706f'), (b'parlorLamp', '\u5ba2\u5385\u706f'), (b'roomLamp', '\u9910\u5385\u706f')])),
                ('saleCount', models.IntegerField(default=0)),
                ('inventoryCount', models.IntegerField(default=0)),
                ('minImageUrl1', models.CharField(max_length=256, blank=True)),
                ('minImageUrl2', models.CharField(max_length=256, blank=True)),
                ('minImageUrl3', models.CharField(max_length=256, blank=True)),
                ('descImageUrl1', models.CharField(max_length=256, blank=True)),
                ('descImageUrl2', models.CharField(max_length=256, blank=True)),
                ('descImageUrl3', models.CharField(max_length=256, blank=True)),
                ('descImageUrl4', models.CharField(max_length=256, blank=True)),
                ('descImageUrl5', models.CharField(max_length=256, blank=True)),
                ('descImageUrl6', models.CharField(max_length=256, blank=True)),
                ('descImageUrl7', models.CharField(max_length=256, blank=True)),
                ('descImageUrl8', models.CharField(max_length=256, blank=True)),
                ('descImageUrl9', models.CharField(max_length=256, blank=True)),
                ('descImageUrl10', models.CharField(max_length=256, blank=True)),
                ('aboutImageUrl', models.CharField(max_length=256, blank=True)),
                ('remarkImageUrl', models.CharField(max_length=256, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ManagerOrderTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=64)),
                ('orderId', models.CharField(unique=True, max_length=64)),
                ('totalPrice', models.CharField(max_length=64)),
                ('contact', models.CharField(max_length=256)),
                ('phoneNumber', models.CharField(max_length=64)),
                ('address', models.TextField()),
                ('status', models.CharField(default=b'undefine', max_length=64, choices=[(b'undefine', '\u672a\u5b9a\u4e49'), (b'new', '\u65b0\u8ba2\u5355'), (b'process', '\u5df2\u53d1\u8d27'), (b'ok', '\u5df2\u6210\u4ea4'), (b'cancel', '\u5df2\u53d6\u6d88'), (b'ruturnGoods', '\u8bf7\u6c42\u9000\u8d27'), (b'ruturnGoodsing', '\u9000\u8d27\u4e2d'), (b'ruturnGoodsed', '\u5df2\u9000\u8d27')])),
                ('company', models.CharField(max_length=64)),
                ('expressId', models.CharField(max_length=128)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=64)),
                ('orderId', models.CharField(max_length=64)),
                ('goodsId', models.CharField(default=b'00000', max_length=64)),
                ('count', models.IntegerField(default=0)),
                ('sumPrice', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCartTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=64)),
                ('goodsId', models.CharField(default=b'00000', max_length=64)),
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
                ('orderId', models.CharField(unique=True, max_length=64)),
                ('totalPrice', models.CharField(max_length=64)),
                ('contact', models.CharField(max_length=256)),
                ('phoneNumber', models.CharField(max_length=64)),
                ('address', models.TextField()),
                ('status', models.CharField(default=b'undefine', max_length=64, choices=[(b'undefine', '\u672a\u5b9a\u4e49'), (b'new', '\u65b0\u8ba2\u5355'), (b'process', '\u5df2\u53d1\u8d27'), (b'ok', '\u5df2\u6210\u4ea4'), (b'cancel', '\u5df2\u53d6\u6d88'), (b'ruturnGoods', '\u8bf7\u6c42\u9000\u8d27'), (b'ruturnGoodsing', '\u9000\u8d27\u4e2d'), (b'ruturnGoodsed', '\u5df2\u9000\u8d27')])),
                ('company', models.CharField(max_length=64)),
                ('expressId', models.CharField(max_length=128)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UsersTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(unique=True, max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('iconUrl', models.CharField(max_length=256)),
                ('nickname', models.CharField(max_length=256)),
                ('sex', models.CharField(default=b'undefine', max_length=64, choices=[(b'undefine', '\u672a\u5b9a\u4e49'), (b'male', '\u7537'), (b'female', '\u5973')])),
                ('vip', models.BooleanField(default=False)),
                ('level', models.IntegerField(default=0)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254)),
                ('superUser', models.BooleanField(default=False)),
            ],
        ),
    ]
