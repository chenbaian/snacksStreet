from django.conf.urls import url
from .views import *

app_name = 'axfday'
urlpatterns = [
    url(r"^home$", home, name="home"),
    url(r"^cart$", cart, name="cart"),
    url(r"^market$", market, name="market"),
    url(r"^market_with_params/(\d+)/(\d+)/(\d+)", market_with_params, name="market_with_params"),
    url(r"^mine$", mine, name="mine"),
    url(r"^register$", RegisterAPI.as_view(), name="register"),
    url(r"^login$", LoginAPI.as_view(), name="login"),
    url(r"^confirm/(.*)", confirm),
    url(r"^logout$", logout_api, name="logout"),
    url(r"^check_uname$", check_uname),
    url(r"^cart_api$", CartAPI.as_view()),
    url(r"^cart_status$", CartStatusAPI.as_view()),
    url(r"^cart_all_status$", CartAllStatusAPI.as_view()),
    url(r"^cart_item$", CartItemAPI.as_view()),
    url(r"^order$", OrderAPI.as_view(), name="order")
]