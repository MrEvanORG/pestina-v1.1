from django import forms
# from .models import
# from .models import tickets
from .models import User
from django.core.exceptions import ValidationError

class OrderForm(forms.Form):
    buyer_namelastname = forms.CharField(max_length=30,required=True,label='نام و نام خانوادگی')
    buyer_phonenumber = forms.CharField(max_length=15,required=True,label='شماره تلفن')
    request_title = forms.CharField(max_length=20,required=True,label='عنوان') #need to fill
    request_text = forms.CharField(max_length=200,required=True,label='متن درخواست') #need to fill

    def clean_buyer_namelastname(self):
        name = self.cleaned_data['buyer_namelastname']
        if len(name) >= 29:
            raise forms.ValidationError('بیش از حد مجاز است')
        elif len(name) < 5 :
            raise forms.ValidationError('بسیار کوتاه است')
        return name
    
    
    def clean_buyer_phonenumber(self):
        phone = self.cleaned_data['buyer_phonenumber']
        if not phone.isdigit():
            raise ValidationError('شماره تلفن باید فقط شامل اعداد باشد')
        if not len(phone) == 11 :
            raise ValidationError('شماره تلفن نامعتبر است')
        
        return phone
    
    def clean_request_title(self):
        title = self.cleaned_data['request_title']
        print(len(title))
        if len(title) > 19 :
            print('# ERROR RAISED')
            raise forms.ValidationError('بیش از حد مجاز است')
        elif len(title) < 5 :
            raise forms.ValidationError('بسیار کوتاه است')
        return title
        
    def clean_request_text(self):
        text = self.cleaned_data['request_text']
        if len(text) >= 198 :
            raise forms.ValidationError('بیش از حد مجاز است')
        elif len(text) < 5 :
            raise forms.ValidationError('بسیار کوتاه است')
        return text
        


class BuyForm(forms.Form):
    buyer_namelastname = forms.CharField(max_length=30,required=True,label='نام و نام خانوادگی') #need to fill
    buyer_phone = forms.CharField(max_length=15,required=True,label='شماره تلفن')
    gain_product = forms.FloatField(required=True,label='مقدار (به کیلو)')
    order_discription = forms.CharField(required=False,max_length=400,label='توضیحات سفارش')

    def clean_buyer_namelastname(self):
        name = self.cleaned_data['buyer_namelastname']
        if len(name) >= 29:
            raise forms.ValidationError('بیش از حد مجاز است')
        elif len(name) < 5 :
            raise forms.ValidationError('بسیار کوتاه است')
        return name
    
    def clean_buyer_phone(self):
        phone = self.cleaned_data['buyer_phone']
        if len(str(phone)) < 10 :
            raise forms.ValidationError('بسیار کوتاه است')
        return phone

    def clean_gain_product(self):
        gain = self.cleaned_data['gain_product']
        if float(gain) < 0.5 :
            raise forms.ValidationError('نمیتواند کمتر از 500 گرم باشد')
        elif float(gain) > 10 :
            raise forms.ValidationError('در حال حاضر امکان ثبت سفارش بیش از 10 کیلوگرم وجود ندارد')
        
        return gain

    def clean_order_discription(self):
        text = self.cleaned_data['order_discription']
        if len(text) >= 390 :
            raise forms.ValidationError('بیش از حد مجاز است')

        return text
    
class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=50)
    password = forms.CharField(max_length=120)

class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=18,required=True,label='first_name')
    last_name = forms.CharField(max_length=18,required=True,label='last_name')
    phone_number = forms.CharField(max_length=13,required=True,label='phone_number')

    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number']
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) <= 2 :
            raise ValidationError('نام بسیار کوتاه است')
        elif len(first_name) >= 17 :
            raise ValidationError('نام بسیار طولانی است')
        
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name) <= 2 :
            raise ValidationError('نام خانوادگی بسیار کوتاه است')
        elif len(last_name) >= 17 :
            raise ValidationError('نام خانوادگی بسیار طولانی است')
        
        return last_name
    
    def clean_phone_number(self):
        phone = (self.cleaned_data['phone_number']).strip()
        if not phone.isdigit():
            raise ValidationError('شماره تلفن باید فقط شامل اعداد باشد')
        if not len(phone) == 11 :
            raise ValidationError('شماره تلفن نامعتبر است')
        if User.objects.filter(phone_number=phone).exists() :
            raise ValidationError('این شماره تلفن قبلا ثبت شده است')
        
        return phone
                
class VerifyNumberForm(forms.Form):

    code = forms.CharField(max_length=5,required=True,label='verification')

    def clean_code(self):
        code = (self.cleaned_data['code']).strip()

        if not code.isdigit() :
            raise ValidationError('کد تایید باید عددی باشد')
        if not len(code) == 5 :
            raise ValidationError('کد باید به طول ۵ کاراکتر باشد')
        
        return code
    
class SetPasswordForm(forms.Form):
    new_password1 = forms.CharField(max_length=128,required=True,label='password')
    new_password2 = forms.CharField(max_length=128,required=True,label='repassword')

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if len(password) < 8 :
            raise ValidationError('پسورد نمیتواند کمتر از ۸ کاراکتر باشد')
        
        if not any(char.isdigit() for char in password) :
            raise ValidationError('رمز عبور باید حداقل یک کاراکتر عددی داشته باشد')
        
        if not any(char.isalpha() for char in password) :
            raise ValidationError('پسورد باید شامل حروف انگلیسی کوچک و بزرگ باشد')
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2 :
            self.add_error('new_password2','رمز عبور و تکرار آن باید یکسان باشند')
 
        return cleaned_data
        







    



