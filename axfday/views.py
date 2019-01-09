from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import View

from .models import *
from .tasks import send_confirm_email
from .utils import *


def home(req):
    # 读取轮播数据
    wheels = MyWheel.objects.all()
    navs = MyNav.objects.all()
    # 必购的数据
    musts = MustBuy.objects.all()
    shops = Shop.objects.all()
    data = {
        "title": "首页",
        "wheels": wheels,
        "navs": navs,
        "musts": musts,
        "shop0": shops[0],
        "shop1_3": shops[1:3],
        "shop3_7": shops[3:7],
        "shop_last": shops[7:],
        "mains": MainShow.objects.all()
    }
    return render(req, 'home/home.html', data)


@login_required(login_url="/axf/login")
def cart(req):
    # 确定用户
    user = req.user
    # 根据用户去购物车表中搜索数据
    data = Cart.objects.filter(user_id=user.id)

    sum_money = get_cart_money(data)
    # 判断全选按钮状态
    if data.exists() and not data.filter(is_selected=False).exists():
        is_all_select = True
    else:
        is_all_select = False
    res = {
        'title': '购物车',
        'uname': user.username,
        'phone': user.phone if user.phone else "暂无",
        'address': user.address if user.address else "暂无",
        'cart_items': data,
        'sum_money': sum_money,
        'is_all_select': is_all_select
    }
    return render(req, 'cart/cart.html', res)


def market(req):
    return redirect(reverse("axf:market_with_params", args=(104749, 0, 1)))


def market_with_params(req, typeid, sub_type_id, sort_type):
    """
        1 综合排序
        2 销量
        3 价格
    :param req:
    :param typeid:
    :param sub_type_id:
    :return:
    """
    sub_type_id = int(sub_type_id)
    # 拿到所有的分类数据
    my_types = GoodsTypes.objects.all()
    # 通过typeid拿商品数据
    my_goods = Goods.objects.filter(
        categoryid=int(typeid)
    )
    # 拿一级分类数据
    current_type = my_types.filter(typeid=typeid).first()
    # 拿二级分类数据
    # result = []
    # sub_types_str = current_type.childtypenames
    # sub_types_array = sub_types_str.split("#")
    # for i in sub_types_array:
    #     tmp = i.split(":")
    #     print(tmp)
    #     result.append(tmp)
    # print(result)
    result = [i.split(":") for i in current_type.childtypenames.split("#")]

    # 通过二级分类数据过滤商品
    result_goods = None
    if sub_type_id == 0:
        result_goods = my_goods
    else:
        result_goods = my_goods.filter(childcid=sub_type_id)
    # 确定数据集以后 做排序

    if sort_type == "2":
        result_goods = result_goods.order_by("productnum")
    elif sort_type == "3":
        result_goods = result_goods.order_by("price")
    else:
        pass

    user = req.user
    if isinstance(user, AxfUser):
        tmp_dict = {}
        cart_nums = Cart.objects.filter(user=user)
        for i in cart_nums:
            tmp_dict[i.goods.id] = i.num
        for i in my_goods:
            i.num = tmp_dict.get(i.id) if tmp_dict.get(i.id) else 0


    data = {
        "title": "闪购",
        "types": my_types,
        "select_type_id": typeid,
        "goods": result_goods,
        "sub_types": result,
        "select_sub_type_id": str(sub_type_id)
    }
    return render(req, 'market/market.html', data)


def mine(req):
    user = req.user
    is_login = False
    username = ""
    u_icon = ""
    btns = MineBtns.objects.all()
    if isinstance(user, AxfUser):
        is_login = True
        username = user.username
        if user.icon:
            u_icon = "http://" + req.get_host() + "/static/uploads/" +user.icon.url
        data = {
            "title": "我的",
            'is_login': is_login,
            'u_name': username,
            'icon': u_icon,
            'btns': btns
        }
        return render(req, 'mine/mine.html', data)
    else:
        data = {
            "title": "我的",
            'is_login': is_login,
            'u_name': username,
            'icon': u_icon,
            'btns': btns
        }
        return render(req, 'mine/mine.html', data)


