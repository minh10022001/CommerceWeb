from email.policy import default
from pickle import FALSE, TRUE
from turtle import position
from urllib import request
from django import forms
from django.forms import fields
from .models import *
from django.contrib.auth.models import User
import datetime
import requests
METHOD =(
    ("1", "Cash"),
    ("2", "Banking"),
    ("3", "QRCode")
)
METHOD_SHIPPING =(

     ("1", "Normal"),
    ("2", "Fast"),

)
class CheckoutForm(forms.ModelForm):
    customershippingaddress = forms.ModelChoiceField(queryset= CustomerShippingaddress.objects.all())
    paymentMethod = forms.CharField(label = "Payment Method", widget=forms.Select(choices=METHOD))
    shippingmethod = forms.CharField(label = "Shipping Method", widget=forms.Select(choices=METHOD_SHIPPING))
    class Meta:
        model = Order
        fields = ["customershippingaddress",
                  "paymentMethod", "shippingmethod"]
    # def __init__(self, user, *args, **kwargs):
    #     super(CheckoutForm, self).__init__(*args, **kwargs)
    #     customer = Customer.objects.get(userid__accountid__user = user)
    #     self.fields['shippingaddressid'].queryset = CustomerShippingaddress.objects.filter(customerid =customer)
    def __init__(self,user, *args, **kwargs): 
        # user = kwargs.pop('user', None) # pop the 'user' from kwargs dictionary      
        customer = Customer.objects.get(userid__accountid__user = user)
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields['customershippingaddress'].queryset = CustomerShippingaddress.objects.filter(customerid =customer)
class FeedBackForm(forms.ModelForm):
    content = forms.CharField(label = "Nội Dung", widget=forms.Textarea(attrs={'rows':2, 'cols':70,'class': "form-control",}))
    rating = forms.TypedChoiceField(choices=[(x, x) for x in range(1, 6)], coerce=int, help_text = 'Units: ')
    class Meta:
        model = Feedback
        fields = ["content", "rating"]

class ReviewForm(forms.ModelForm):
    content = forms.CharField(label = "Nội Dung", widget=forms.Textarea(attrs={'rows':6, 'cols':100}))
    class Meta:
        model = Customerreview
        fields = ["content"]

class ReplyReviewForm(forms.ModelForm):
    content = forms.CharField(label = "Nội Dung", widget=forms.Textarea(attrs={'rows':6, 'cols':100}))
    class Meta:
        model = Reviewreply
        fields = ["content"]

class EditProfileForm(forms.ModelForm):
    username = forms.CharField(label = "Tài Khoản",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000;',

                }))
    phonenumber = forms.CharField(label = "Số điện thoại",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    email = forms.CharField(label = "Email",widget=forms.EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    full_name = forms.CharField(label = "Họ tên",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    city = forms.CharField(label = "Thành phố/Tỉnh",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    district = forms.CharField(label = "Quận huyện",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    subdistrict = forms.CharField(label = "Phường xã",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    street = forms.CharField(label = "Phố/Làng",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }), required=False)
    description = forms.CharField(label = "Địa chỉ",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }), required= False)
    class Meta:
        model = Customer
        fields = ["username", "phonenumber", "email", "full_name", "city", "district","subdistrict", "street", "description"]

class ShippingAddressCreateForm(forms.ModelForm):
    city = forms.CharField(label = "Thành phố/Tỉnh",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000;',

                }))
    district = forms.CharField(label = "Quận huyện",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000;',

                }))
    subdistrict = forms.CharField(label = "Phường xã",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000;',

                }))
    street = forms.CharField(label = "Phố/Làng",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000;',

                }), required=False)
    description = forms.CharField(label = "Địa chỉ",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000;',

                }), required= False)
    phonenumberreceive = forms.CharField(label = "SĐT nhận hàng",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000;',

                }))
    class Meta:
        model = CustomerShippingaddress
        fields = ["city", "district","subdistrict", "street", "description","phonenumberreceive"] 

