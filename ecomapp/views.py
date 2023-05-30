from cgitb import reset
import email
from pickle import GET
from tkinter import N
from tracemalloc import start
# from turtle import position
from unicodedata import name
from unittest import mock
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from .utils import password_reset_token
from django.core.mail import send_mail
from django.http import JsonResponse, HttpRequest, HttpResponse, StreamingHttpResponse

from django.conf import settings
from django.db.models import Q
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User

import datetime as dt
import random
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.ticker as ticker
from docxtpl import DocxTemplate, InlineImage
import os
from django.db import connection
from docx.shared import Mm

import openpyxl
from openpyxl.styles import Alignment
from openpyxl.styles import Alignment, Border, Side


#----------------CUSTOMER--------------------#

#Lấy thông tin Cart hiện tại
class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = get_object_or_404(Shoppingcart, id=cart_id)
            if request.user.is_authenticated and request.user.account:
                cart_obj.customerid = Customer.objects.get(userid__accountid = self.request.user.account)
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)

#Kiểm tra đăng nhập
class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = request.user).exists() and Users.objects.filter(accountid__user = request.user, is_active = True).exists():
            pass
        else:
            return redirect("/login")
        return super().dispatch(request, *args, **kwargs)

# Trang chủ -> tất cả sản phẩm, thông tin mặt hàng yêu thích ( tym tại các sản phẩm)
class HomeView(EcomMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Item.objects.all().order_by("-id")
        paginator = Paginator(all_products, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        if self.request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = self.request.user).exists():
            customer = Customer.objects.get(userid__accountid__user = self.request.user)
            if Wishlist.objects.filter(customerid = customer).exists():
                wishlist = Wishlist.objects.get(customerid = customer)
                wishListItem = [wishlistline.itemid for wishlistline in Wishlistline.objects.filter(wishlistid = wishlist)]
                context['wishListItem'] = wishListItem
            else:
                wishList = Wishlist.objects.create(customerid = customer)
                wishList.save()
                context['wishListItem'] = []
        return context

#Cập nhật danh sách yêu thích
class UpdateToWishList(LoginRequiredMixin,EcomMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        action = self.request.GET.get("action")
        pro_id = self.kwargs["pro_id"]
        all_products = Item.objects.all().order_by("-id")
        paginator = Paginator(all_products, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        if self.request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = self.request.user).exists():
            item = Item.objects.get(id = pro_id)
            customer = Customer.objects.get(userid__accountid__user = self.request.user)
            wishlist = Wishlist.objects.get(customerid = customer)
            if action == "add":
                wishlistline = Wishlistline.objects.create(wishlistid = wishlist, itemid = item)
                wishlistline.save()
            else:
                wishlistline = Wishlistline.objects.filter(wishlistid = wishlist, itemid = item)
                for line in wishlistline:
                    line.delete()
                # wishlistline.delete()
            wishListItem = [wishlistline.itemid for wishlistline in Wishlistline.objects.filter(wishlistid = wishlist)]
            context['wishListItem'] = wishListItem

        return context


# class AllProductsView(EcomMixin, TemplateView):
#     template_name = "allproducts.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['allcategories'] = Category.objects.all()
#         return context

#Danh sách sản phẩm Sách
class BookProductsView(EcomMixin, TemplateView):
    template_name = "bookproducts.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Book.objects.count()>0:
            productbook = Product.objects.filter(type ="Book").order_by("-id")
            allbook =[]
            for book in productbook:
                itembook = Item.objects.get(productid = book)
                allbook.append(itembook)
        else:
            allbook = []
        paginator = Paginator(allbook, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        print(product_list)
        if self.request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = self.request.user).exists():
            customer = Customer.objects.get(userid__accountid__user = self.request.user)
            if Wishlist.objects.filter(customerid = customer).exists():
                wishlist = Wishlist.objects.get(customerid = customer)
                wishListItem = [wishlistline.itemid for wishlistline in Wishlistline.objects.filter(wishlistid = wishlist)]
                context['wishListItem'] = wishListItem
            else:
                wishList = Wishlist.objects.create(customerid = customer)
                wishList.save()
                context['wishListItem'] = []
        context['product_list'] =  product_list
        return context

# Danh sách sản phẩm đồ điện tử
class ElectronicProductsView(EcomMixin, TemplateView):
    template_name = "electronicproducts.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Electronic.objects.count()>0:
            productelectronic = Product.objects.filter(type ="Electronic").order_by("-id")
            allelectronic =[]
            for electronic in productelectronic:
                itemelectronic = Item.objects.get(productid = electronic)
                allelectronic.append(itemelectronic)
        else:
            allelectronic = []
        paginator = Paginator(allelectronic, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        if self.request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = self.request.user).exists():
            customer = Customer.objects.get(userid__accountid__user = self.request.user)
            if Wishlist.objects.filter(customerid = customer).exists():
                wishlist = Wishlist.objects.get(customerid = customer)
                wishListItem = [wishlistline.itemid for wishlistline in Wishlistline.objects.filter(wishlistid = wishlist)]
                context['wishListItem'] = wishListItem
            else:
                wishList = Wishlist.objects.create(customerid = customer)
                wishList.save()
                context['wishListItem'] = []
        context['product_list'] =  product_list
        return context

# Danh sách sản phẩm Quần áo
class ClothesProductsView(EcomMixin, TemplateView):
    template_name = "clothesproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Clothes.objects.count()>0:
            productclothes = Product.objects.filter(type ="Clothes").order_by("-id")
            allclothes =[]
            for clothes in productclothes:
                itemclothes = Item.objects.get(productid = clothes)
                allclothes.append(itemclothes)
        else: 
            allclothes = []
        paginator = Paginator(allclothes, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        if self.request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = self.request.user).exists():
            customer = Customer.objects.get(userid__accountid__user = self.request.user)
            if Wishlist.objects.filter(customerid = customer).exists():
                wishlist = Wishlist.objects.get(customerid = customer)
                wishListItem = [wishlistline.itemid for wishlistline in Wishlistline.objects.filter(wishlistid = wishlist)]
                context['wishListItem'] = wishListItem
            else:
                wishList = Wishlist.objects.create(customerid = customer)
                wishList.save()
                context['wishListItem'] = []
        context['product_list'] =  product_list
        return context

#Chỉnh sửa thông tin cá nhân khách hàng
class EditProfileView(View):
    template_name = "customerprofileedit.html"
    def get(self, request, *args, **kwargs):
        form = EditProfileForm()
        usr_id = kwargs['usr_id']
        user = Users.objects.get(id = usr_id)
        form.fields['username'].initial  = user.accountid.user.username
        form.fields['phonenumber'].initial  = user.contactinfoid.phonenumber
        form.fields['email'].initial  = user.contactinfoid.email
        form.fields['full_name'].initial  = user.fullnameid.fullname
        form.fields['city'].initial  = user.addressid.city
        form.fields['district'].initial  = user.addressid.district
        form.fields['subdistrict'].initial  = user.addressid.subdistrict
        form.fields['street'].initial  = user.addressid.street
        form.fields['description'].initial  = user.addressid.description
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = EditProfileForm(data=request.POST)
        if form.is_valid():
            usr_id = kwargs['usr_id']
            user = Users.objects.get(id = usr_id)
            username = form.cleaned_data.get("username")
            phonenumber = form.cleaned_data.get("phonenumber")
            email = form.cleaned_data.get("email")
            name = form.cleaned_data.get("full_name")
            fn = name.split(" ")[0]
            ln = name.split(" ")[-1]
            mn = ""
            for i in name.split(" ")[1:-1]:
                mn = mn + i + " "
            city = form.cleaned_data.get("city")
            district = form.cleaned_data.get("district")
            subdistrict = form.cleaned_data.get("subdistrict")
            street = form.cleaned_data.get("street")
            description = form.cleaned_data.get("description")
            user.accountid.user.username = username
            user.contactinfoid.phonenumber = phonenumber
            user.contactinfoid.email = email
            user.fullnameid.firstname = fn
            user.fullnameid.middlename = mn
            user.fullnameid.lastname = ln
            user.addressid.city = city
            user.addressid.district = district
            user.addressid.subdistrict = subdistrict
            user.addressid.street = street
            user.addressid.description = description
            
            user.accountid.user.save()
            user.contactinfoid.save()
            user.fullnameid.save()
            user.addressid.save()
            user.save()

            form.instance.userid = user
            context = {"customer" : Customer.objects.get(userid = user)}
        return render(request, "customerprofile.html", context)

# Danh sách dịa chỉ nhận hàng của khách hàng
class ShippingAddressListView(View):
    template_name = "shippingaddresslist.html"
    def get(self, request, *args, **kwargs):
        cus_id = kwargs['cus_id']
        customer = Customer.objects.get(id = cus_id)
        shippingaddresslist = [customeraddress.shippingaddressid for customeraddress in CustomerShippingaddress.objects.filter(customerid = customer)]
        context = {"shippingaddresslist" : shippingaddresslist, "customer" : customer}
        return render(request, self.template_name, context)

# Xóa địa chỉ nhận hàng
class ShippingAddressDeleteView(View):
    template_name = "shippingaddresslist.html"
    def get(self, request, *args, **kwargs):
        addr_id = kwargs['addr_id']
        address = Address.objects.get(id = addr_id)
        address.delete()
        cus_id = kwargs['cus_id']
        customer = Customer.objects.get(id = cus_id)
        shippingaddresslist = [customeraddress.shippingaddressid for customeraddress in CustomerShippingaddress.objects.filter(customerid = customer)]
        context = {"shippingaddresslist" : shippingaddresslist, "customer" : customer}
        return render(request, self.template_name, context)
        
#Tạo địa chỉ nhận Hàng
class ShippingAddressCreateView(EcomMixin, View):
    template_name = "shippingaddresscreate.html"

    def get(self, request, *args, **kwargs):
        form = ShippingAddressCreateForm()
        context = {"form":form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ShippingAddressCreateForm(request.POST)
        if form.is_valid():
            cus_id = kwargs['cus_id']
            customer = Customer.objects.get(id = cus_id)
            city = form.cleaned_data.get("city")
            district = form.cleaned_data.get("district")
            subdistrict = form.cleaned_data.get("subdistrict")
            street = form.cleaned_data.get("street")
            description = form.cleaned_data.get("description")
            phonenumberreceive = form.cleaned_data.get('phonenumberreceive')
            address = Address.objects.create(city = city, district = district, subdistrict = subdistrict, street = street, description = description)
            shippingaddress = Shippingaddress.objects.create(addressid = address, phonenumberreceive = phonenumberreceive)
            form.instance.customerid = customer
            form.instance.shippingaddressid = shippingaddress
            form.save()
            shippingaddresslist = [customeraddress.shippingaddressid for customeraddress in CustomerShippingaddress.objects.filter(customerid = customer)]
            context = {"form":form, "shippingaddresslist":shippingaddresslist, "customer" : customer}

        return render(request, "shippingaddresslist.html", context)

#Chỉnh sửa địa chỉ nhận hàng
class ShippingAddressEditView(EcomMixin, View):
    template_name = "shippingaddressedit.html"

    def get(self, request, *args, **kwargs):
        form = ShippingAddressCreateForm()
        addr_id = kwargs['addr_id']
        shippingaddress = Shippingaddress.objects.get(id = addr_id)
        form.fields['city'].initial  = shippingaddress.addressid.city
        form.fields['district'].initial  =shippingaddress.addressid.district
        form.fields['subdistrict'].initial  = shippingaddress.addressid.subdistrict
        form.fields['street'].initial  = shippingaddress.addressid.street
        form.fields['description'].initial  = shippingaddress.addressid.description
        form.fields['phonenumberreceive'].initial  = shippingaddress.phonenumberreceive
        context = {"form":form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ShippingAddressCreateForm(request.POST)
        if form.is_valid():
            cus_id = kwargs['cus_id']
            addr_id = kwargs['addr_id']
            customer = Customer.objects.get(id = cus_id)
            city = form.cleaned_data.get("city")
            district = form.cleaned_data.get("district")
            subdistrict = form.cleaned_data.get("subdistrict")
            street = form.cleaned_data.get("street")
            description = form.cleaned_data.get("description")
            phonenumberreceive = form.cleaned_data.get("phonenumberreceive")
            shippingaddress = Shippingaddress.objects.get(id = addr_id)
            address = Address.objects.get(id = shippingaddress.addressid.id)
            address.city = city
            address.district = district
            address.subdistrict = subdistrict
            address.street = street
            address.description = description
            address.save()
            shippingaddress.phonenumberreceive = phonenumberreceive
            shippingaddress.save()
            shippingaddresslist = [customeraddress.shippingaddressid for customeraddress in CustomerShippingaddress.objects.filter(customerid = customer)]
            context = {"form":form, "shippingaddresslist":shippingaddresslist, "customer" : customer}

        return render(request, "shippingaddresslist.html", context)

# Xem chi tiết sản phẩm -> thêm vào giỏ hàng, bình luận
class ProductDetailView(View):

    def get(self, request, *args, **kwargs):
        form = FeedBackForm()
        url_slug = kwargs['slug']
        item = Item.objects.get(slug=url_slug)
        product = Product.objects.get(id = item.productid.id)
        print ('sdjkshdkjashdkjashdkjasdhas, ',product.id)
        product1 = Product.objects.get(id = item.productid.id)
        if product1.type == 'Clothes':
            product = Clothes.objects.get(productid = product1)
        elif product1.type == 'Electronic':
            product = Electronic.objects.get(productid = product1)
        elif product1.type == 'Book':
            product = Book.objects.get(productid = product1) 
      
        feedbacks = Feedback.objects.filter(itemid =item)
        context = {'form': form, "item":item, "product":product, "feedbacks": feedbacks}
        return render(request, 'productdetailTEST.html', context)
    def dispatch(self, request, *args, **kwargs):
        print(request.method)
        if request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = request.user).exists() and Users.objects.filter(accountid__user = request.user, is_active = True).exists():
            pass
        else:
            if(request.method == 'POST'):
                return redirect("/login")
            else:
                pass
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        form = FeedBackForm(data=request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            rate = form.cleaned_data['rating']
            url_slug = kwargs['slug']
            item = Item.objects.get(slug=url_slug)
            customer = Customer.objects.get(userid__accountid__user = request.user)
            feedback = Feedback.objects.create(itemid = item, customerid = customer, content = content, rate = rate)
            feedback.save()
            feedbacks = Feedback.objects.filter(itemid = item)
            context = {'form': FeedBackForm(), "item": item, "feedbacks": feedbacks}
        return render(request, 'productdetailTEST.html', context)


# Thêm vào giỏ hàng
class AddToCartView( LoginRequiredMixin,EcomMixin, View):
        def get(self, request, *args, **kwargs):
            product_id = self.kwargs['pro_id']
        # get product
            product_obj = Item.objects.get(id=product_id)
            if self.request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = self.request.user).exists():
                customer = Customer.objects.get(userid__accountid__user = self.request.user)
                # check if cart exists
                cart_id = self.request.session.get("cart_id", None)
                if cart_id:
                    cart_obj = Shoppingcart.objects.get(id=cart_id)
                    this_product_in_cart = Cartline.objects.filter(itemid = product_obj)

                    # item already exists in cart
                    if this_product_in_cart.exists():
                        cartproduct = this_product_in_cart.last()
                        cartproduct.num += 1
                        cartproduct.save()
                        cart_obj.save()
                    # new item is added in cart
                    else:
                        cartproduct = Cartline.objects.create(
                            shoppingcartid=cart_obj, itemid=product_obj, num=1)
                        cart_obj.save()

                else:
                    if Shoppingcart.objects.filter(customerid = customer).exists():
                        cart_obj = Shoppingcart.objects.get(customerid = customer)
                        this_product_in_cart = Cartline.objects.filter(itemid = product_obj)

                        # item already exists in cart
                        if this_product_in_cart.exists():
                            cartproduct = this_product_in_cart.last()
                            cartproduct.num += 1
                            cartproduct.save()
                            cart_obj.save()
                        # new item is added in cart
                        else:
                            cartproduct = Cartline.objects.create(
                                shoppingcartid=cart_obj, itemid=product_obj, num=1)
                            cart_obj.save()  
                    else:
                        cart_obj = Shoppingcart.objects.create(customerid = customer)
                        self.request.session['cart_id'] = cart_obj.id
                        cartproduct = Cartline.objects.create(
                            shoppingcartid=cart_obj, itemid=product_obj, num=1)
                        cart_obj.save()
                return redirect("ecomapp:mycart")

# Chỉnh sửa giỏ hàng -> xóa sản phẩm trong giỏ, tăng giảm số lượng
class ManageCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = Cartline.objects.get(id=cp_id)
        cart_obj = cp_obj.shoppingcartid

        if action == "inc":
            cp_obj.num += 1
            cp_obj.save()
            cart_obj.save()
        elif action == "dcr":
            cp_obj.num -= 1
            cp_obj.save()
            cart_obj.save()
            if cp_obj.num == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("ecomapp:mycart")

# Xóa toàn bộ sản phẩm trong giỏ
class EmptyCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        # # if cart_id:
        # cart = Shoppingcart.objects.get(id=cart_id)
        customer = Customer.objects.get(userid__accountid__user = self.request.user)
        cart = Shoppingcart.objects.get(id=cart_id) if cart_id else Shoppingcart.objects.get(customerid =customer)
        [cartline.delete() for cartline in Cartline.objects.filter(shoppingcartid = cart)]
        cart.save()
        return redirect("ecomapp:mycart")

# Xem giỏ hàng
class MyCartView(EcomMixin, LoginRequiredMixin,TemplateView):
    template_name = "mycartTEST.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = self.request.user).exists():
            cart_id = self.request.session.get("cart_id", None)
            if cart_id:
                cart = Shoppingcart.objects.get(id=cart_id)
            else:
                customer = Customer.objects.get(userid__accountid__user = self.request.user)
                if Shoppingcart.objects.filter(customerid = customer).exists():
                    cart = Shoppingcart.objects.get(customerid = customer)
                else:
                    cart = Shoppingcart.objects.create(customerid = customer)
            cartline = Cartline.objects.filter(shoppingcartid = cart)
            context['cartline'] = cartline
            context['cart'] = cart
        return context

# Đặt hàng -> chọn đia chỉ nhận, chọn hình thức vận chuyển, thanh toán
class CheckoutView(EcomMixin, CreateView ):
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("ecomapp:home")

    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.account):
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        customer = Customer.objects.get(userid__accountid__user = self.request.user)
        cart_obj = Shoppingcart.objects.get(id=cart_id) if cart_id else Shoppingcart.objects.get(customerid =customer)
        context['cart'] = cart_obj
        return context
    def form_valid(self,form):
        cart_id = self.request.session.get("cart_id")
        customer = Customer.objects.get(userid__accountid__user = self.request.user)
        cart_obj = Shoppingcart.objects.get(id=cart_id) if cart_id else Shoppingcart.objects.get(customerid =customer)
        cartlines = cart_obj.cartline_set.all()
        if Orderhistory.objects.filter(customerid__userid__accountid__user = self.request.user).exists():
            orderhistory = Orderhistory.objects.get(customerid__userid__accountid__user = self.request.user)
        else:
            orderhistory = Orderhistory.objects.create(customerid = customer)
        
        method = form.cleaned_data.get("paymentMethod")
        method_shipping = form.cleaned_data.get("shippingmethod")
        convert ={"1": "Cash",
                    "2": "Banking",
                    "3": "QRCode"}
        convert_shipping ={"1": "Normal",
                    "2": "Fast",
        }
        customershippingaddress  =form.cleaned_data.get("customershippingaddress")
        print("----------------------------------------",customershippingaddress)
        shippingaddressid  = customershippingaddress.shippingaddressid
        payment = Payment.objects.create(isComplete = False, method = convert[method])
        methodshipping = convert_shipping[method_shipping]
        form.instance.customerid = customer
        form.instance.paymentid = payment
        form.instance.shippingaddressid = shippingaddressid
        form.instance.status = "Order Received"
        form.instance.time = datetime.datetime.now()
        form.instance.shippingmethod = methodshipping
        order = form.save()
        historyline = Historyline.objects.create(orderhistoryid = orderhistory, orderid = order)
        historyline.save()
        for cartline in cartlines:
            orderitem = Orderitem.objects.create(orderid = order, itemid = cartline.itemid, count = cartline.num)
            orderitem.save()
            cartline.delete()
        return super().form_valid(form)

# Đăng ký tài khoản
class CustomerRegistrationView(CreateView):
    template_name = "customerregistration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("ecomapp:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        phonenumber = form.cleaned_data.get("phonenumber")
        email = form.cleaned_data.get("email")
        name = form.cleaned_data.get("full_name")
        fn = name.split(" ")[0]
        ln = name.split(" ")[-1]
        mn = ""
        for i in name.split(" ")[1:-1]:
            mn = mn + i + " "
        city = form.cleaned_data.get("city")
        district = form.cleaned_data.get("district")
        subdistrict = form.cleaned_data.get("subdistrict")
        street = form.cleaned_data.get("street")
        description = form.cleaned_data.get("description")
        fullname = Fullname.objects.create(lastname = ln, firstname = fn, middlename = mn)
        contact = Contactinfo.objects.create(email = email, phonenumber = phonenumber)
        user_ = User.objects.create_user(username = username, password = password)
        account = Account.objects.create(user = user_)
        addressid = Address.objects.create(description = description, city = city, district= district, subdistrict = subdistrict, street=street)
        # shippingaddressid = Shippingaddress.objects.create(addressid = addressid, phonenumberreceive = phonenumber)
        user = Users.objects.create(accountid = account, contactinfoid = contact, fullnameid = fullname, addressid = addressid)
        # customer = Customer.objects.create(userid = user,type_customer = "Normal" )
        # CustomerShippingaddress.objects.create(shippingaddressid =shippingaddressid, customerid = customer)
        form.instance.type_customer = 'Normal'
        form.instance.userid = user
        login(self.request, user.accountid.user)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

# Đăng xuất
class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecomapp:home")

# Thông báo đánh giá hệ thông thành công
class ReviewSuccessView(TemplateView):
    template_name = "reviewsuccess.html"
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

# Gửi đánh giá hệ thông
class SendReview(CreateView):
    template_name = "review.html"
    form_class = ReviewForm
    success_url = reverse_lazy("ecomapp:reviewsuccess")
    def form_valid(self, form):
        customer = Customer.objects.get(userid__accountid__user = self.request.user)
        content = form.cleaned_data.get("content")
        form.instance.customerid = customer
        form.instance.content = content
        form.instance.reviewtime = datetime.datetime.now()
        
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

# Đăng nhập tài khoản
class CustomerLoginView(FormView):
    template_name = "customerlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomapp:home")

    # form_valid method is a type of post method and is available in createview formview and updateview
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Customer.objects.filter(userid__accountid__user = usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


# class AboutView(EcomMixin, TemplateView):
#     template_name = "about.html"


# class ContactView(EcomMixin, TemplateView):
#     template_name = "contactus.html"


# Xem thông tin cá nhân , lịch sử đặt hàng
class CustomerProfileView(TemplateView):
    template_name = "customerprofile.html"
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        customer = Customer.objects.get(userid__accountid = self.request.user.account)
        context['customer'] = customer
        if kw is not None:
            orders = Order.objects.filter (Q(id__icontains=kw))
        else:
            orders = Order.objects.filter(customerid=customer).order_by("-id")
        context["orders"] = orders
        return context

#Xem danh sách các sản phẩm yêu thích
class WishListView(LoginRequiredMixin,EcomMixin,TemplateView):
    template_name = "wishlist.html"
    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = self.request.user).exists():
            context = super().get_context_data(**kwargs)
            customer = Customer.objects.get(userid__accountid = self.request.user.account)
            wishlist = Wishlist.objects.get(customerid = customer)
            wishListItem = [wishlistline.itemid for wishlistline in Wishlistline.objects.filter(wishlistid = wishlist)]
            context['wishListItem'] = wishListItem
            return context
        else:
            return redirect("ecomapp:home")
         
# Xem danh danh đã đánh giá hệ thống của tài khoản
class ReviewListView(TemplateView):
    template_name = "reviewlist.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(userid__accountid = self.request.user.account)
        reviews = Customerreview.objects.filter(customerid = customer)
        context['reviews'] = reviews
        return context

# Xem chi tiết đơn hàng cho khách hàng
class CustomerOrderDetailView(DetailView):
    template_name = "customerorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.account != order.customerid.userid.accountid:
                return redirect("ecomapp:customerprofile")
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)


