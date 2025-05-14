from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.shortcuts import render ,get_object_or_404 , redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
#----------------------------------------------------------#
from .models import Product , Ticket ,BuyTicket , User 
from .forms import OrderForm , BuyForm , LoginForm , SignUpForm , VerifyNumberForm , SetPasswordForm
from .addons import *


def homepage(request):
    return render(request,'nindex.html')

@csrf_protect
def login_page(request):
    if request.user.is_authenticated : 
        return redirect(dashboard)
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        context = {'form':form}
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['phone_number'],
                                password=form.cleaned_data['password'])
            if user:
                login(request,user)
                request.session.set_expiry(2*60*60)
                return redirect(dashboard)
            else:
                context = {'form':form,'auth_error':True}
        
        return render(request,'l-pages/login.html',context)
            
    
    if request.method == 'GET':
        return render(request,'l-pages/login.html')

@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            otp = random.randint(10000,99999)
            print(">> otp" + str(otp))
            request.session['form-data'] = form.cleaned_data
            request.session['phone-number'] = form.cleaned_data['phone_number']
            request.session['otp-code'] = otp
            request.session['is-verified'] = False

            # send code with function
            # send_otp(form.cleaned_data['first_name'],form.cleaned_data['phone_number'],otp)
            return redirect(number_verify)

        else:
            context = {'form':form}
            return render(request,'l-pages/signup.html',context)




    if request.method == 'GET':
        return render(request,'l-pages/signup.html')

@csrf_protect
def number_verify(request):
    if not 'phone-number' in request.session : #if session has destroid
        return redirect(signup)
    
    if request.method == 'POST': #for submit form
        form = VerifyNumberForm(request.POST)

        if form.is_valid(): #if format of code be correct

            form_code = form.cleaned_data['code']
            otp_code = request.session.get('otp-code')
            if str(form_code) == str(otp_code) :
                request.session['is-verified'] = True
                print('phone veified save in session check for correction : '+str(request.session['is-verified']))
                return redirect(set_password)
            else:
                context = {'form':{'code':{'errors':'کد وارد شده اشتباه است'}}}
                return render(request,'l-pages/verify-sms.html',context)


        else:
            context = {'form':form}
            return render(request,'l-pages/verify-sms.html',context)


    

    if request.method == "GET": #for comming to this page from signup
        form_phone = request.session.get('phone-number')
        return render(request,'l-pages/verify-sms.html',{'number':form_phone})

@csrf_protect
def set_password(request):
    if not request.session.get('is-verified'):
        return redirect(signup)
    
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            data = request.session.get('form-data',{})
            # form = SignUpForm(data=data)
            user = User.objects.create_user(
                phone_number = data.get('phone_number'),
                first_name = data.get('first_name'),
                last_name = data.get('last_name'),
                is_verified = True,
                username = data.get('phone_number'),
                password = form.cleaned_data['new_password1'],
                ip_address = get_ip(request),
            )
            user.save()
            del request.session['form-data'] 
            del request.session['phone-number'] 
            del request.session['otp-code'] 
            del request.session['is-verified'] 
            login(request,user)
            # login(request,user)
            request.session.set_expiry(2*60*60)
            return redirect(dashboard)

        else:
            return render(request,'l-pages/set-password.html',{'form':form})

    if request.method == 'GET':
        return render(request,'l-pages/set-password.html')

def forgotpass(request):
    return render(request,'l-pages/forgot-pass.html')    

def view_products(request):
    prd = Product.objects.all()
    pagin = Paginator(prd,2)
    page_number = request.GET.get('page')
    page_obj = pagin.get_page(page_number)
    context = {'prd': page_obj}
    return render(request,'nproducts.html',context)

# def view_products(request):
#     products = Product.objects.filter(is_confirmed=True)

#     # فیلترها
#     if request.GET.get("free_shipping") == "1":
#         products = products.filter(free_shipping=True)

#     if request.GET.get("pestina") == "1":
#         products = products.filter(is_pestina_product=True)

#     selected_types = request.GET.getlist("kind")
#     if selected_types:
#         products = products.filter(kind__in=selected_types)

#     paginator = Paginator(products, 12)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     context = {
#         "page_obj": page_obj,
#         "selected_types": selected_types,
#         "free_shipping": request.GET.get("free_shipping", ""),
#         "pestina": request.GET.get("pestina", "")
#     }
#     return render(request, "nproducts.html", context)