class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(label = "Tài Khoản",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000;',

                }))
    password = forms.CharField(label = "Mật Khẩu",widget=forms.PasswordInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    phonenumber = forms.CharField(label = "Số điện thoại",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    email = forms.CharField(label = "Email",widget=forms.EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    full_name = forms.CharField(label = "Họ tên",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    city = forms.CharField(label = "Thành phố/Tỉnh",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    district = forms.CharField(label = "Quận huyện",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    subdistrict = forms.CharField(label = "Phường xã",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    street = forms.CharField(label = "Phố/Làng",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }), required=False)
    description = forms.CharField(label = "Địa chỉ",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }), required= False)

    class Meta:
        model = Customer
        fields = ["username", "password", "phonenumber", "email", "full_name", "city", "district","subdistrict", "street", "description"]

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "Customer with this username already exists.")

        return uname
TYPE_STAFF =  (
    ("Manager", "Manager"),
    ("Sale Staff", "Sale Staff"),
    ("Warehouse Staff", "Warehouse Staff"),
    ("Business Staff", "Business Staff")
)
class StaffForm(forms.ModelForm):
    username = forms.CharField(label = "Tài Khoản",widget=forms.TextInput())
    password = forms.CharField(label = "Mật Khẩu",widget=forms.PasswordInput())
    phonenumber = forms.CharField(label = "Số điện thoại",widget=forms.TextInput())
    email = forms.CharField(label = "Email",widget=forms.EmailInput())
    full_name = forms.CharField(label = "Họ tên",widget=forms.TextInput())
    city = forms.CharField(label = "Thành phố/Tỉnh",widget=forms.TextInput())
    district = forms.CharField(label = "Quận huyện",widget=forms.TextInput())
    subdistrict = forms.CharField(label = "Phường xã",widget=forms.TextInput())
    street = forms.CharField(label = "Phố/Làng",widget=forms.TextInput(), required=False)
    description = forms.CharField(label = "Địa chỉ",widget=forms.TextInput(), required= False)
    codeStaff = forms.CharField(label = "Mã nhân viên", widget=forms.TextInput())
    position =forms.CharField(label = "Chức vụ", widget=forms.Select(choices=TYPE_STAFF))  # Field name made lowercase.
    salary =forms.FloatField(label = "Lương", widget=forms.NumberInput())  # Field name made lowercase.
    startdate =forms.DateField(label = "Ngày bắt đầu",widget=forms.DateInput())  # Field name made lowercase.
    workingtime =forms.IntegerField(label = "Thời gian làm việc trong tuần",widget=forms.NumberInput())  # Field name made lowercase.
    
    class Meta:
        model = Staffs
        fields = ["username", "password", "phonenumber", "email", "full_name", "city", "district","subdistrict", "street", "description","codeStaff","position","salary","startdate", "workingtime"]

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "Staff with this username already exists.")

        return uname
class EditStaffForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    phonenumber = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())
    full_name = forms.CharField(widget=forms.TextInput())
    city = forms.CharField(widget=forms.TextInput())
    district = forms.CharField(widget=forms.TextInput())
    subdistrict = forms.CharField(widget=forms.TextInput())
    street = forms.CharField(widget=forms.TextInput())
    description = forms.CharField(widget=forms.TextInput())
    codeStaff = forms.CharField(widget=forms.TextInput())
    position =forms.CharField(label = "Staff Type", widget=forms.Select(choices=TYPE_STAFF), disabled= False)  # Field name made lowercase.
    salary =forms.FloatField(widget=forms.NumberInput())  # Field name made lowercase.
    startdate =forms.DateField(widget=forms.DateInput())  # Field name made lowercase.
    workingtime =forms.IntegerField(widget=forms.NumberInput())  # Field name made lowercase.
    is_active = forms.BooleanField(required=False)
    class Meta:
        model = Staffs
        fields = ["username", "phonenumber", "email", "full_name", "city", "district","subdistrict", "street", "description", "position", "salary","startdate","workingtime", "is_active"]


TYPE =(
    ("1", "Clothes"),
    ("2", "Electronic"),
    ("3", "Book")
)

class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000;',

                }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000;',

                }))

