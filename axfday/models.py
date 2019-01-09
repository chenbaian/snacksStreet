from django.contrib.auth.models import AbstractUser
from django.db import models
from .choices import PERMISSION, ORDER_STATUS


# Create your models here.

class AxfUser(AbstractUser):
    phone = models.CharField(
        verbose_name="手机号",
        max_length=12,
        null=True
    )
    address = models.CharField(
        verbose_name="地址",
        max_length=200,
        null=True
    )
    permission = models.IntegerField(
        verbose_name="权限",
        choices=PERMISSION,
        default=1
    )
    icon = models.ImageField(
        upload_to="icons"
    )

#  axf_wheel(img,name,trackid)
class BaseData(models.Model):
    img = models.CharField(
        max_length=255
    )
    name = models.CharField(
        max_length=40
    )
    trackid = models.CharField(
        max_length=10
    )

    class Meta:
        abstract = True

class MyWheel(BaseData):

    class Meta:
        db_table = "axf_wheel"


class MyNav(BaseData):

    class Meta:
        db_table = "axf_nav"


class MustBuy(BaseData):

    class Meta:
        db_table = "axf_mustbuy"


class Shop(BaseData):

    class Meta:
        db_table = "axf_shop"

# axf_mainshow(
# trackid,name,img,categoryid,brandname,
# img1,childcid1,productid1,longname1,price1,marketprice1,
# img2,childcid2,productid2,longname2,price2,marketprice2,
# img3,childcid3,productid3,longname3,price3,marketprice3)
# values("
# 21782","方便速食","http://img01.bqstatic.com//upload/activity/2017031018205492.jpg@90Q.jpg","103532","爱鲜蜂","http://img01.bqstatic.com/upload/goods/201/701/1916/20170119164159_996462.jpg@200w_200h_90Q","103533","118824","爱鲜蜂·特小凤西瓜1.5-2.5kg/粒","25.80","25.8","http://img01.bqstatic.com/upload/goods/201/611/1617/20161116173544_219028.jpg@200w_200h_90Q","103534","116950","蜂觅·越南直采红心火龙果350-450g/盒","15.3","15.8","http://img01.bqstatic.com/upload/goods/201/701/1916/20170119164119_550363.jpg@200w_200h_90Q","103533","118826","爱鲜蜂·海南千禧果400-450g/盒","9.9","13.8");
class MainShow(BaseData):
    categoryid = models.CharField(
        max_length=100
    )
    brandname = models.CharField(
        max_length=100
    )

    img1 = models.CharField(
        max_length=255
    )
    childcid1 = models.CharField(
        max_length=100
    )
    productid1 = models.CharField(
        max_length=100
    )
    longname1 = models.CharField(
        max_length=100
    )
    price1 = models.CharField(
        max_length=100
    )
    marketprice1 = models.CharField(
        max_length=100
    )

    img2 = models.CharField(
        max_length=255
    )
    childcid2 = models.CharField(
        max_length=100
    )
    productid2 = models.CharField(
        max_length=100
    )
    longname2 = models.CharField(
        max_length=100
    )
    price2 = models.CharField(
        max_length=100
    )
    marketprice2 = models.CharField(
        max_length=100
    )
    img3 = models.CharField(
        max_length=255
    )
    childcid3 = models.CharField(
        max_length=100
    )
    productid3 = models.CharField(
        max_length=100
    )
    longname3 = models.CharField(
        max_length=100
    )
    price3 = models.CharField(
        max_length=100
    )
    marketprice3 = models.CharField(
        max_length=100
    )

    class Meta:
        db_table = "axf_mainshow"


class Goods(models.Model):
    productid = models.CharField(
        max_length=20
    )
    productimg = models.CharField(
        max_length=200
    )
    productname = models.CharField(
        max_length=200,
        null=True
    )
    productlongname = models.CharField(
        max_length=200
    )
    isxf = models.BooleanField(
        default=0
    )
    pmdesc = models.BooleanField(
        default=0
    )
    specifics = models.CharField(
        max_length=20
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    marketprice = models.FloatField()
    categoryid = models.IntegerField()
    childcid = models.IntegerField()
    childcidname = models.CharField(
        max_length=10
    )
    dealerid = models.CharField(
        max_length=20
    )
    storenums = models.IntegerField()
    productnum = models.IntegerField()

    def __str__(self):
        return str(self.price)

    class Meta:
        db_table = "axf_goods"


class GoodsTypes(models.Model):
    typeid = models.CharField(
        max_length=40
    )
    typename = models.CharField(
        max_length=10
    )
    childtypenames = models.CharField(
        max_length=200,
    )
    typesort = models.IntegerField()

    class Meta:
        db_table = "axf_foodtypes"


class Cart(models.Model):
    user = models.ForeignKey(
        AxfUser,
        on_delete=models.CASCADE
    )

    goods = models.ForeignKey(
        Goods,
        on_delete=models.CASCADE
    )

    num = models.IntegerField(
        default=1
    )

    create_time = models.DateTimeField(
        auto_now_add=True
    )

    update_time = models.DateTimeField(
        auto_now=True
    )

    is_selected = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = '购物车'
        index_together = ['user', 'goods']


class MineBtns(models.Model):
    btn = models.CharField(
        max_length=30
    )

    class_name = models.CharField(
        max_length=100
    )

    bref_url = models.CharField(
        max_length=255,
        null=True
    )

    class Meta:
        verbose_name = '我的页面的下一排按钮'


class Order(models.Model):

    user = models.ForeignKey(
        AxfUser,
        on_delete=models.CASCADE
    )

    create_time = models.DateTimeField(
        auto_now_add=True
    )
    status = models.IntegerField(
        choices=ORDER_STATUS,
        default=1
    )


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    goods = models.ForeignKey(
        Goods,
        on_delete=models.CASCADE
    )

    num = models.IntegerField(
        verbose_name="数量"
    )

    buy_money = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