class RegisterAPI(View):

    def get(self, req):
        return render(req, 'user/register.html')

    def post(self, req):
        params = req.POST
        icon_file = req.FILES.get("icon")
        uname = params.get("uname")
        pwd = params.get("pwd")
        c_pwd = params.get("c_pwd")
        email = params.get("email")

#         开始校验数据
        if uname and len(uname) >= 3:
#             继续校验此用户名是否可用
            if AxfUser.objects.filter(username=uname).exists():
#                 如果查到了数据说明用户名不可用
                return render(req, "user/register.html", {"help_msg": "该用户已存在"})
            else:
                if pwd and len(pwd)>0 and pwd == c_pwd:
#                     创建用户，发送验证邮件
                    user = AxfUser.objects.create_user(
                        username=uname,
                        password=pwd,
                        email=email,
                        is_active=False,
                        icon=icon_file
                    )
#                     发送验证邮件 需要的参数用户
                    if send_confirm_email(user, req.get_host()):
                        return HttpResponse("恭喜您注册成功")
                    else:
                        return HttpResponse("验证邮件发送失败")
                else:
                    return HttpResponse("好好学习，没事别抓人接口")
        else:
            return HttpResponse("好好学习，没事别抓人接口")


class LoginAPI(View):

    def get(self, req):
        return render(req, 'user/login.html')

    def post(self, req):
        params = req.POST
        uname = params.get("uname")
        pwd = params.get("pwd")
#         校验数据
        if uname and pwd and len(uname)>=3 and len(pwd)>0:
            # 校验用户
            user = authenticate(username=uname, password=pwd)
            if user:
                login(req, user)
                return redirect(reverse("axf:mine"))
            else:
                return redirect(reverse("axf:login"))
        else:
            return HttpResponse("别瞎搞")


def confirm(req, random_str):
    # 去那缓存拿数据
    uid = cache.get(random_str)

    if uid:
        # 通过uid找到用户,更新字段
        AxfUser.objects.filter(pk=int(uid)).update(
            is_active=True
        )
        return redirect(reverse("axf:login"))
    else:
        return HttpResponse("验证链接无效")


def logout_api(req):
    logout(req)
    return redirect(reverse("axf:mine"))


def check_uname(req):
    # 解析参数
    uname = req.GET.get("uname")
    data = {
        "code": 1,
        "data": ""
    }
    if uname and len(uname) >= 3:
        if AxfUser.objects.filter(username=uname).exists():
            data["msg"] = "账号已存在"
        else:
            data["msg"] = "账号可用"
    else:
        data["msg"] = "用户名过短"
    return JsonResponse(data)


class CartAPI(View):

    def post(self, req):
        # 查看用户是否登录
        user = req.user
        if not isinstance(user, AxfUser):
            data = {
                "code": 2,
                "msg": "not login",
                "data": "/axf/login"
            }
            return JsonResponse(data)
        # 拿参数
        op_type = req.POST.get('type')
        g_id = int(req.POST.get('g_id'))
        # 获取商品数据
        goods = Goods.objects.get(pk=g_id)
        if op_type == "add":
            goods_num = 1
            # 添加购物车
            if goods.storenums > 1:
                cart_goods = Cart.objects.filter(user=user, goods=goods)
                # 判断购物车是否存在该商品
                if cart_goods.exists():
                    cart_item = cart_goods.first()
                    cart_item.num += 1
                    cart_item.save()
                    # 修改返回的数量
                    goods_num = cart_item.num
                else:
                    Cart.objects.create(
                        user=user,
                        goods=goods
                    )
                data = {
                    "code": 1,
                    "msg": "ok",
                    "data": goods_num
                }
                return JsonResponse(data)
            else:
                data = {
                    "code": 3,
                    "msg": "库存不足",
                    "data": ""
                }
                return JsonResponse(data)

        elif op_type == 'sub':
            goods_num = 0
            # 查看购物车的数据
            cart_item = Cart.objects.get(user=user, goods=goods)
            cart_item.num -= 1
            cart_item.save()

            if cart_item.num == 0:
                cart_item.delete()

            else:
                goods_num = cart_item.num
            data = {
                "code": 1,
                "msg": "ok",
                "data": goods_num
            }
            return JsonResponse(data)