class ProductForm(forms.ModelForm):
    # codeproduct = forms.CharField(label = "Product Code")
    producer = forms.ModelChoiceField(queryset= Producer.objects.all(), empty_label="-"*20)
    manufacturingyear = forms.IntegerField(widget=forms.NumberInput())
    name = forms.CharField(label = "Product Name")
    type = forms.CharField(label = "Product Type", widget=forms.Select(choices=TYPE))

    slug = forms.SlugField()
    description = forms.CharField()
    images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))

    class Meta:
        model = Item
        fields = ["producer", "manufacturingyear", "name", "type", "slug", "description", "images"]
class BookProductForm(forms.ModelForm):
    producer = forms.ModelChoiceField(queryset= Producer.objects.all(), empty_label="-"*20, required=False)
    manufacturingyear = forms.IntegerField(widget=forms.NumberInput())
    name = forms.CharField(label = "Product Name")
    numpage = forms.IntegerField(widget=forms.NumberInput())
    author = forms.CharField(label = "Author", widget=forms.TextInput())
    genre = forms.CharField(label = "Genre", widget=forms.TextInput())
    slug = forms.SlugField()
    description = forms.CharField()
    images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))


    class Meta:
        model = Item
        fields = ["producer", "manufacturingyear", "name","numpage","author","genre" ,"slug", "description", "images"]

class ClothesProductForm(forms.ModelForm):
    producer = forms.ModelChoiceField(queryset= Producer.objects.all(), empty_label="-"*20)
    manufacturingyear = forms.IntegerField(widget=forms.NumberInput())
    name = forms.CharField(label = "Product Name")
    clothtype = forms.CharField(label = "Clothes Type", widget=forms.TextInput())
    color = forms.CharField(label = "Color ", widget=forms.TextInput())
    gender = forms.CharField(label = "Gender", widget=forms.TextInput())
    brand = forms.CharField(label = " Brand", widget=forms.TextInput())
    material= forms.CharField(label = "Material", widget=forms.TextInput())
    slug = forms.SlugField()
    description = forms.CharField()
    images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))


    class Meta:
        model = Item
        fields = ["producer", "manufacturingyear", "name","clothtype","color","gender" ,"brand","material","slug", "description", "images"]
class ElectronicProductForm(forms.ModelForm):
    producer = forms.ModelChoiceField(queryset= Producer.objects.all(), empty_label="-"*20)
    manufacturingyear = forms.IntegerField(widget=forms.NumberInput())
    name = forms.CharField(label = "Product Name")
    devicetype = forms.CharField(label = "Device Type", widget=forms.TextInput())
    color = forms.CharField(label = "Color ", widget=forms.TextInput())
    weight = forms.CharField(label = "Weight", widget=forms.TextInput())
    brand = forms.CharField(label = " Brand", widget=forms.TextInput())
    size= forms.CharField(label = "Size", widget=forms.TextInput())
    power= forms.CharField(label = "Power", widget=forms.TextInput())
    slug = forms.SlugField()
    description = forms.CharField()
    images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))


    class Meta:
        model = Item
        fields = ["producer", "manufacturingyear", "name","devicetype","color","weight" ,"brand","size","power","slug", "description", "images"]
class EditProductForm(forms.ModelForm):
    # codeproduct = forms.CharField(label = "Product code")
    producer = forms.ModelChoiceField(queryset= Producer.objects.all(), empty_label="-"*20)
    name = forms.CharField(label = "Product Name")
    type = forms.CharField(label = "Product Type", widget=forms.Select(choices=TYPE))
    manufacturingyear = forms.IntegerField(widget=forms.NumberInput())
    # manufacturingdate = forms.IntegerField(initial=datetime.date.today)
    # expirydate = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = Product
        fields = ["producer", "name", "type", "manufacturingyear"]

class EditClothesProductForm(forms.ModelForm):
    producer = forms.ModelChoiceField(queryset= Producer.objects.all(), empty_label="-"*20)
    name = forms.CharField(label = "Product Name")
    # type = forms.CharField(label = "Product Type", widget=forms.Select(choices=TYPE))
    # type = forms.CharField(label = "Product Type",widget=forms.TextInput(), disabled= True, required= False )
    manufacturingyear = forms.IntegerField(widget=forms.NumberInput())
    clothtype = forms.CharField(label = "Clothes Type", widget=forms.TextInput())
    color = forms.CharField(label = "Color ", widget=forms.TextInput())
    gender = forms.CharField(label = "Gender", widget=forms.TextInput())
    brand = forms.CharField(label = " Brand", widget=forms.TextInput())
    material= forms.CharField(label = "Material", widget=forms.TextInput())

    class Meta:
        model = Clothes
        fields = ["producer", "name", "manufacturingyear","clothtype","color","gender" ,"brand","material"]

