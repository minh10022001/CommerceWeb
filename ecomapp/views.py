from asyncio.windows_events import NULL
from cgitb import reset
import email
from pickle import GET
# from turtle import position
from unicodedata import name
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from .utils import password_reset_token
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from .models import *
from .forms import *
import requests
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User

class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = get_object_or_404(Shoppingcart, id=cart_id)
            if request.user.is_authenticated and request.user.account:
                cart_obj.customerid = Customer.objects.get(userid__accountid = self.request.user.account)
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)

class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = request.user).exists() and Users.objects.filter(accountid__user = request.user, is_active = True).exists():
            pass
        else:
            return redirect("/login")
        return super().dispatch(request, *args, **kwargs)
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


class AllProductsView(EcomMixin, TemplateView):
    template_name = "allproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context
class BookProductsView(EcomMixin, TemplateView):
    template_name = "bookproducts.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Book.objects.count()>0:
            # productbook = Product.objects.get(type ="Book")
            # allbook = Item.objects.filter(productid = productbook  ).order_by("-id")
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

class ClothesProductsView(EcomMixin, TemplateView):
    template_name = "clothesproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Clothes.objects.count()>0:
            # productclothes = Product.objects.get(type ="Clothes")
            # allclothes = Item.objects.filter(productid =  productclothes ).order_by("-id")
            productclothes = Product.objects.filter(type ="Clothes").order_by("-id")
            allclothes =[]
            for clothes in productclothes:
                itemclothes = Item.objects.get(productid = clothes)
                allclothes.append(itemclothes)
        else: 
            allclothes = []
        paginator = Paginator(allclothes, 8)
        # all_products = Item.objects.all().order_by("-id")
        # paginator = Paginator(all_products, 8)
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

class ShippingAddressListView(View):
    template_name = "shippingaddresslist.html"
    def get(self, request, *args, **kwargs):
        cus_id = kwargs['cus_id']
        customer = Customer.objects.get(id = cus_id)
        shippingaddresslist = [customeraddress.shippingaddressid for customeraddress in CustomerShippingaddress.objects.filter(customerid = customer)]
        context = {"shippingaddresslist" : shippingaddresslist, "customer" : customer}
        return render(request, self.template_name, context)

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

# class AddToCartView(EcomMixin, TemplateView):
#     template_name = "addtocart.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # get product id from requested url
#         product_id = self.kwargs['pro_id']
#         # get product
#         product_obj = Item.objects.get(id=product_id)
#         if self.request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = self.request.user).exists():
#             customer = Customer.objects.get(userid__accountid__user = self.request.user)
#             # check if cart exists
#             cart_id = self.request.session.get("cart_id", None)
#             if cart_id:
#                 cart_obj = Shoppingcart.objects.get(id=cart_id)
#                 this_product_in_cart = Cartline.objects.filter(itemid = product_obj)

#                 # item already exists in cart
#                 if this_product_in_cart.exists():
#                     cartproduct = this_product_in_cart.last()
#                     cartproduct.num += 1
#                     cartproduct.save()
#                     cart_obj.save()
#                 # new item is added in cart
#                 else:
#                     cartproduct = Cartline.objects.create(
#                         shoppingcartid=cart_obj, itemid=product_obj, num=1)
#                     cart_obj.save()

#             else:
#                 if Shoppingcart.objects.filter(customerid = customer).exists():
#                     cart_obj = Shoppingcart.objects.get(customerid = customer)
#                 else:
#                     cart_obj = Shoppingcart.objects.create(customerid = customer)
#                 self.request.session['cart_id'] = cart_obj.id
#                 cartproduct = Cartline.objects.create(
#                     shoppingcartid=cart_obj, itemid=product_obj, num=1)
#                 cart_obj.save()
#             context["error"] = False
#         else:
#             context["error"] = True
#         return context