# Tìm kiếm sản phẩm theo tên hoặc mô tả sản phẩm
class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Item.objects.filter(
            Q(productid__name__icontains=kw) | Q(description__icontains=kw))
        context["results"] = results
        return context

#------------------------- ADMIN ---------------------------

# nhân viên đăng xuất
class AdminLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecomapp:adminhome")

# Nhân viên đăng nhập
class AdminLoginView(FormView):
    template_name = "adminpages/adminlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomapp:adminhome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Staffs.objects.filter(userid__accountid__user = usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)

# Kiểm tra tài khoản có là tk của nhân viên hay không?
class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Staffs.objects.filter(userid__accountid__user = request.user).exists() and Users.objects.filter(accountid__user = request.user, is_active = True).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


# Trang chủ nhân viên 
class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminhome.html"

# Danh sách đơn hàng đang chờ xác nhận
class AdminPendingOrder(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminpendingorders.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(
            status="Order Received").order_by("-id")
        return context

# Danh sách nhân viên  (chỉ cho Manager)
class AdminStaffListView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/stafflist.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        if kw is not None:
            queryset = Staffs.objects.filter(
                Q(codeStaff__icontains=kw) | Q(position__icontains=kw))
        else:
            queryset = Staffs.objects.all()
        context["allstaffs"] = queryset
        return context

# Thêm nhân viên mới (chỉ cho manager)
class AdminStaffCreateView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/adminstaffcreate.html"
    form_class = StaffForm
    success_url = reverse_lazy("ecomapp:adminstafflist")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        phonenumber = form.cleaned_data.get("phonenumber")
        email = form.cleaned_data.get("email")
        name = form.cleaned_data.get("full_name")
        fn = name.split(" ")[0]
        ln = name.split(" ")[-1]
        mn = ""
        for i in name.split(" ")[1:-1]:
            mn = mn + i + " "
        city = form.cleaned_data.get("city")
        district = form.cleaned_data.get("district")
        subdistrict = form.cleaned_data.get("subdistrict")
        street = form.cleaned_data.get("street")
        description = form.cleaned_data.get("description")
        codeStaff = form.cleaned_data.get("codeStaff")
        position = form.cleaned_data.get("position")
        salary = form.cleaned_data.get("salary")
        startdate = form.cleaned_data.get("startdate")
        workingtime = form.cleaned_data.get("workingtime")
        fullname = Fullname.objects.create(lastname = ln, firstname = fn, middlename = mn)
        contact = Contactinfo.objects.create(email = email, phonenumber = phonenumber)
        user_ = User.objects.create_user(username = username, password = password)
        account = Account.objects.create(user = user_)
        addressid = Address.objects.create(description = description, city = city, district= district, subdistrict = subdistrict, street=street)
        user = Users.objects.create(accountid = account, contactinfoid = contact, fullnameid = fullname, addressid = addressid)
        form.instance.userid = user
        staff = Staffs.objects.create(userid = form.instance.userid, codeStaff= codeStaff ,position= position, salary = salary, startdate =startdate,   workingtime=   workingtime ) 
     
        if position == 'Manager':
            manager = Manager.objects.create(staffid = staff.userid)
        elif position == "SaleStaff":
            salestaff = Salesstaff.objects.create(staffid = staff.userid)
        elif position == "WarehouseStaff":
            warehousestaff = Warehousestaff.objects.create(staffid = staff.userid)
        elif position == "BusinessStaff":
            businessstaff = Businessstaff.objects.create(staffid = staff.userid)
        form.instance.staff =staff
        return super().form_valid(form)

# Xem thông tin và chỉnh sửa thông tin nhân viên( chỉ cho manager)
class AdminStaffDetailView(View):
    template_name = "adminpages/adminstaffdetail.html"

    def get(self, request, *args, **kwargs):
        form = EditStaffForm()
        staff_id = kwargs['staff_id']
        staff = Staffs.objects.get(userid = staff_id)
        form.fields['username'].initial  = staff.userid.accountid.user.username
        if staff.userid.contactinfoid is not None:
            form.fields['phonenumber'].initial  = staff.userid.contactinfoid.phonenumber
        if staff.userid.contactinfoid is not None:
            form.fields['email'].initial  = staff.userid.contactinfoid.email
        if staff.userid.fullnameid is not None:
            form.fields['full_name'].initial  = staff.userid.fullnameid.fullname
        if staff.userid.addressid is not None:
            form.fields['city'].initial  = staff.userid.addressid.city
            form.fields['district'].initial  = staff.userid.addressid.district
            form.fields['subdistrict'].initial  = staff.userid.addressid.subdistrict
            form.fields['street'].initial  = staff.userid.addressid.street
            form.fields['description'].initial  = staff.userid.addressid.description
        form.fields['codeStaff'].initial = staff.codeStaff
        form.fields['salary'].initial = staff.salary
        form.fields['position'].initial = staff.position
        form.fields['startdate'].initial = staff.startdate
        form.fields['workingtime'].initial = staff.workingtime
        form.fields['is_active'].initial = staff.userid.is_active
        print("--------------------------------")
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = EditStaffForm(data=request.POST or None) 
        print("------")
        if form.is_valid():
            print('------------------------sahjÁGJha')
            staff_id = kwargs['staff_id']
            staff = Staffs.objects.get(userid = staff_id)
         
            username = form.cleaned_data.get("username")
            phonenumber = form.cleaned_data.get("phonenumber")
            email = form.cleaned_data.get("email")
            name = form.cleaned_data.get("full_name")
            fn = name.split(" ")[0]
            ln = name.split(" ")[-1]
            mn = ""
            for i in name.split(" ")[1:-1]:
                mn = mn + i + " "
            city = form.cleaned_data.get("city")
            district = form.cleaned_data.get("district")
            subdistrict = form.cleaned_data.get("subdistrict")
            street = form.cleaned_data.get("street")
            description = form.cleaned_data.get("description")
            codeStaff = form.cleaned_data.get("codeStaff")
            # position = form.cleaned_data.get("position")
            salary = form.cleaned_data.get("salary")
            startdate = form.cleaned_data.get("startdate")
            workingtime = form.cleaned_data.get("workingtime")
            is_active = form.cleaned_data.get('is_active')
            if  staff.userid.addressid  is None:
                staff.userid.addressid = Address.objects.create()
            if  staff.userid.contactinfoid  is None:
                staff.userid.contactinfoid = Contactinfo.objects.create()
            if  staff.userid.fullnameid  is None:
                staff.userid.fullnameid = Fullname.objects.create()
            staff.userid.accountid.user.username = username
            staff.userid.contactinfoid.phonenumber = phonenumber
            staff.userid.contactinfoid.email = email
            staff.userid.fullnameid.firstname = fn
            staff.userid.fullnameid.middlename = mn
            staff.userid.fullnameid.lastname = ln
            staff.userid.addressid.city = city
            staff.userid.addressid.district = district
            staff.userid.addressid.subdistrict = subdistrict
            staff.userid.addressid.street = street
            staff.userid.addressid.description = description
            staff.codeStaff= codeStaff
            staff.position =  staff.position
            staff.salary = salary
            staff.startdate  =  startdate 
            staff.workingtime = workingtime
            print("---------------------------",is_active)
            staff.userid.is_active = is_active
            staff.userid.accountid.user.save()
            staff.userid.contactinfoid.save()
            staff.userid.fullnameid.save()
            staff.userid.addressid.save()
            staff.userid.save()
            staff.save()
        return redirect("/admin-staff/list/")

# Xem thông tin và chỉnh sủa thông tin sản phẩm (Book, electronic, clothes)
class AdminProductDetailView(View):
    template_name = "adminpages/adminproductdetail.html"

    def get(self, request, *args, **kwargs):
        form = EditBookProductForm()
        pro_id = kwargs['pro_id']
        product = Product.objects.get(id=pro_id)
        if product.type ==  'Clothes':
            form = EditClothesProductForm()
        elif product.type ==  'Electronic':
            form = EditElectronicProductForm()
        elif  product.type ==  'Book':
            form = EditBookProductForm()
        form.fields['producer'].initial  = product.producerid
        form.fields['name'].initial  = product.name
        form.fields['manufacturingyear'].initial  = product.manufacturingyear
        # form.fields['type'].initial = product.type
        if product.type ==  'Clothes':
            clothes = Clothes.objects.get(productid = product)
            form.fields['clothtype'].initial = clothes.clothtype 
            form.fields['color'].initial = clothes.color 
            form.fields['gender'].initial = clothes.gender 
            form.fields['brand'].initial = clothes.brand
            form.fields['material'].initial = clothes.material
        elif product.type ==  'Electronic':
            electronic =  Electronic.objects.get(productid = product)
            form.fields['devicetype'].initial = electronic.devicetype 
            form.fields['color'].initial = electronic.color 
            form.fields['weight'].initial = electronic.weight 
            form.fields['brand'].initial = electronic.brand
            form.fields['size'].initial = electronic.size
            form.fields['power'].initial = electronic.power
        elif  product.type ==  'Book':
            book = Book.objects.get(productid = product)
            form.fields['numpage'].initial = book.numpage
            form.fields['author'].initial = book.author
            form.fields['genre'].initial = book.genre
        context = {'form': form, "product": product}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = EditBookProductForm(data=request.POST)
        pro_id = kwargs['pro_id']
        product = Product.objects.get(id=pro_id)
        if product.type ==  'Clothes':
            form = EditClothesProductForm(data=request.POST)
        elif product.type ==  'Electronic':
            form = EditElectronicProductForm(data=request.POST)
        elif  product.type ==  'Book':
            form = EditBookProductForm(data=request.POST)
        if form.is_valid():
            producer = form.cleaned_data['producer']
            name = form.cleaned_data['name']
            manufacturingyear = form.cleaned_data['manufacturingyear']
            product = Product.objects.get(id=pro_id)
            product.producer = producer
            product.name = name
            product.manufacturingyear = manufacturingyear
            product.save()
            form.fields['producer'].initial  = product.producerid
            form.fields['name'].initial  = product.name
            form.fields['manufacturingyear'].initial  = product.manufacturingyear
    
            if  type ==  'Clothes':
                clothes =  Clothes.objects.get(productid = product)
                
                color = form.cleaned_data.get("color")
                clothtype = form.cleaned_data.get("clothtype")
                gender = form.cleaned_data.get("gender")
                brand  = form.cleaned_data.get("brand")
                material = form.cleaned_data.get("material")
                
                clothes.color = color
                clothes.clothtype = clothtype
                clothes.gender = gender
                clothes.brand = brand
                clothes.material = material
                clothes.save()

                form.fields['clothetype'].initial = clothes.clothetype 
                form.files['color'].initial = clothes.color 
                form.files['gender'].initial = clothes.gender 
                form.files['brand'].initial = clothes.brand
                form.files['material'].initial = clothes.material
            elif type ==  'Electronic':
                electronic =  Electronic.objects.get(productid = product)
                
                devicetype = form.clean_data.get('devicetype')
                color = form.cleaned_data.get("color")
                brand  = form.cleaned_data.get("brand")
                weight = form.cleaned_data.get("weight")
                size = form.cleaned_data.get("size")
                power = form.cleaned_data.get("power")

                electronic.devicetype =  devicetype
                electronic.color =  color
                electronic.brand =  brand
                electronic.weight =  weight
                electronic.size =  size
                electronic.power =  power
                electronic.save()

                form.fields['devicetype'].initial = electronic.devicetype 
                form.fields['color'].initial = electronic.color 
                form.fields['weight'].initial = electronic.weight 
                form.fields['brand'].initial = electronic.brand
                form.fields['size'].initial = electronic.size
                form.fields['power'].initial = electronic.power
            elif  product.type ==  'Book': 
                book = Book.objects.get(productid = product)
                
                numpage = form.cleaned_data.get("numpage")
                author = form.cleaned_data.get("author")
                genre  = form.cleaned_data.get("genre")  

                book.numpage = numpage  
                book.author = author 
                book.genre = genre
                book.save()

                form.fields['numpage'].initial = book.numpage
                form.fields['author'].initial = book.author
                form.fields['genre'].initial = book.genre
        context = {'form': form, "product": product}
        return render(request, self.template_name, context)


# Xem chi tiết mặt hàng -> có thể thạy đổi giá, mô tả , đăng tải or không đăng tải
class AdminItemDetailView(View):
    template_name = "adminpages/adminitemdetail.html"

    def get(self, request, *args, **kwargs):
        form = EditItemForm()
        url_slug = kwargs['slug']
        product = Item.objects.get(slug=url_slug)
        form.fields['price'].initial  = product.price
        form.fields['description'].initial  = product.description
        context = {'form': form, "product": product}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = EditItemForm(data=request.POST)
        if form.is_valid():
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            url_slug = kwargs['slug']
            product = Item.objects.get(slug=url_slug)
            product.price = price
            product.description = description
            if request.POST.get("upload", "") == "true":
                product.isUpload = True
            else:
                product.isUpload = False
            product.save()
            form.fields['price'].initial  = price
            form.fields['description'].initial  = description
            context = {'form': form, "product": product}
        return render(request, self.template_name, context)

# Xem chi tiết đơn hàng 
class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = "adminpages/adminorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context

# Xem danh sách đơn hàng
class AdminOrderListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminorderlist.html"
    queryset = Order.objects.all().order_by("-id")
    context_object_name = "allorders"

# Xem danh sách đánh giá hệ thống của khách hàng
class AdminReviewListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminreviewlist.html"
    queryset = Customerreview.objects.all().order_by("-id")
    context_object_name = "allreviews"

#Xem chi tiết đánh giá của khách hàng
class AdminReviewDetailView(AdminRequiredMixin, DetailView):
    template_name = "adminpages/adminreviewdetail.html"
    model = Customerreview
    context_object_name = "rv_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session["review_id"] = context['rv_obj'].id
        return context

#Phản hồi đánh giá của khách hàng
class AdminReplyReviewView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/adminreplyreview.html"
    form_class = ReplyReviewForm
    success_url = reverse_lazy("ecomapp:adminhome")

    def form_valid(self, form):
        staff = Staffs.objects.get(userid__accountid__user = self.request.user)
        review = Customerreview.objects.get(id = self.request.session['review_id'])
        review.isReply = True
        review.save()
        del self.request.session['review_id']
        message = form.cleaned_data.get("content")
        form.instance.customerreviewid = review
        form.instance.message = message
        form.instance.time = datetime.datetime.now()
        form.instance.staffid = staff

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

# Thay đổi trạng thái đơn hàng
class AdminOrderStatusChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.status = new_status
        order_obj.save()
        return redirect(reverse_lazy("ecomapp:adminorderdetail", kwargs={"pk": order_id}))

# Xem danh sách các sản phẩm
class AdminProductListView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminproductlistTEST.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        allcategory = Category.objects.all().order_by("-id")
        
        kw = self.request.GET.get("keyword")
        if kw is not None:
            queryset = Product.objects.filter(
                Q(id__icontains=kw) | Q(name__icontains=kw))
        else:
            queryset = Product.objects.all().order_by("-id")
        context["allproducts"] = queryset
        context["allcategory"] =  allcategory
        return context

# Xem danh sách mặt hàng 
class AdminItemListView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminitemlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        if kw is not None:
            queryset = Item.objects.filter(
                Q(productid__name__icontains=kw) | Q(description__icontains=kw))
         
           
        else:
            queryset = Item.objects.all().order_by("-id")
        # list_import_item = []
        # a = []
        # for i in queryset:
        #     list1 = Importingrecord.objects.filter(productid= i.productid)
        #     if len(list1)==1:
        #         list_import_item.append(Importingrecord.objects.get(productid= i.productid))
        #     else :
        #         max_id = list1[0].id
        #         for j in list1:
        #             max_id =  max(max_id, j.id)
        #         list_import_item.append(Importingrecord.objects.get(id =max_id))
        context["allproducts"] = queryset
        # context["importitem"] = list_import_item
    
        return context

# Xem danh sách các lịch sử hóa đơn nhập hàng
class AdminImprotingrecordListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminimportingrecordlist.html"
    queryset = Importingrecord.objects.all().order_by("-id")
    context_object_name = "allrecords"

# Xóa sản phẩm
class AdminProductDeleteView(AdminRequiredMixin, View):
    template_name = "adminpages/adminproductlistTEST.html"
    
    def get(self, request, *args, **kwargs):
        allcategory = Category.objects.all().order_by("-id")
        pro_id = self.kwargs["pro_id"]
        product = Product.objects.get(id = pro_id)
        product.delete()
        queryset = Product.objects.all().order_by("-id")
        # context = {"allproducts":queryset}
        # context['allcatgory'] =  allcategory
        # return render(request, self.template_name, context)
        return redirect(reverse_lazy("ecomapp:adminproductlist"))

#
# class AdminItemDeleteView(AdminRequiredMixin, View):
#     template_name = "adminpages/adminproductlist.html"
#     def get(self, request, *args, **kwargs):
#         queryset = Item.objects.all().order_by("-id")
#         pro_id = self.kwargs["pro_id"]
#         item = Item.objects.get(id = pro_id)
#         item.productid.delete()
#         context = {"allproducts":queryset}
#         return render(request, self.template_name, context)


# Thêm sản phẩm
class AdminProductCreateView(AdminRequiredMixin, View):
    template_name = "adminpages/adminproductcreate.html"

    def get(self, request, *args, **kwargs):
        cagetoryid = kwargs["cate_id"]
        form = BookProductForm()
        if cagetoryid==1:
            form = ClothesProductForm()
        elif cagetoryid==2:
            form = ElectronicProductForm()
        elif cagetoryid ==3:
            form = BookProductForm()
        context = {'form': form}
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        cagetoryid = kwargs["cate_id"]
        form = BookProductForm(data=request.POST)
        if cagetoryid==1:
            form = ClothesProductForm(data=request.POST)
        elif cagetoryid==2:
            form = ElectronicProductForm(data=request.POST)
        elif cagetoryid ==3:
            form = BookProductForm(data=request.POST)
        if form.is_valid():
            producer = form.cleaned_data.get("producer")
            manufacturingyear = form.cleaned_data.get("manufacturingyear")
            name = form.cleaned_data.get("name")
            prod_type =str(cagetoryid)
            slug = form.cleaned_data.get("slug")
            description = form.cleaned_data.get("description")
            convert = {
                "1": "Clothes",
                "2": "Electronic",
                "3": "Book"
            }
            p = Product.objects.create(producerid = producer, manufacturingyear = manufacturingyear,
                                        type = convert[prod_type], name = name)
            if cagetoryid ==1: # Clothes
                color = form.cleaned_data.get("color")
                clothtype = form.cleaned_data.get("clothetype")
                gender = form.cleaned_data.get("gender")
                brand  = form.cleaned_data.get("brand")
                material = form.cleaned_data.get("material")
                Clothes.objects.create(productid = p,clothtype = clothtype,color =color, gender =gender, brand =brand, material = material )
            elif cagetoryid ==2: #Electronic
                devicetype = form.cleaned_data.get('devicetype')
                color = form.cleaned_data.get("color")
                brand  = form.cleaned_data.get("brand")
                weight = form.cleaned_data.get("weight")
                size = form.cleaned_data.get("size")
                power = form.cleaned_data.get("power")
                Electronic.objects.create(productid = p, devicetype = devicetype, color = color,  brand = brand, weight = weight ,  size  =  size , power = power)
            elif cagetoryid == 3: #Book
                numpage = form.cleaned_data.get("numpage")
                author = form.cleaned_data.get("author")
                genre  = form.cleaned_data.get("genre")
                Book.objects.create(productid = p, numpage= numpage, author= author, genre = genre )
            images = self.request.FILES.getlist("images")
            Item.objects.create(productid= p, slug = slug,   image = images[0], description = description)
            ProductCategory.objects.create(categoryid = Category.objects.get(name = convert[prod_type]), productid = p)
        
            form.instance.productid = p
            form.instance.description = description
            form.instance.slug = slug
            form.instance.image = images[0]
        # return super().form_valid(form)
        return redirect(reverse_lazy("ecomapp:adminproductlist"))

#Nhập hàng (kho có sản phẩm)
class AdminImportProductView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/adminimportproduct.html"
    form_class = ImportProductForm
    success_url = reverse_lazy("ecomapp:adminimportproduct")

    def form_valid(self, form):
        supplier = form.cleaned_data.get("supplier")
        product = form.cleaned_data.get("product")
        number = form.cleaned_data.get("number")
        price = form.cleaned_data.get("price")
        product.num += number
        item = Item.objects.get(productid = product)
        item.price_import = price
        item.price = price*(1+0.1)
        item.save()
        product.save()
        staff = Staffs.objects.get(userid__accountid__user = self.request.user)
        date = datetime.datetime.now()
        form.instance.supplierid = supplier
        form.instance.productid = product
        form.instance.staffid = staff
        form.instance.date = date
        form.instance.num = number
        form.instance.price = price
        return super().form_valid(form)
    
# class Statistic(AdminRequiredMixin, TemplateView):
#     template_name = "adminpages/statistic.html"
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["pendingorders"] = Order.objects.filter(
#             status="Order Received").order_by("-id")
#         # position = ""
#         # if Staffs.objects.get(userid__accountid__user = request.user).exists():
#         #     staff = Staffs.objects.get(userid__accountid__user = request.user)
#         #     position = staff.position
#         # else:
#         #     position = "Null"
#         # context['position'] = self.get_abc()
#         return context

# Báo cáo về doanh thu
class Reports(AdminRequiredMixin, TemplateView):
  
    template_name = "adminpages/test.html"
    def run_custome_sql(self, query):
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchall()
        return row
    def generate_template(self, startdate, enddate):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = "media/docx_template/BaoCaoDoanhThu.docx"
        filepath = os.path.join(base_dir, filename)
        # create a document object
        doc = DocxTemplate(filepath)

        syear ,smonth= startdate.split('-')
        eyear, emonth  = enddate.split('-')
        # create context to pass data to template
        # query_tong_doanh_thu = f"select sum((i.price)*oi.count) as revenue\
        #                         from [order] o \
        #                         join [orderitem] oi on o.id = oi.id\
        #                         join [item] i on oi.ItemID = i.id\
        #                         where (strftime('%m', o.Time) >= \"{smonth}\" and strftime('%m', o.Time) <= \"{emonth}\" and strftime('%Y', o.Time) = \"{syear}\"and strftime('%Y', o.Time) = \"{eyear}\" ) or ( strftime('%Y', o.Time) >= \"{syear}\" and strftime('%Y', o.Time) <= \"{eyear}\")"
        # query_loi_nhuan = f"select  sum((i.price - im.price)*oi.count) as profit \
        #                     from [order] o  \
        #                     join [orderitem] oi on o.id = oi.id \
        #                     join [item] i on oi.ItemID = i.id \
        #                     join [product] p on i.ProductID = p.id \
        #                     join [importingrecord] im on im.productid = p.id\
        #                      where (strftime('%m', o.Time) >= \"{smonth}\" and strftime('%m', o.Time) <= \"{emonth}\" and strftime('%Y', o.Time) = \"{syear}\"and strftime('%Y', o.Time) = \"{eyear}\" ) or ( strftime('%Y', o.Time) >= \"{syear}\" and strftime('%Y', o.Time) <= \"{eyear}\")"
        # query_ti_le_loi_nhuan = f"select  (CAST((i.price - im.price) as REAL)/i.Price)*100 as profit \
        #                     from [order] o \
        #                     join [orderitem] oi on o.id = oi.id \
        #                     join [item] i on oi.ItemID = i.id \
        #                     join [product] p on i.ProductID = p.id \
        #                     join [importingrecord] im on im.productid = p.id \
        #                     where (strftime('%m', o.Time) >= \"{smonth}\" and strftime('%m', o.Time) <= \"{emonth}\" and strftime('%Y', o.Time) = \"{syear}\"and strftime('%Y', o.Time) = \"{eyear}\" ) or ( strftime('%Y', o.Time) >= \"{syear}\" and strftime('%Y', o.Time) <= \"{eyear}\") \
        #                     group by strftime('%m', o.Time)"
        # query_khach_hang_moi = f"select count(*) as new_customer \
        #                     from [users] u  \
        #                     join account a on a.user_id = u.id \
        #                     where  strftime('%m', a.Date_created) >= \"{smonth}\" and strftime('%m', a.Date_created) <= \"{emonth}\" and strftime('%Y', a.Date_created) >= \"{syear}\" and strftime('%Y', a.Date_created) <= \"{eyear}\""                     
        # query_doanh_thu_tb_khach = f"select  cast(sum(i.price*oi.count) as real)/(count(distinct o.CustomerID)) as profit \
        #                         from [order] o \
        #                         join [orderitem] oi on o.id = oi.id \
        #                         join [item] i on oi.ItemID = i.id \
        #                          where (strftime('%m', o.Time) >= \"{smonth}\" and strftime('%m', o.Time) <= \"{emonth}\" and strftime('%Y', o.Time) = \"{syear}\"and strftime('%Y', o.Time) = \"{eyear}\" ) or ( strftime('%Y', o.Time) >= \"{syear}\" and strftime('%Y', o.Time) <= \"{eyear}\")"
        # query_doanh_thu_chi_tiet = f"select  p.name, i.price, sum(oi.count) as quantity, sum(i.price *oi.count) as revenue \
        #                         from [order] o \
        #                         join [orderitem] oi on o.id = oi.id \
        #                         join [item] i on oi.ItemID = i.id \
        #                         join [product] p on i.ProductID = p.id \
        #                         join [importingrecord] im on im.productid = p.id \
        #                          where (strftime('%m', o.Time) >= \"{smonth}\" and strftime('%m', o.Time) <= \"{emonth}\" and \"{syear}\" = \"{eyear}\"  ) or ( strftime('%Y', o.Time) >= \"{syear}\" and strftime('%Y', o.Time) <= \"{eyear}\") \
        #                         group by itemid \
        #                         order by revenue desc \
        #                         limit 10"
        # query_doanh_thu_theo_thang = f"select strftime('%m', o.Time) as month,strftime('%Y', o.Time) as year,\
        #                         sum((i.price)*oi.count) as revenue \
        #                         from [order] o  \
        #                         join [orderitem] oi on o.id = oi.id \
        #                         join [item] i on oi.ItemID = i.id \
        #                         where (strftime('%m', o.Time) >= \"{smonth}\" and strftime('%m', o.Time) <= \"{emonth}\" and strftime('%Y', o.Time) = \"{syear}\"and strftime('%Y', o.Time) = \"{eyear}\" ) or ( strftime('%Y', o.Time) >= \"{syear}\" and strftime('%Y', o.Time) <= \"{eyear}\" and  \"{eyear}\" != \"{syear}\" ) \
        #                         group by strftime('%m', o.Time), strftime('%Y', o.Time)"
        # query_doanh_thu_theo_category = f"select c.name as category_name, \
        #                         sum((i.price)*oi.count) as revenue \
        #                         from [order] o  \
        #                         join [orderitem] oi on o.id = oi.id \
        #                         join [item] i on oi.ItemID = i.id \
        #                         join [product] p on p.ID = i.ProductID \
        #                         join [product_category] pc on p.ID = pc.ProductID \
        #                         join [category] c on c.ID = pc.CategoryID  \
        #                         where (strftime('%m', o.Time) >= \"{smonth}\" and strftime('%m', o.Time) <= \"{emonth}\" and strftime('%Y', o.Time) = \"{syear}\"and strftime('%Y', o.Time) = \"{eyear}\" ) or ( strftime('%Y', o.Time) >= \"{syear}\" and strftime('%Y', o.Time) <= \"{eyear}\") \
        #                         group by c.name"
        query_tong_doanh_thu = f"select sum((i.price)*oi.count) as revenue\
                                from [order] o \
                                join [orderitem] oi on o.id = oi.id\
                                join [item] i on oi.ItemID = i.id\
                                where strftime('%Y-%m', o.Time) >= \"{startdate}\" and strftime('%Y-%m', o.Time) <= \"{enddate}\" "
        query_loi_nhuan = f"select  sum((i.price - im.price)*oi.count) as profit \
                            from [order] o  \
                            join [orderitem] oi on o.id = oi.id \
                            join [item] i on oi.ItemID = i.id \
                            join [product] p on i.ProductID = p.id \
                            join [importingrecord] im on im.productid = p.id\
                            where strftime('%Y-%m', o.Time) >= \"{startdate}\" and strftime('%Y-%m', o.Time) <= \"{enddate}\""
        query_ti_le_loi_nhuan = f"select  (CAST((i.price - im.price) as REAL)/i.Price)*100 as profit \
                            from [order] o \
                            join [orderitem] oi on o.id = oi.id \
                            join [item] i on oi.ItemID = i.id \
                            join [product] p on i.ProductID = p.id \
                            join [importingrecord] im on im.productid = p.id \
                            where strftime('%Y-%m', o.Time) >= \"{startdate}\" and strftime('%Y-%m', o.Time) <= \"{enddate}\" \
                            group by strftime('%m', o.Time)"
        query_khach_hang_moi = f"select count(*) as new_customer \
                            from [users] u  \
                            join account a on a.user_id = u.id \
                            where  strftime('%Y-%m', a.Date_created) >= \"{startdate}\" and strftime('%Y-%m', a.Date_created) <= \"{enddate}\" "                     
        query_doanh_thu_tb_khach = f"select  cast(sum(i.price*oi.count) as real)/(count(distinct o.CustomerID)) as profit \
                                from [order] o \
                                join [orderitem] oi on o.id = oi.id \
                                join [item] i on oi.ItemID = i.id \
                                 where strftime('%Y-%m', o.Time) >= \"{startdate}\" and strftime('%Y-%m', o.Time) <= \"{enddate}\""
        query_doanh_thu_chi_tiet = f"select  p.name, i.price, sum(oi.count) as quantity, sum(i.price *oi.count) as revenue \
                                from [order] o \
                                join [orderitem] oi on o.id = oi.id \
                                join [item] i on oi.ItemID = i.id \
                                join [product] p on i.ProductID = p.id \
                                join [importingrecord] im on im.productid = p.id \
                                where strftime('%Y-%m', o.Time) >= \"{startdate}\" and strftime('%Y-%m', o.Time) <= \"{enddate}\" \
                                group by itemid \
                                order by revenue desc \
                                limit 10"
        query_doanh_thu_theo_thang = f"select strftime('%m', o.Time) as month,strftime('%Y', o.Time) as year,\
                                sum((i.price)*oi.count) as revenue \
                                from [order] o  \
                                join [orderitem] oi on o.id = oi.id \
                                join [item] i on oi.ItemID = i.id \
                                where strftime('%Y-%m', o.Time) >= \"{startdate}\" and strftime('%Y-%m', o.Time) <= \"{enddate}\" \
                                group by strftime('%m', o.Time), strftime('%Y', o.Time) \
                                order by  strftime('%Y', o.Time) asc, strftime('%m', o.Time) asc"
        query_doanh_thu_theo_category = f"select c.name as category_name, \
                                sum((i.price)*oi.count) as revenue \
                                from [order] o  \
                                join [orderitem] oi on o.id = oi.id \
                                join [item] i on oi.ItemID = i.id \
                                join [product] p on p.ID = i.ProductID \
                                join [product_category] pc on p.ID = pc.ProductID \
                                join [category] c on c.ID = pc.CategoryID  \
                                where strftime('%Y-%m', o.Time) >= \"{startdate}\" and strftime('%Y-%m', o.Time) <= \"{enddate}\" \
                                group by c.name"
        tong_doanh_thu = "{:,}".format(self.run_custome_sql(query_tong_doanh_thu)[0][0])
        loi_nhuan = "{:,}".format(self.run_custome_sql(query_loi_nhuan)[0][0])
        ti_le_loi_nhuan = str(round(self.run_custome_sql(query_ti_le_loi_nhuan)[0][0],2))+"%"
        khach_hang_moi = "{:,}".format(self.run_custome_sql(query_khach_hang_moi)[0][0])
        doanh_thu_tb_khach = "{:,}".format(self.run_custome_sql(query_doanh_thu_tb_khach)[0][0])
        listDoanhThu = self.run_custome_sql(query_doanh_thu_chi_tiet)
        listDoanhThuTheoThang = self.run_custome_sql(query_doanh_thu_theo_thang)
        listDoanhThuTheoCategory = self.run_custome_sql(query_doanh_thu_theo_category)
        # create data for reports
        bangDoanhThuChiTiet = []
        for k in range(len(listDoanhThu)):
            bangDoanhThuChiTiet.append({"sNo": k+1, "ten": listDoanhThu[k][0],
                                "gia": "{:,}".format(listDoanhThu[k][1]), "soluong": "{:,}".format(listDoanhThu[k][2]),
                                  "doanhthu": "{:,}".format(listDoanhThu[k][3])})
        time =  ""
        if startdate != enddate:
            time =  " từ " +smonth + "/"+syear + " đến "+ emonth +"/"+eyear
        else:
            time = " trong " +emonth +"/"+eyear
      

        context = {
            # "startmonth": startmonth,
            # # "endmonth": endmonth,
            # "year": year,
            "time" : time,
            "tong_doanh_thu": tong_doanh_thu,
            "loi_nhuan": loi_nhuan,
            "ti_le_loi_nhuan": ti_le_loi_nhuan,
            "khách_hang_moi": khach_hang_moi,
            "doanh_thu_tb_khach": doanh_thu_tb_khach, 
            "bangDoanhThuChiTiet": bangDoanhThuChiTiet
        }
        
        doanhThuTheoThang = []
        for k in range(len(listDoanhThuTheoThang)):
            doanhThuTheoThang.append({"month": listDoanhThuTheoThang[k][0] +"-"+listDoanhThuTheoThang[k][1] ,"revenue": "{:,}".format(listDoanhThuTheoThang[k][2])})

        doanhThuTheoCategory = []
        for k in range(len(listDoanhThuTheoCategory)):
            doanhThuTheoCategory.append({"category_name": listDoanhThuTheoCategory[k][0], "revenue": "{:,}".format(listDoanhThuTheoCategory[k][1])})
        # print(doanhThuTheoThang)
        # Graph doanh thu theo category
        fig, ax = plt.subplots()
        # Plot the data on the axes
        ax.pie([x[1] for x in listDoanhThuTheoCategory], labels = [x[0] for x in listDoanhThuTheoCategory], autopct='%1.1f%%')

        # Add labels and title
        plt.legend(title='Danh muc', bbox_to_anchor=(1, 1))
        ax.set_title('Tỉ lệ doanh thu theo danh mục sản phẩm')
        image_path = os.path.join(base_dir, "static/doanhThuCategoryImg.png")
        fig.savefig(image_path)
        context['doanhThuCategoryImg'] = InlineImage(doc, image_path)   
             



        # Graph doanh thu theo thang
        fig, ax = plt.subplots(figsize=(10, 8))
        # Plot the data on the axes
        x1 = [x[0]+"-"+x[1] for x in listDoanhThuTheoThang]
        y1 = [x[2] for x in listDoanhThuTheoThang]
        ax.plot(x1, y1)
        plt.xticks(rotation = 90)
        # ax.xticks(ticks=x1, labels=x1, rotation='vertical')
        # Add labels and title
        ax.set_xlabel('Tháng')
        ax.set_ylabel('(Doanh thu(VND)')
     
        ax.set_title('Thống kê doanh thu theo tháng')
        # Format the y-axis labels
        fmt = ticker.StrMethodFormatter('{x:,.0f}')
        ax.yaxis.set_major_formatter(fmt)
        ax2 = ax.twinx()
        # Plot the bar chart
        ax2.bar(x1, y1, alpha=0.5, color='green', align='center')
        # ax2.set_ylabel('Bar chart', color='green')
        # ax2.tick_params('y', colors='green')

        image_path = os.path.join(base_dir, "static/doanhThuImg.png")
        fig.savefig(image_path)
        # context['doanhThuImg'] = InlineImage(doc, image_path)
        context['doanhThuImg'] = InlineImage(doc, image_path, width=Mm(150), height=Mm(100))
        # render context into the document object
        doc.render(context)

        # save the document object as a word file
        reportWordPath = 'reports/documents/report_month_{0}_{1}.docx'.format(startdate, enddate)
        output_path = os.path.join(base_dir, reportWordPath)
        doc.save(output_path)
        return output_path
    
    def download_file(self, **kwargs):
        a =kwargs['monthyear']
        report = Reports()  
        filepath = report.generate_template(a.split('_')[0],a.split('_')[1] )
        if os.path.exists(filepath ):
            with open(filepath , 'rb') as fh:
                response = HttpResponse(fh.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filepath )
                return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        startdate = self.request.GET.get("startdate")
        enddate= self.request.GET.get("enddate")
       
       
        monthyear = None
        error =  False
       
        # print(startdate, enddate)
        # print(type(startdate))
        if startdate is not None and enddate is not None:
            # syear ,smonth= startdate.split('-')
            # eyear, emonth  = enddate.split('-')
            # print(smonth, syear)
            # print(startdate < enddate )
            if startdate<= enddate:
                report = Reports()
                # try:
                file_path = report.generate_template(startdate, enddate)
                monthyear = startdate + "_"+enddate
                # except:
                #     error = True
            else:
                error = True
        else:
             error = True
        # if startmonth is not None and year is not None :
        #     if int(startmonth) <= int(endmonth) and int(endmonth) <= 12 and int(startmonth)>=1 :
        #         report = Reports()
        #         try:
        #             file_path = report.generate_template(startmonth,endmonth, year)
        #         except:
        #             error = True
        #         monthyear = str(startmonth)+"-"+str(endmonth)+"-"+str(year)
        #     else: 
        #         error = True
            
        # else: 
        #     error = True
        # print(error)
        context['monthyear'] = monthyear  
        context['startdate'] =  startdate
        context['enddate'] =  enddate
        # context['year'] = year
        context['error'] =  error
        return context