class EditElectronicProductForm(forms.ModelForm):
    producer = forms.ModelChoiceField(queryset= Producer.objects.all(), empty_label="-"*20)
    name = forms.CharField(label = "Product Name")
    # type = forms.CharField(label = "Product Type",widget=forms.TextInput(), disabled= True , required= True)
    # type = forms.CharField(label = "Product Type", widget=forms.Select(choices=TYPE))
    manufacturingyear = forms.IntegerField(widget=forms.NumberInput())
    devicetype = forms.CharField(label = "Device Type", widget=forms.TextInput())
    color = forms.CharField(label = "Color ", widget=forms.TextInput())
    weight = forms.CharField(label = "Weight", widget=forms.TextInput())
    brand = forms.CharField(label = " Brand", widget=forms.TextInput())
    size= forms.CharField(label = "Size", widget=forms.TextInput())
    power= forms.CharField(label = "Power", widget=forms.TextInput())
    class Meta:
        model = Electronic
        fields = ["producer", "name", "manufacturingyear","devicetype","color","weight" ,"brand","size","power"]

class EditBookProductForm(forms.ModelForm):
    producer = forms.ModelChoiceField(queryset= Producer.objects.all(), empty_label="-"*20)
    name = forms.CharField(label = "Product Name")  
    # type = forms.CharField(label = "Product Type",widget=forms.TextInput(), disabled= True , required= True)  
    # type = forms.CharField(label = "Product Type", widget=forms.Select(choices=TYPE))
    manufacturingyear = forms.IntegerField(widget=forms.NumberInput())
    numpage = forms.IntegerField(widget=forms.NumberInput())
    author = forms.CharField(label = "Author", widget=forms.TextInput())
    genre = forms.CharField(label = "Genre", widget=forms.TextInput())
    class Meta:
        model = Product
        fields = ["producer", "name", "manufacturingyear","numpage","author","genre"]

class EditItemForm(forms.ModelForm):
    price = forms.IntegerField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':50}))
    class Meta:
        model = Item
        fields= ["price", "description"]

class ImportProductForm(forms.ModelForm):
    supplier = forms.ModelChoiceField(queryset= Supplier.objects.all())
    # prodtype = forms.CharField(label = "Product Type", widget=forms.Select(choices=TYPE))
    product = forms.ModelChoiceField(queryset= Product.objects.all())
    number = forms.IntegerField()
    price = forms.IntegerField()
    # description = forms.CharField()
    # images = forms.FileField(required=False, widget=forms.FileInput(attrs={
    # "class": "form-control",
    # "multiple": True
    # }))
    class Meta:
        model = Importingrecord
        fields = ["supplier", "product", "number", "price"]

# class PasswordForgotForm(forms.Form):
#     email = forms.CharField(widget=forms.EmailInput(attrs={
#         "class": "form-control",
#         "placeholder": "Enter the email used in customer account..."
#     }))

#     def clean_email(self):
#         e = self.cleaned_data.get("email")
#         if Customer.objects.filter(userid__accountid__user__email=e).exists():
#             pass
#         else:
#             raise forms.ValidationError(
#                 "Customer with this account does not exists..")
#         return e


# class PasswordResetForm(forms.Form):
#     new_password = forms.CharField(widget=forms.PasswordInput(attrs={
#         'class': 'form-control',
#         'autocomplete': 'new-password',
#         'placeholder': 'Enter New Password',
#     }), label="New Password")
#     confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
#         'class': 'form-control',
#         'autocomplete': 'new-password',
#         'placeholder': 'Confirm New Password',
#     }), label="Confirm New Password")

#     def clean_confirm_new_password(self):
#         new_password = self.cleaned_data.get("new_password")
#         confirm_new_password = self.cleaned_data.get("confirm_new_password")
#         if new_password != confirm_new_password:
#             raise forms.ValidationError(
#                 "New Passwords did not match!")
#         return confirm_new_password
