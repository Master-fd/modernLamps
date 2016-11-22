#coding: utf8

from django.db import models

# Create your models here.
#用户表
class UsersTable(models.Model):
    account = models.CharField(unique=True, blank=False, max_length=64);
    password = models.CharField(blank=False, max_length=64);
    iconUrl = models.CharField(max_length=256);
    nickname = models.CharField(max_length=256);
    sex_choices = (("undefine", u"未定义"),
                   ("male", u"男"),
                ("female", u"女"));
    sex = models.CharField(max_length=64, choices=sex_choices, default=sex_choices[0][0]);
    vip = models.BooleanField(default=False);
    level = models.IntegerField(default=0);
    createDate = models.DateTimeField(auto_now_add=True);
    updateDate = models.DateTimeField(auto_now=True);
    email = models.EmailField();
    superUser = models.BooleanField(default=False);  #管理员用户

#地址表
class AddressTable(models.Model):
    account = models.CharField(blank=False, max_length=64);  #账户
    addressId = models.CharField(unique=True, max_length=64, default='00000');  #地址id
    contact = models.CharField(blank=False, max_length=256);  #联系人
    phoneNumber = models.CharField(blank=False, max_length=64);  #电话
    address = models.TextField(blank=False);           #详细地址
    defaults = models.BooleanField(default=False);     #默认地址

#收藏表
class CollectTable(models.Model):
    account = models.CharField(blank=False, max_length=64);  #账户
    collectId = models.CharField(unique=True, max_length=64, default='00000');  #收藏id
    goodsId = models.CharField(max_length=64, default='00000');  #商品id

#购物车表
class ShoppingCartTable(models.Model):
    account = models.CharField(blank=False, max_length=64);
    goodsId = models.CharField(max_length=64, default='00000');  #商品id
    count = models.IntegerField(default=0);
    sumPrice = models.CharField(max_length=64);   #小计
    isSelect = models.BooleanField(default=True);

#订单表，只有增加和删除
class OrderTable(models.Model):
    account = models.CharField(blank=False, max_length=64);  #账户
    orderId = models.CharField(max_length=64);  #订单id,一个订单有多个商品，采用order id来归类同一个订单
    goodsId = models.CharField(max_length=64, default='00000');  #商品id
    count = models.IntegerField(default=0);
    sumPrice = models.CharField(max_length=64);   #小计

#用户订单表,由用户控制删除
class UserOrderTable(models.Model):
    account = models.CharField(blank=False, max_length=64);  #账户
    orderId = models.CharField(unique=True, max_length=64);  #订单id,一个订单有多个商品，采用order id来归类同一个订单
    totalPrice = models.CharField(max_length=64);  #订单总价
    contact = models.CharField(blank=False, max_length=256);  #联系人
    phoneNumber = models.CharField(blank=False, max_length=64);  #电话
    address = models.TextField(blank=False);           #详细地址
    status_choices = (("undefine", u"未定义"),
                      ("new", u"新订单"),    #新订单
                    ("process", u"已发货"),    #已发货
                    ("ok", u"已成交"),         #已结束
                      ("cancel", u"已取消"),
                      ("ruturnGoods", u'请求退货'),
                      ("ruturnGoodsing", u'退货中'),
                      ("ruturnGoodsed", u'已退货'),);
    status = models.CharField(choices=status_choices, default=status_choices[0][0], max_length=64);   #订单状态
    company = models.CharField(max_length=64);   #快递公司
    expressId = models.CharField(max_length=128); #快递单号
    userDelete = models.BooleanField(default=False);   #用户是否删除了订单
    managerDelete = models.BooleanField(default=False);   #管理员是否删除,只有两个都删除了才是真的删除
    createDate = models.DateTimeField(auto_now_add=True);
    updateDate = models.DateTimeField(auto_now=True);

#管理员订单表,由管理控制删除
class ManagerOrderTable(models.Model):
    account = models.CharField(blank=False, max_length=64);  #账户
    orderId = models.CharField(unique=True, max_length=64);  #订单id,一个订单有多个商品，采用order id来归类同一个订单
    totalPrice = models.CharField(max_length=64);  #订单总价
    contact = models.CharField(blank=False, max_length=256);  #联系人
    phoneNumber = models.CharField(blank=False, max_length=64);  #电话
    address = models.TextField(blank=False);           #详细地址
    status_choices = (("undefine", u"未定义"),
                      ("new", u"新订单"),    #新订单
                    ("process", u"已发货"),    #已发货
                    ("ok", u"已成交"),         #已结束
                      ("cancel", u"已取消"),
                      ("ruturnGoods", u'请求退货'),
                      ("ruturnGoodsing", u'退货中'),
                      ("ruturnGoodsed", u'已退货'),);
    status = models.CharField(choices=status_choices, default=status_choices[0][0], max_length=64);   #订单状态
    company = models.CharField(max_length=64);   #快递公司
    expressId = models.CharField(max_length=128); #快递单号
    createDate = models.DateTimeField(auto_now_add=True);
    updateDate = models.DateTimeField(auto_now=True);

#商品表
class GoodsTable(models.Model):
    goodsName = models.CharField(max_length=256);   #商品名称
    goodsId = models.CharField(unique=True, max_length=64, default='00000');  #商品id
    goodsDescUrl = models.CharField(max_length=256);  #商品详情url
    description = models.TextField(); #描述
    price = models.CharField(max_length=64, default='0');   #价格max_digits最大多少位，decimal_places最大小数位多少位
    freightCost = models.CharField(max_length=64, default='0');   #运费
    subClass_choices = (("undefine", u"未定义"),
                         ("dropLamp", u"吊灯"),
                         ('deskLamp', u"台灯"),
                         ('parlorLamp', u"客厅灯"),
                        ('roomLamp', u"餐厅灯"));
    subClass = models.CharField(choices=subClass_choices, default=subClass_choices[0][0], max_length=64);   #分类
    saleCount = models.IntegerField(default=0);   #销量
    inventoryCount = models.IntegerField(default=0);      #库存

    #image url
    minImageUrl1 = models.CharField(max_length=256, blank=True);
    minImageUrl2 = models.CharField(max_length=256, blank=True);
    minImageUrl3 = models.CharField(max_length=256, blank=True);
    descImageUrl1 = models.CharField(max_length=256, blank=True);
    descImageUrl2 = models.CharField(max_length=256, blank=True);
    descImageUrl3 = models.CharField(max_length=256, blank=True);
    descImageUrl4 = models.CharField(max_length=256, blank=True);
    descImageUrl5 = models.CharField(max_length=256, blank=True);
    descImageUrl6 = models.CharField(max_length=256, blank=True);
    descImageUrl7 = models.CharField(max_length=256, blank=True);
    descImageUrl8 = models.CharField(max_length=256, blank=True);
    descImageUrl9 = models.CharField(max_length=256, blank=True);
    descImageUrl10 = models.CharField(max_length=256, blank=True);
    aboutImageUrl = models.CharField(max_length=256, blank=True);
    remarkImageUrl = models.CharField(max_length=256, blank=True);