class AddToCartView( LoginRequiredMixin,EcomMixin, View):
    # template_name = "addtocart.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # get product id from requested url
    #     product_id = self.kwargs['pro_id']
    #     # get product
    #     product_obj = Item.objects.get(id=product_id)
    #     if self.request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = self.request.user).exists():
    #         customer = Customer.objects.get(userid__accountid__user = self.request.user)
    #         # check if cart exists
    #         cart_id = self.request.session.get("cart_id", None)
    #         if cart_id:
    #             cart_obj = Shoppingcart.objects.get(id=cart_id)
    #             this_product_in_cart = Cartline.objects.filter(itemid = product_obj)

    #             # item already exists in cart
    #             if this_product_in_cart.exists():
    #                 cartproduct = this_product_in_cart.last()
    #                 cartproduct.num += 1
    #                 cartproduct.save()
    #                 cart_obj.save()
    #             # new item is added in cart
    #             else:
    #                 cartproduct = Cartline.objects.create(
    #                     shoppingcartid=cart_obj, itemid=product_obj, num=1)
    #                 cart_obj.save()

    #         else:
    #             if Shoppingcart.objects.filter(customerid = customer).exists():
    #                 cart_obj = Shoppingcart.objects.get(customerid = customer)
    #                 this_product_in_cart = Cartline.objects.filter(itemid = product_obj)

    #                 # item already exists in cart
    #                 if this_product_in_cart.exists():
    #                     cartproduct = this_product_in_cart.last()
    #                     cartproduct.num += 1
    #                     cartproduct.save()
    #                     cart_obj.save()
    #                 # new item is added in cart
    #                 else:
    #                     cartproduct = Cartline.objects.create(
    #                         shoppingcartid=cart_obj, itemid=product_obj, num=1)
    #                     cart_obj.save()  
    #             else:
    #                 cart_obj = Shoppingcart.objects.create(customerid = customer)
    #                 self.request.session['cart_id'] = cart_obj.id
    #                 cartproduct = Cartline.objects.create(
    #                     shoppingcartid=cart_obj, itemid=product_obj, num=1)
    #                 cart_obj.save()
    #         context["error"] = False
    #     else:
    #         context["error"] = True
    #     # return redirect("ecomapp:mycart")
    #     return context
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


# class EmptyCartView(EcomMixin, View):
#     def get(self, request, *args, **kwargs):
#         cart_id = request.session.get("cart_id", None)
#         if cart_id:
#             cart = Shoppingcart.objects.get(id=cart_id)
#             [cartline.delete() for cartline in Cartline.objects.filter(shoppingcartid = cart)]
#             cart.save()
#         return redirect("ecomapp:mycart")

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


# class CheckoutView(EcomMixin, CreateView ):
#     template_name = "checkout.html"
#     # def sample_view(request):
#     #     current_user = request.user
#     #     return current_user.id
#     # print(sample_view(request))
#     form_class = CheckoutForm

#     success_url = reverse_lazy("ecomapp:home")
#     # def get_form(self, request):
#     #         # if form_class is None:
#     #         #     form_class = self.get_form_class()
#     #         #     return form_class(**self.get_form_kwargs(),current_user_profile=get_profile(self.request.user))
#     #         return self.request.user
#     # user = get_form()
#     def get_form_kwargs(self):
#         kwargs = super(CheckoutView, self).get_form_kwargs()
#         # kwargs['user'] = self.request.user # pass the 'user' in kwargs
#         kwargs.update({'user': self.request.user})
#         return kwargs
#     def dispatch(self, request, *args, **kwargs):
#         if not (request.user.is_authenticated and request.user.account):
#             return redirect("/login/?next=/checkout/")
#         return super().dispatch(request, *args, **kwargs)
#     def get_context_data(self, **kwargs):
     