@csrf_protect
def send_ticket(request,ticket_type):
    if str(ticket_type) == 'technical':
        context = {'title':'ارتباط با پشتیبانی/گزارش نقص فنی',
                    'text':'لطفا جهت گزارش نقص فنی فرم زیر را تکمیل کنید',
                    'form_type':'technical'}
        form_type = Ticket.TicketType.TECHNICAL
    elif str(ticket_type) == 'feedback':
        context = {'title':'ارتباط با پشتیبانی/انتقادات و پیشنهادات',
                    'text':'لطفا جهت تبادل نظراتتان فرم زیر را کامل کنید',
                    'form_type':'feedback'}
        form_type = Ticket.TicketType.FEEDBACK
    elif str(ticket_type) == 'purchase':
        context = {'title':'فرم درخواست خرید پسته',
                    'text':'لطفا جهت سفارش محصول ناموجود فرم زیر را کامل کنید',
                    'form_type':'purchase'}
        form_type = Ticket.TicketType.PURCHASE
    if not context:
        return redirect(homepage)
    
    if request.method == 'POST':
        form = OrderForm(data=request.POST)
            # ticket.save()
        if not form.errors and form.is_valid():
            ticket = Ticket.objects.create(
            user = request.user,
            buyer_namelastname = form.cleaned_data['buyer_namelastname'],
            buyer_phone = form.cleaned_data['buyer_phonenumber'],
            request_title = form.cleaned_data['request_title'],
            request_discription = form.cleaned_data['request_text'],
            ticket_type = form_type,
            ip_address = get_ip(request))
            ticket.save()
            #send message
            request.session['buyer-phone'] = form.cleaned_data['buyer_phonenumber']
            request.session['buyer-name'] = form.cleaned_data['buyer_namelastname']
            return redirect(registered)
        else:
            form_context = {'form':form}
            context.update(form_context)
            return render(request,"send_ticket.html",context,)

    if request.method == 'GET':
        return render(request,"send_ticket.html",context)

def buy_product(request,pid):
    order_data = request.session.get("order_data")
    if order_data:
        del request.session["order_data"]
    

    prd = Product.objects.get(id=pid)
    if request.method == 'POST':
        form = BuyForm(data=request.POST)
        if not form.errors and form.is_valid():

            form_data = form.cleaned_data
            price_string , price = calculate_price(form.cleaned_data['gain_product'],prd.pistachio_price)

            request.session["order_data"] = {
                "prd":pid,
                "form_data":form_data,
                "price":price,
            }
            context = {'form':form,'p':prd,'price':price_string}
            return render(request,'calculate.html',context)
        else:
            context = {'form':form,'p':prd} #return prodct and form error and form content
            return render(request,"buy_product.html",context)
            
    elif request.method == 'GET':
        context = {'p':prd}
        return render(request, "buy_product.html", context)
    
def confirm_buy(request):
    order_data = request.session.get("order_data")
    if not order_data:
        return HttpResponse('sorry something happend in backend process and your order does not save\nThis is an Error !')
    else:
        del request.session["order_data"]


    form = BuyForm(data=order_data['form_data'])
    pid = order_data['prd']
    price = order_data['price']

    print(form,pid,price)
    prd = Product.objects.get(pistachio_id=pid)

    ticket = BuyTicket.objects.create(
    buyer_namelastname = form.cleaned_data['buyer_namelastname'],
    buyer_phone = form.cleaned_data['buyer_phone'],
    pistachio = prd,
    gain_product = form.cleaned_data['gain_product'],
    order_discription = form.cleaned_data['order_discription'],
    calculated_price = price,
    ip_address = get_ip(request))
    ticket.save()
    Generate_email('buy',form.cleaned_data['buyer_namelastname'],form.cleaned_data['buyer_phone'],0,form.cleaned_data['order_discription'],prd.pistachio_name,form.cleaned_data['gain_product'],price)
# Generate_email(type,name,phone,title,discription,pistachio,gain,price)
    context = {'buyer_name':ticket.buyer_namelastname,'buyer_phone':ticket.buyer_phone}
    return render(request,'registered.html',context)

def about_us(request):
    return render(request,"nabout_us.html")

def dashboard(request):
    if not request.user.is_authenticated : 
        return redirect(login_page)
    
    return render(request,'l-pages/dashboard.html')

def user_logout(request):
    logout(request)
    return redirect(homepage)

def registered(request):
    phone = request.session.get("buyer-phone")
    name = request.session.get("buyer-name")
    print(phone,name)
    if not phone:
        return redirect(send_ticket,'purchase')
    try:
        del request.session["buyer-phone"]
        del request.session["buyer-name"]
    except:
        pass
    context = {"buyer_name":name,"buyer_phone":phone}
    return render(request,'registered.html',context)


from django.http import HttpResponse
from .templatetags.custom_filters import format_toman

def format_price_view(request, amount):
    try:
        price = int(amount)
    except ValueError:
        return HttpResponse("۰ تومان")
    return HttpResponse(format_toman(price))
    
    
    



