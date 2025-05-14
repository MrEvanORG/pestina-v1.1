from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=20,verbose_name='نام کاربر')
    last_name = models.CharField(max_length=20,verbose_name='نام خانوادگی کاربر')
    phone_number = models.CharField(max_length=15,primary_key=True,verbose_name='شماره تلفن کاربر')
    is_verified = models.BooleanField(default=False,verbose_name='وضعیت تایید شدن شماره تلغن')
    ip_address = models.GenericIPAddressField(null=True,blank=True,verbose_name='آیپی کاربر هنگام ثبت نام')
    register_time = models.DateTimeField(auto_now=True,verbose_name='زمان ثبت نام')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Product(models.Model):

    class ptype(models.TextChoices):
        AKBARI = "akbari","اکبری"
        FANDOGHI = "fandoghi","فندوقی"
        AHMADAGHAII = "ahmadaghaii","احمد آقایی"
        KALE_GHOOCHI = 'kaleghoochi','کله قوچی'
        SHAHPASAND = 'shahpasand','شاه پسند'
        SEPID = 'sefid','سفید'
        BADAMI = 'badami','بادامی'
        KHANJARI = 'khanjari','خنجری'
        MAKHLOOT = 'makhloot',' مخلوط'
        
    class pstatus(models.TextChoices):
        KHANDAN = 'khandan','خندان'
        DAHANBAST = 'dahanbast','دهن بست'
        ABKHANDAN = 'abkhandan','آب خندان'
        TARKIBI = 'tarkibi','ترکیبی'

    class pquality(models.TextChoices):
        D1 = 'd1','درجه یک'
        D2 = 'd2','درجه دو'
        D3 = 'd3','درجه سه'
        D4 = 'd4','درجه چهار'

    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    id = models.AutoField(primary_key=True,verbose_name='آیدی محصول')

    photo = models.ImageField(verbose_name='عکس محصول',upload_to='prdphotos')
    kind = models.CharField(max_length=20,choices=ptype.choices,verbose_name='نوع پسته')
    status = models.CharField(max_length=20,choices=pstatus.choices,verbose_name='وضعیت محصول')
    ounce = models.PositiveIntegerField(verbose_name='انس محصول')
    quality = models.CharField(max_length=20,choices=pquality.choices,verbose_name='(کیفی) کیفیت محصول')
    price = models.DecimalField(max_digits=13,decimal_places=0,verbose_name='(تومان) قیمت محصول')
    show_inventory = models.BooleanField(default=True,verbose_name='وضعیت نمایش وزن محصول')
    inventory = models.FloatField(verbose_name='وزن محصول')
    min_order = models.FloatField(null=True,blank=True,verbose_name='حداقل سفارش (کیلوگرم - خالی برای بدون محدودیت)')
    max_order = models.FloatField(null=True,blank=True,verbose_name='حداکثر سفارش (کیلوگرم - خالی برای بدون محدودیت)')
    discription = models.CharField(max_length=500,null=True,blank=True,verbose_name='توضیحات بیشتر برای محصول')
    free_shipping = models.BooleanField(default=False,verbose_name='ارسال رایگان')
    shipping_cost = models.DecimalField(max_digits=13,null=True,blank=True,decimal_places=0,verbose_name='(تومان) هزینه ارسال')
    is_pestina_product = models.BooleanField(default=False,verbose_name='محصول پستینا')
    is_confirmed = models.BooleanField(default=False,verbose_name='وضعیت تایید شدن توسط ادمین')
    ip_address = models.GenericIPAddressField(null=True,blank=True,verbose_name='آیپی')
    upload_time = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت محصول')

    def save(self,*args,**kwargs):
        if self.free_shipping :
            self.shipping_cost = None
        super().save(*args,**kwargs)


    def __str__(self):
        return f"{self.kind} uploaded by {'admin' if self.is_pestina_product else self.user.first_name}"
    



class Ticket(models.Model): #order a product
    class TicketType(models.TextChoices):
        FEEDBACK = "feedback","نظرات و پیشنهادات"
        PURCHASE = "purchase","درخواست خرید محصول"
        TECHNICAL = "technical","نقص فنی سایت"

    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,verbose_name='کاربر')

    ticket_id = models.AutoField(primary_key=True,verbose_name='شماره تیکت')
    buyer_namelastname = models.CharField(max_length=30,verbose_name='نام خریدار') #need to fill
    buyer_phone = models.CharField(max_length=20,verbose_name='شماره تلفن')
    ticket_type = models.CharField(max_length=20,choices=TicketType.choices,verbose_name='نوع تیکت')
    request_title = models.CharField(max_length=20,verbose_name='عنوان تیکت')
    request_discription = models.CharField(max_length=150,verbose_name='متن درخواست')
    ticket_time = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت تیکت')
    ip_address = models.GenericIPAddressField(null=True,blank=True,verbose_name='أیپی')

    def __str__(self):
        return f"{self.ticket_type} -> by {self.buyer_namelastname} {self.buyer_phone}"

class BuyTicket(models.Model):
    ticket_id = models.AutoField(primary_key=True,verbose_name='شماره سفارش')
    buyer_namelastname = models.CharField(max_length=30,verbose_name='نام خریدار')
    buyer_phone = models.CharField(max_length=20,verbose_name='شماره تلفن')
    pistachio = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول سفارش داده شده')
    gain_product = models.FloatField(verbose_name='مقدار (به کیلو)')
    order_discription = models.CharField(max_length=400,null=True,blank=True,verbose_name='توضیحات سفارش')
    calculated_price = models.FloatField(verbose_name='قیمت نهایی')
    ticket_time = models.DateTimeField(auto_now=True,verbose_name='تاریخ سفارش')
    ip_address = models.GenericIPAddressField(null=True,blank=True,verbose_name='آیپی')

    def __str__(self):
        return self.buyer_namelastname