#         context = super().get_context_data(**kwargs)
#         cart_id = self.request.session.get("cart_id", None)
#         # cart_obj = Shoppingcart.objects.get(id=cart_id) if cart_id else None
#         customer = Customer.objects.get(userid__accountid__user = self.request.user)
#         cart_obj = Shoppingcart.objects.get(id=cart_id) if cart_id else Shoppingcart.objects.get(customerid =customer)
#         context['cart'] = cart_obj
#         return context
#     def form_valid(self,form):
#         # template_name = "checkout.html"
#         # # form_class = CheckoutForm()
#         # success_url = reverse_lazy("ecomapp:home")
#         # form  = CheckoutForm(request.user)
#         cart_id = self.request.session.get("cart_id")
#         if cart_id:
#             customer = Customer.objects.get(userid__accountid__user = self.request.user)
#             cart_obj = Shoppingcart.objects.get(id=cart_id)
#             cartlines = cart_obj.cartline_set.all()
#             if Orderhistory.objects.filter(customerid__userid__accountid__user = self.request.user).exists():
#                 orderhistory = Orderhistory.objects.get(customerid__userid__accountid__user = self.request.user)
#             else:
#                 orderhistory = Orderhistory.objects.create(customerid = customer)
            
#             method = form.cleaned_data.get("paymentMethod")
#             method_shipping = form.cleaned_data.get("shippingmethod")
#             convert ={"1": "Cash",
#                       "2": "Banking",
#                       "3": "QRCode"}
#             convert_shipping ={"1": "Normal",
#                       "2": "Fast",
#             }
#             customershippingaddress  =form.cleaned_data.get("customershippingaddress")
#             print("----------------------------------------",customershippingaddress)
#             shippingaddressid  = customershippingaddress.shippingaddressid
#             payment = Payment.objects.create(isComplete = False, method = convert[method])
#             methodshipping = convert_shipping[method_shipping]
#             form.instance.customerid = customer
#             form.instance.paymentid = payment
#             form.instance.shippingaddressid = shippingaddressid
#             form.instance.status = "Order Received"
#             form.instance.time = datetime.datetime.now()
#             form.instance.shippingmethod = methodshipping
#             order = form.save()
#             historyline = Historyline.objects.create(orderhistoryid = orderhistory, orderid = order)
#             historyline.save()
#             for cartline in cartlines:
#                 orderitem = Orderitem.objects.create(orderid = order, itemid = cartline.itemid, count = cartline.num)
#                 orderitem.save()
#                 cartline.delete()
#         else:
#             return redirect("ecomapp:home")
#         return super().form_valid(form)

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
        # cart_obj = Shoppingcart.objects.get(id=cart_id) if cart_id else None
        customer = Customer.objects.get(userid__accountid__user = self.request.user)
        cart_obj = Shoppingcart.objects.get(id=cart_id) if cart_id else Shoppingcart.objects.get(customerid =customer)
        context['cart'] = cart_obj
        return context
    def form_valid(self,form):
        # template_name = "checkout.html"
        # # form_class = CheckoutForm()
        # success_url = reverse_lazy("ecomapp:home")
        # form  = CheckoutForm(request.user)
        cart_id = self.request.session.get("cart_id")
        # if cart_id:
        customer = Customer.objects.get(userid__accountid__user = self.request.user)
        # cart_obj = Shoppingcart.objects.get(id=cart_id)
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
        # else:
        #     return redirect("ecomapp:home")
        return super().form_valid(form)
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


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecomapp:home")

class ReviewSuccessView(TemplateView):
    template_name = "reviewsuccess.html"
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

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


class AboutView(EcomMixin, TemplateView):
    template_name = "about.html"


class ContactView(EcomMixin, TemplateView):
    template_name = "contactus.html"


class CustomerProfileView(TemplateView):
    template_name = "customerprofile.html"
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     kw = self.request.GET.get("keyword")
    #     results = Item.objects.filter(
    #         Q(productid__name__icontains=kw) | Q(description__icontains=kw))
    #     context["results"] = results
    #     return context
         
    #     kw = self.request.GET.get("keyword")
    #     if kw is not None:
    #         queryset = Product.objects.filter(
    #             Q(id__icontains=kw) | Q(name__icontains=kw))
    #     else:
    #         queryset = Product.objects.all().order_by("-id")
    #    context["allproducts"] = queryset
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
        # context["results"] = results
        else:
            orders = Order.objects.filter(customerid=customer).order_by("-id")
        context["orders"] = orders
        return context

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
         

