
from django.urls import path
from . import views as v


urlpatterns = [
    path("", v.index, name="index"),
    path("pcs/", v.products, name="products"),
    path("success/", v.success, name="success"),
    path("cancel/", v.cancel, name="cancel"), 
    path("add/", v.add, name="add"),
    path("addpart/", v.addpart, name="addpart"),
    path("register/", v.register, name="register"),
    path("login/", v.loginPage, name="loginPage"),
    path("account/", v.account, name="account"),
    path("pcs/<slug:slug>/", v.productPage, name="productPage"),
    #("pcs/<slug:slug>/review", v.reviewPage, name="reviewPage"),
    path('stripe_webhook', v.stripe_webhook, name='stripe_webhook'),
]