class CartStatusAPI(View):

    def patch(self, req):
        params = QueryDict(req.body)
        c_id = int(params.get('c_id'))
        user = req.user
        # 获取和user有关的购物车数据
        cart_items = Cart.objects.filter(user_id=user.id)

        # 获取c_id对应的数据
        cart_data = cart_items.get(id=c_id)

        # 修改状态 取反
        cart_data.is_selected = not cart_data.is_selected
        cart_data.save()

        # 算钱
        sum_money = get_cart_money(cart_items)

        # 判断是否是全选
        if cart_items.filter(is_selected=False).exists():
            is_all_select = False
        else:
            is_all_select = True
        res = {
            "code": 1,
            "msg": "ok",
            "data": {
                "is_all_select": is_all_select,
                "sum_money": sum_money,
                "status": cart_data.is_selected
            }
        }
        return JsonResponse(res)


class CartAllStatusAPI(View):

    def put(self, req):
        user = req.user
#         判断操作
        cart_items = Cart.objects.filter(user_id=user.id)

        is_all_select = False
        if cart_items.exists() and cart_items.filter(is_selected=False):
            is_all_select = True
            cart_items.filter(is_selected=False).update(is_selected=True)
            # 算钱
            sum_money = get_cart_money(cart_items)

        else:
            cart_items.update(is_selected=False)

            sum_money = 0

        result = {
            "code": 1,
            "msg": "ok",
            "data": {
                "sum_money": sum_money,
                "all_select": is_all_select
            }
        }
        return JsonResponse(result)


class CartItemAPI(View):

    def post(self, req):
        user = req.user
        c_id = req.POST.get("c_id")

#       确定购物车数据
        cart_item = Cart.objects.get(id=int(c_id))

        if cart_item.goods.storenums < 1:
            data = {
                'code': 2,
                "msg": "库存不足",
                "data": ""
            }
            return JsonResponse(data)

        cart_item.num += 1
        cart_item.save()

        # 算钱
        cart_items = Cart.objects.filter(
            user_id=user.id, is_selected=True
        )

        sum_money = get_cart_money(cart_items)

        data = {
            "code": 1,
            "msg": "ok",
            "data": {
                "num": cart_item.num,
                "sum_money": sum_money
            }
        }
        return JsonResponse(data)


    def delete(self, req):
        user = req.user
        c_id = QueryDict(req.body).get("c_id")

        cart_item = Cart.objects.get(pk=int(c_id))

        cart_item.num -= 1
        cart_item.save()

        if cart_item.num == 0:
            goods_num = 0
            cart_item.delete()
        else:
            goods_num = cart_item.num

#             算钱
        cart_items = Cart.objects.filter(user_id=user.id, is_selected=True)

        sum_money = get_cart_money(cart_items)

        data = {
            "code": 1,
            "msg": "ok",
            "data": {
                "num": goods_num,
                "sum_money": sum_money
            }
        }
        return JsonResponse(data)


class OrderAPI(View):

    def get(self, req):
        user = req.user
        cart_items = Cart.objects.filter(user_id=user.id, is_selected=True)

        if not cart_items.exists():
            return render(req, "order/order_detail.html")
        # 创建order
        order = Order.objects.create(
            user=user
        )
        for i in cart_items:
            OrderItem.objects.create(
                order=order,
                goods=i.goods,
                num=i.num,
                buy_money=i.goods.price
            )
        # 算钱
        sum_money = get_cart_money(cart_items)
        # 清空购物车中被选中的商品
        cart_items.delete()

        data = {
            "sum_money": sum_money,
            "order": order
        }
        return render(req, "order/order_detail.html", data)