class ReviewListView(TemplateView):
    template_name = "reviewlist.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(userid__accountid = self.request.user.account)
        reviews = Customerreview.objects.filter(customerid = customer)
        context['reviews'] = reviews
        return context

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


class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Item.objects.filter(
            Q(productid__name__icontains=kw) | Q(description__icontains=kw))
        context["results"] = results
        return context


# class PasswordForgotView(FormView):
#     template_name = "forgotpassword.html"
#     form_class = PasswordForgotForm
#     success_url = "/forgot-password/?m=s"
#     # contactinfo = Contactinfo.objects.get(email =  "minh0353845565@gmail.com")

#     # users = Users.objects.get(contactinfoid =contactinfo)
#     # # customer = Customer.objects.get(userid = users)
#     # print(customer.id)
#     def form_valid(self, form):
#         # get email from user
#         email = form.cleaned_data.get("email")
#         print(email)
#         # get current host ip/domain
#         url = self.request.META['HTTP_HOST']
#         # get customer and then user
#         # print("--------------------")
#         # customer = Customer.objects.get(userid_contactinfoid_email=email)
#         contactinfo = Contactinfo.objects.get(email = email)
#         users = Users.objects.get(contactinfoid =contactinfo)
#         customer = Customer.objects.get(userid = users)
#         print(customer.id)
#         user = customer.userid
#         # send mail to the user with email
#         text_content = 'Please Click the link below to reset your password. '
#         html_content = url + "/password-reset/" + email + \
#             "/" + password_reset_token.make_token(user) + "/"
#         send_mail(
#             'Password Reset Link | Django Ecommerce',
#             text_content + html_content,
#             settings.EMAIL_HOST_USER,
#             [email],
#             fail_silently=False,
#         )
#         return super().form_valid(form)


# class PasswordResetView(FormView):
#     template_name = "passwordreset.html"
#     form_class = PasswordResetForm
#     success_url = "/login/"

#     def dispatch(self, request, *args, **kwargs):
#         email = self.kwargs.get("email")
#         user = User.objects.get(email=email)
#         token = self.kwargs.get("token")
#         if user is not None and password_reset_token.check_token(user, token):
#             pass
#         else:
#             return redirect(reverse("ecomapp:passworforgot") + "?m=e")

#         return super().dispatch(request, *args, **kwargs)

#     def form_valid(self, form):
#         password = form.cleaned_data['new_password']
#         email = self.kwargs.get("email")
#         user = User.objects.get(email=email)
#         user.set_password(password)
#         user.save()
#         return super().form_valid(form)

# # admin pages
class AdminLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecomapp:adminhome")

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


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Staffs.objects.filter(userid__accountid__user = request.user).exists() and Users.objects.filter(accountid__user = request.user, is_active = True).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


# class AdminHomeView(AdminRequiredMixin, TemplateView):
#     # if Staffs.objects.filter(position = 'Manager'):
#     #     template_name =  "adminpages/manager/managehome.html"
       
