# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# classes are used for User
class Account(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    user = models.OneToOneField(User, on_delete=models.CASCADE,  null=True)
    date_create = models.DateField(db_column='Date_created', blank=True, null=True)
    # gender = models.CharField(db_column='Gender', max_length=255, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        
        db_table = 'account'

class Users(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    dateofbirth = models.DateField(db_column='DateOfBirth', blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=255, blank=True, null=True)  # Field name made lowercase.
    accountid = models.OneToOneField('Account', models.CASCADE, db_column='AccountID', blank=True, null=True)
    contactinfoid = models.OneToOneField('ContactInfo', models.CASCADE, db_column='ContactInfoID', blank=True, null=True)
    fullnameid = models.OneToOneField('FullName', models.CASCADE, db_column='FullNameID', blank=True, null=True)
    addressid = models.OneToOneField('Address', models.CASCADE, db_column='AddressID', blank=True, null=True)
    is_active = models.BooleanField(db_column='IsAcitve', default= True)

    class Meta:
        
        db_table = 'users'
class Address(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=255, blank=True, null=True)  # Field name made lowercase.
    district = models.CharField(db_column='District', max_length=255, blank=True, null=True)  # Field name made lowercase.
    subdistrict = models.CharField(db_column='Town', max_length=255, blank=True, null=True)  # Field name made lowercase.
    street = models.CharField(db_column='Street', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    # user  = models.ForeignKey(Users, on_delete=models.CASCADE)
    class Meta:
        
        db_table = 'address'
    
    def __str__(self):
        return f"{self.description} {self.street} {self.subdistrict} {self.district} {self.city}"

    @property
    def address(self):
        return f"{self.description} {self.street} {self.subdistrict} {self.district} {self.city}"

class Fullname(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    middlename = models.CharField(db_column='MiddleName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'fullname'

    @property
    def fullname(self):
        return f"{self.firstname} {self.middlename} {self.lastname}"
 
    def __str__(self):
        return f"{self.firstname} {self.middlename} {self.lastname}"
class Contactinfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'contactinfo'


#class Customer
class Customer(models.Model):
        id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
        userid = models.OneToOneField("Users", models.CASCADE, db_column='CustomerID', blank=True, null=True)
        typecustomer = models.CharField(db_column='TypeCustomer', max_length=255, blank=True, null=True) 
        class Meta:
            db_table = 'customer'

        @property
        def count_item_cart(self):
            if Shoppingcart.objects.filter(customerid = self.id) ==None:
                return 0
            else:
                cart = Shoppingcart.objects.get(customerid = self.id)
                count = 0
                if Cartline.objects.filter(shoppingcartid  =cart) ==  None:
                    return 0
                else:
                    cartlinelist = Cartline.objects.filter(shoppingcartid  =cart)
                    for cartline in cartlinelist:
                        count+=1
                    return count
        @property
        def count_wishline(self):
            if Wishlist.objects.filter(customerid = self.id) ==None:
                return 0
            else:
                wishlist = Wishlist.objects.get(customerid = self.id)
                count = 0
                if Wishlistline.objects.filter(wishlistid  = wishlist) ==  None:
                    return 0
                else:
                    wishlinelist = Wishlistline.objects.filter(wishlistid  =wishlist)
                    for wishline in wishlinelist:
                        count+=1
                    return count

# classes are usef for Staff
class Staffs(models.Model):
    codeStaff = models.CharField(db_column='codeStaff', max_length=255,unique=True) 
    position = models.CharField(db_column='Position', max_length=255, blank=True, null=True)  # Field name made lowercase.
    salary = models.BigIntegerField(db_column='Salary', blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    workingtime = models.IntegerField(db_column='WorkingTime', blank=True, null=True)  # Field name made lowercase.
    userid = models.OneToOneField('Users', models.CASCADE, db_column='UsersID', primary_key=True)  # Field name made lowercase.
    # userid = models.OneToOneField('Users', models.CASCADE, db_column='UsersID',blank=True, null=True)
    class Meta:
        
        db_table = 'staffs'

class Businessstaff(models.Model):
    numproductprocessed = models.IntegerField(db_column='NumProductProcessed', blank=True, null=True)  # Field name made lowercase.
    staffid = models.OneToOneField('Staffs', models.CASCADE, db_column='StaffID', primary_key=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'businessstaff'

class Warehousestaff(models.Model):
    numbills = models.IntegerField(db_column='NumBills', blank=True, null=True)  # Field name made lowercase.
    staffid = models.OneToOneField('Staffs', models.CASCADE, db_column='StaffID', primary_key=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'warehousestaff'

class Salesstaff(models.Model):
    numorderprocessed = models.IntegerField(db_column='NumOrderProcessed', blank=True, null=True)  # Field name made lowercase.
    staffid = models.OneToOneField('Staffs', models.CASCADE, db_column='StaffID', primary_key=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'salesstaff'

class Manager(models.Model):
    numstaffcreated = models.IntegerField(db_column='NumStaffCreated', blank=True, null=True)
    numproductprocessed = models.IntegerField(db_column='NumProductProcessed', blank=True, null=True)
    numbills = models.IntegerField(db_column='NumBills', blank=True, null=True)
    numorderprocessed = models.IntegerField(db_column='NumOrderProcessed', blank=True, null=True)
    description  = models.CharField(db_column='Description', max_length=255, blank=True, null=True)
    staffid = models.OneToOneField('Staffs', models.CASCADE, db_column='StaffID', primary_key=True)  # Field name made lowercase.
    class Meta:
        
        db_table = 'manager'

#classes are used for Product
class Producer(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'producer'
    
    def __str__(self):
        return self.name

class Supplier(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'supplier'

    def __str__(self) -> str:
        return self.name
class Category(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique = True, max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'category'

class Product(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) 
    producerid = models.ForeignKey(Producer, models.CASCADE, db_column='ProducerID')  # Field name made lowercase.
    manufacturingyear = models.IntegerField(db_column='ManufacturingYear', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=255, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    num = models.IntegerField(db_column='Number', default=0)

    class Meta:
        
        db_table = 'product'

    def __str__(self) -> str:
        return str(self.id) +"-"+ self.name
    
    @property
    def category(self):
        return ProductCategory.objects.get(productid = self).categoryid.name
class ProductCategory(models.Model):
    productid = models.OneToOneField(Product, models.CASCADE, db_column='ProductID', primary_key=True)  # Field name made lowercase.
    categoryid = models.ForeignKey(Category, models.CASCADE, db_column='CategoryID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'product_category'
        unique_together = (('productid', 'categoryid'),)

class Book(models.Model):
    numpage = models.IntegerField(db_column='Page', blank=True, null=True)  # Field name made lowercase.
    author = models.CharField(db_column='Author', max_length=255, blank=True, null=True)
    productid = models.OneToOneField('Product', models.CASCADE, db_column='ProductID', primary_key=True)  # Field name made lowercase.
    genre = models.CharField(db_column='Genre', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'book'

class Clothes(models.Model):
    clothtype = models.CharField(db_column='ClothType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=255, blank=True, null=True)  # Field name made lowercase.
    brand = models.CharField(db_column='Brand', max_length=255, blank=True, null=True)  # Field name made lowercase.
    material = models.CharField(db_column='Material', max_length=255, blank=True, null=True)  # Field name made lowercase.
    productid = models.OneToOneField('Product', models.CASCADE, db_column='ProductID', primary_key=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'clothes'

class Electronic(models.Model):
    devicetype = models.CharField(db_column='DeviceType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=255, blank=True, null=True)  # Field name made lowercase.
    brand = models.CharField(db_column='Brand', max_length=255, blank=True, null=True)  # Field name made lowercase.
    weight = models.CharField(db_column='Weight', max_length=255, blank=True, null=True)  # Field name made lowercase.
    power = models.CharField(db_column='Power', max_length=255, blank=True, null=True)  # Field name made lowercase.
    size = models.CharField(db_column='Size', max_length=255, blank=True, null=True)  # Field name made lowercase.
    productid = models.OneToOneField('Product', models.CASCADE, db_column='ProductID', primary_key=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'electronic'


class Item(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    productid = models.ForeignKey('Product', models.CASCADE, db_column='ProductID')  # Field name made lowercase.
    price = models.BigIntegerField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="products/images/")
    isUpload = models.BooleanField(default=False)

    class Meta:
        
        db_table = 'item'
    @property
    def count_review(self):
        all_feedback =  Feedback.objects.filter(itemid = self.id)
        if all_feedback ==None:
            return 0
        else: 
            return len(all_feedback)

    @property
    def avg_rating(self):
        all_feedback =  Feedback.objects.filter(itemid = self.id)
        if all_feedback ==None:
            return 0
        elif len(all_feedback)==0:
            return 0
        else: 
            sum =0 
            for feedback in all_feedback:
                sum += feedback.rate
            return round(sum/len(all_feedback),2)
    def __str__(self) -> str:
        return self.productid.name

class Feedback(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    itemid = models.ForeignKey('Item', models.CASCADE, db_column='ItemID')  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.CASCADE, db_column='CustomerID')  # Field name made lowercase.
    rate = models.IntegerField(db_column='Rate', validators = [MinValueValidator(0), MaxValueValidator(5)])  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'feedback'
    
    @property
    def relevant(self):
        text = self.content.lower()
        if "giao hàng" in text or "đóng gói" in text or "nhân viên" in text:
            return "non-relevant"
        return "relevant"

class Historyline(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    orderhistoryid = models.ForeignKey('Orderhistory', models.CASCADE, db_column='OrderHistoryID')  # Field name made lowercase.
    orderid = models.ForeignKey('Order', models.CASCADE, db_column='OrderID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'historyline'

class Orderhistory(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.CASCADE, db_column='CustomerID')  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'orderhistory'

class Orderitem(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    orderid = models.ForeignKey("Order", models.CASCADE, db_column='OrderID')  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)
    itemid = models.ForeignKey(Item, models.CASCADE, db_column='ItemID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'orderitem'

    @property
    def subTotal(self):
        return self.count*self.itemid.price
class Shippingaddress(models.Model):
    id = models.AutoField(db_column='ID',  blank=True, null=False,primary_key=True)  # Field name made lowercase.
    addressid = models.ForeignKey('Address', models.CASCADE, db_column='AddressID', blank=True, null=True)
    phonenumberreceive = models.CharField(db_column='PhoneNumberReceive', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'shippingaddress'    
    def __str__(self) -> str:
        return str(self.addressid.address) +"-"+ self.phonenumberreceive 
    @property
    def address(self):
        return self.addressid.address


class CustomerShippingaddress(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True ) 
    customerid = models.ForeignKey(Customer, models.CASCADE, db_column='CustomerID')  # Field name made lowercase.
    shippingaddressid = models.ForeignKey('Shippingaddress', models.CASCADE, db_column='ShippingAddressID' )  # Field name made lowercase.

    class Meta:
        
        db_table = 'customer_shippingaddress'
        # unique_together = (('customerid', 'shippingaddressid'))  
    def __str__(self):
        return f"{self.shippingaddressid.address}"
class Order(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    paymentid = models.ForeignKey('Payment', models.CASCADE, db_column='PaymentID')  # Field name made lowercase.
    # addressid = models.ForeignKey('Address', models.CASCADE, db_column='AddressID', blank=True, null=True)
    customerid = models.ForeignKey(Customer, models.CASCADE, db_column='CustomerID')  # Field name made lowercase.
    shippingaddressid = models.ForeignKey('Shippingaddress', models.CASCADE, db_column='ShippingAddressID',blank=True, null=True)
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=255, blank=True, null=True)  # Field name made lowercase.
    date_shipping = models.DateField(db_column='DateShipping', blank=True, null=True) 
    delayshipnote = models.CharField(db_column='DelayShipNote', max_length=255, blank=True, null=True)
    shippingmethod = models.CharField(db_column='ShippingMethod', max_length=255, blank=True, null=True)
    class Meta:
        
        db_table = 'order'

    @property
    def cost_all_items(self):
        sum = 0
        for orderitem in Orderitem.objects.filter(orderid__id = self.id):
            sum += orderitem.count * orderitem.itemid.price
        return sum
    @property
    def cost_shipping(self):
        costship = 0
        if self.cost_all_items >= 500000:
            costship  = 0
        else:
            if self.shippingmethod =='Fast':
                costship  = 20000
            elif self.shippingmethod =='Normal':
                costship =  10000
        return costship
    @property
    def total(self):
        sum = self.cost_all_items+ self.cost_shipping
        return sum

class Payment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    isComplete = models.BooleanField(blank=True, null=True)
    method = models.CharField(db_column='Method', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'payment'

    def __str__(self):
        return self.method
class Cartline(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    itemid = models.ForeignKey('Item', models.CASCADE, db_column='ItemID')  # Field name made lowercase.
    num = models.IntegerField(db_column='Num', blank=True, null=True)  # Field name made lowercase.
    shoppingcartid = models.ForeignKey('Shoppingcart', models.CASCADE, db_column='ShoppingCartID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'cartline'

    @property
    def sumPrice(self):
        return (self.num * self.itemid.price)


class Customerreview(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.CASCADE, db_column='CustomerID')  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=255, blank=True, null=True)  # Field name made lowercase.
    reviewtime = models.TimeField(db_column='ReviewTime', blank=True, null=True)  # Field name made lowercase.
    isReply = models.BooleanField(default=False)

    class Meta:
        
        db_table = 'customerreview'

    @property
    def sentiment(self):
        return "NEGATIVE"
        # translate_text = translator.translate(self.content, lang_tgt='en')  
        # sentence=flair.data.Sentence(translate_text)
        # flair_sentiment.predict(sentence)
        # total_sentiment = sentence.labels
        # return total_sentiment[0].value

class Reviewreply(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    message = models.CharField(db_column='Message', max_length=255, blank=True, null=True)  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    customerreviewid = models.ForeignKey(Customerreview, models.CASCADE, db_column='CustomerreviewID', blank=True, null=True)  # Field name made lowercase.
    staffid = models.ForeignKey('Staffs', models.CASCADE, db_column='SalesStaffUsersID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'reviewreply'


class Wishlist(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.CASCADE, db_column='CustomerID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'wishlist'


class Wishlistline(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    itemid = models.ForeignKey(Item, models.CASCADE, db_column='ItemID', blank=True, null=True)
    wishlistid = models.ForeignKey(Wishlist, models.CASCADE, db_column='WishListID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'wishlistline'

class Importingrecord(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    supplierid = models.ForeignKey('Supplier', models.CASCADE, db_column='SupplierID')  # Field name made lowercase.
    productid = models.ForeignKey('Product', models.CASCADE, db_column='ProductID')  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    staffid = models.ForeignKey('Staffs', models.CASCADE, db_column='StaffID')  # Field name made lowercase.
    num = models.IntegerField(db_column='Num', blank=True, null=True)
    price = models.IntegerField(db_column='Price', blank=True, null=True)

    class Meta:
        
        db_table = 'importingrecord'

    @property
    def total(self):
        return self.price*self.num


ORDER_STATUS = (
    ("Đã tiếp nhận đơn hàng", "Đã tiếp nhận đơn hàng"),
    ("Đơn hàng đang được xử lý", "Đơn hàng đang được xử lý"),
    ("Đơn hàng đang được giao", "Đơn hàng đang được giao"),
    ("Đơn hàng đã hoàn thành", "Đơn hàng đã hoàn thành"),
    ("Đơn hàng đã bị huỷ", "Đơn hàng đã bị huỷ"),
)


class Shoppingcart(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.CASCADE, db_column='CustomerID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'shoppingcart'
    
    @property
    def total(self):
        s = 0
        for cartline in Cartline.objects.filter(shoppingcartid__id = self.id):
            s += cartline.sumPrice
        return s