#     # else:
#     template_name = "adminpages/adminhome.html"
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["pendingorders"] = Order.objects.filter(
#             status="Order Received").order_by("-id")
#         return context
class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminhome.html"
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["pendingorders"] = Order.objects.filter(
    #         status="Order Received").order_by("-id")
    #     # position = ""
    #     # if Staffs.objects.get(userid__accountid__user = request.user).exists():
    #     #     staff = Staffs.objects.get(userid__accountid__user = request.user)
    #     #     position = staff.position
    #     # else:
    #     #     position = "Null"
    #     # context['position'] = self.get_abc()
    #     return context
class AdminPendingOrder(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminpendingorders.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(
            status="Order Received").order_by("-id")
        # position = ""
        # if Staffs.objects.get(userid__accountid__user = request.user).exists():
        #     staff = Staffs.objects.get(userid__accountid__user = request.user)
        #     position = staff.position
        # else:
        #     position = "Null"
        # context['position'] = self.get_abc()
        return context
class AdminStaffListView(AdminRequiredMixin, TemplateView):
    # if Staffs.objects.filter(position = "Manager"):
    template_name = "adminpages/stafflist.html"
    # else:
    #     template_name = "adminpages/404.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        if kw is not None:
            queryset = Staffs.objects.filter(
                Q(codeStaff__icontains=kw) | Q(position__icontains=kw))
        else:
            # queryset = Staffs.objects.all().order_by("-id")
            queryset = Staffs.objects.all()
        context["allstaffs"] = queryset
        return context
class AdminStaffCreateView(AdminRequiredMixin, CreateView):
    # if Staffs.objects.filter(position = "Manager"):
    #     template_name = "adminpages/stafflist.html"
    # else:
    #     template_name = "adminpages/404.html"
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
        # login(self.request, user.accountid.user)
        return super().form_valid(form)

    # def get_success_url(self):
    #     if "next" in self.request.GET:
    #         next_url = self.request.GET.get("next")
    #         return next_url
    #     else:
    #         return self.success_url
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
           
           

            # form.instance.userid  = staff.userid
        #     context = {"staff" : Staffs.objects.get(userid = staff.userid )}
        # return render(request, self.template_name, context)
        return redirect("/admin-staff/list/")

# class AdminProductDetailView(View):
#     template_name = "adminpages/adminproductdetail.html"

#     def get(self, request, *args, **kwargs):
#         form = EditProductForm()
#         pro_id = kwargs['pro_id']
#         product = Product.objects.get(id=pro_id)
#         if product.type ==  'Clothes':
#             form = EditProductForm()
#         elif product.type ==  'Electronic':
#             form = EditProductForm()
#         elif  product.type ==  'Electronic':
#             form = EditProductForm()
#         form.fields['producer'].initial  = product.producerid
#         form.fields['name'].initial  = product.name
#         form.fields['manufacturingyear'].initial  = product.manufacturingyear
#         # form.fields['expirydate'].initial  = product.expirydate
#         convert = {
#                 "Clothes":"1",
#                 "Electronic":"2",
#                 "Book":"3"
#             }
#         form.fields['type'].initial  = convert[product.type]

#         context = {'form': form, "product": product}
#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         form = EditProductForm(data=request.POST)
#         if form.is_valid():
#             producer = form.cleaned_data['producer']
#             name = form.cleaned_data['name']
#             manufacturingyear = form.cleaned_data['manufacturingyear']
#             # expirydate = form.cleaned_data['expirydate']
#             type = form.cleaned_data['type']

#             pro_id = kwargs['pro_id']
#             product = Product.objects.get(id=pro_id)
#             product.producer = producer
#             product.name = name
#             product.manufacturingyear = manufacturingyear
#             # product.expirydate = expirydate
#             convert = {
#                 "1": "Clothes",
#                 "2": "Electronic",
#                 "3": "Book"
#             }
#             product.type = convert[type]
#             product.save()

#             form.fields['producer'].initial  = product.producerid
#             form.fields['name'].initial  = product.name
#             form.fields['manufacturingyear'].initial  = product.manufacturingyear
#             # form.fields['expirydate'].initial  = product.expirydate
#             form.fields['type'].initial  = product.type

#             context = {'form': form, "product": product}
#         return render(request, self.template_name, context)
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
            # type = form.cleaned_data['type']

            # pro_id = kwargs['pro_id']
            product = Product.objects.get(id=pro_id)
            product.producer = producer
            product.name = name
            product.manufacturingyear = manufacturingyear
           
            # product.expirydate = expirydate
            # convert = {
            #     "1": "Clothes",
            #     "2": "Electronic",
            #     "3": "Book"
            # }
            # product.type = type
            product.save()

            form.fields['producer'].initial  = product.producerid
            form.fields['name'].initial  = product.name
            form.fields['manufacturingyear'].initial  = product.manufacturingyear
            # form.fields['type'].initial  = product.type
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

class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = "adminpages/adminorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context

class AdminOrderListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminorderlist.html"
    queryset = Order.objects.all().order_by("-id")
    context_object_name = "allorders"

class AdminReviewListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminreviewlist.html"
    queryset = Customerreview.objects.all().order_by("-id")
    context_object_name = "allreviews"

class AdminReviewDetailView(AdminRequiredMixin, DetailView):
    template_name = "adminpages/adminreviewdetail.html"
    model = Customerreview
    context_object_name = "rv_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session["review_id"] = context['rv_obj'].id
        return context

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

class AdminOrderStatusChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.status = new_status
        order_obj.save()
        return redirect(reverse_lazy("ecomapp:adminorderdetail", kwargs={"pk": order_id}))

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
        context["allproducts"] = queryset
        return context

class AdminImprotingrecordListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminimportingrecordlist.html"
    queryset = Importingrecord.objects.all().order_by("-id")
    context_object_name = "allrecords"

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

class AdminItemDeleteView(AdminRequiredMixin, View):
    template_name = "adminpages/adminproductlist.html"
    def get(self, request, *args, **kwargs):
        queryset = Item.objects.all().order_by("-id")
        pro_id = self.kwargs["pro_id"]
        item = Item.objects.get(id = pro_id)
        item.productid.delete()
        context = {"allproducts":queryset}
        return render(request, self.template_name, context)


# class AdminProductCreateView(AdminRequiredMixin, CreateView):
#     template_name = "adminpages/adminproductcreate.html"
#     form_class = ProductForm
#     success_url = reverse_lazy("ecomapp:adminproductlist")

#     def form_valid(self, form):
#         # codeproduct =  form.cleaned_data.get("codeproduct")
#         producer = form.cleaned_data.get("producer")
#         manufacturingyear = form.cleaned_data.get("manufacturingyear")
#         # expirydate = form.cleaned_data.get("expirydate")
#         name = form.cleaned_data.get("name")
#         prod_type = form.cleaned_data.get("type")
#         slug = form.cleaned_data.get("slug")
#         description = form.cleaned_data.get("description")
#         convert = {
#             "1": "Clothes",
#             "2": "Electronic",
#             "3": "Book"
#         }
#         p = Product.objects.create(producerid = producer, manufacturingyear = manufacturingyear,
#                                     type = convert[prod_type], name = name)
#         images = self.request.FILES.getlist("images")
#         # Item.objects.create(productid= p, slug = slug,   image = images[0], description = description)
#         ProductCategory.objects.create(categoryid = Category.objects.get(name = convert[prod_type]), productid = p)
       
#         form.instance.productid = p
#         form.instance.description = description
#         form.instance.slug = slug
#         form.instance.image = images[0]
#         return super().form_valid(form)
class AdminProductCreateView(AdminRequiredMixin, View):
    template_name = "adminpages/adminproductcreate.html"
    
    # if 1>2:
    #     form_class = ClothesProductForm
    # else:
    #     form_class = BookProductForm
    # success_url = reverse_lazy("ecomapp:adminproductlist")
  
    # def form_valid(self, form,*args, **kwargs):
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
    
class Statistic(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/statistic.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(
            status="Order Received").order_by("-id")
        # position = ""
        # if Staffs.objects.get(userid__accountid__user = request.user).exists():
        #     staff = Staffs.objects.get(userid__accountid__user = request.user)
        #     position = staff.position
        # else:
        #     position = "Null"
        # context['position'] = self.get_abc()
        return context