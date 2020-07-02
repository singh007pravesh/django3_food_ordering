import uuid ,json
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse
from .models import*
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from math import ceil

from . import context_processors
# Create your views here.


def index(request):
    restaurants = Restaurants.objects.all()
    
    #no of slides..
    n = len(restaurants)
    nslides = n//4 + ceil((n/4)-(n//4))
    params = {'no_of_slides':nslides,'range':range(1,nslides),'restaurant':restaurants}
    return render(request,"food/index.html",params)
def searchMatch(query,item):
    if query in item.dish_name.lower() or query in item.dish_desc.lower() or query in item.category.lower():
        return True
    else:
        return False
def search(request):
    query = request.GET.get('search')
    allDishes = []
    catdishes = Dishes.objects.values('category', 'id')
    cats = {item['category'] for item in catdishes}
    for cat in cats:
        dishtemp = Dishes.objects.filter(category=cat)
        dish = [item for item in dishtemp if searchMatch(query,item)]

        n = len(dish)
        nslides = n//4 + ceil((n/4) - (n//4))
        if len(dish)!=0:
            allDishes.append([dish, range(1,nslides), nslides])
    params = {'alldishes': allDishes}
    return render(request,"food/categories.html",params)



def categories(request):
    #dishes = Dishes.objects.all()
    #print(dishes)
    #n = len(dishes)
    #nslides = n//4 + ceil((n/4) - (n//4))
    #params = {'no_of_slides':nslides, 'range': range(1,nslides), 'dish':dishes}
    #allDishes = [[dishes, range(1,nslides), nslides],
           #     [dishes, range(1,nslides), nslides]]
    #params = {'alldishes': allDishes}
    #return render(request, 'food/categories.html', params)
    allDishes = []
    catdishes = Dishes.objects.values('category', 'id')
    cats = {item['category'] for item in catdishes}
    for cat in cats:
        dish = Dishes.objects.filter(category=cat)
        n = len(dish)
        nslides = n//4 + ceil((n/4) - (n//4))
        allDishes.append([dish, range(1,nslides), nslides])
    params = {'alldishes': allDishes}
    return render(request,"food/categories.html",params)

#def resdishes(request, myid):
 #   alldish=[]
  #  dish = Dishes.objects.filter(restaurant=myid)
   # alldish.append(dish)
    #params = {'alldish':alldish}
    #return render(request,'food/resdishview.html',params)
def single_slug(request,single_slug):
    dishes= []
    dishes=Dishes.objects.filter(restaurant__res_name=single_slug)

    # print(all)
    
    params = {
        'dishes':dishes,
        }
    return render(request,"food/resdishview.html", params)
    # dishes = [d.dish_name for d in Dishes.objects.all()]
    # if single_slug in dishes:
    #     return HttpResponse(f"{single_slug}is a dish")

def dishview(request, myid):
    dish = Dishes.objects.filter(id=myid)
    return render(request, 'food/dishview.html', {'dish': dish[0]})


def aboutus(request):
    return render(request, 'food/aboutus.html')

def contactus(request):
    if request.method =="POST":
    
        name = request.POST.get('name', '')

        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('message','')
        contact = Contact(name=name, email=email, phone=phone, message=desc)
        contact.save()
        messages.success(request, 'Thank You For Contacting With Us')
    return render(request, 'food/contactus.html')

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if len(username) > 10:
            messages.error(request, "username is must me under 10 characters")
            return redirect('FoodHome')
        if pass1 != pass2:
            messages.error(request, "passwords do not match ")
            return redirect('FoodHome')
        if not username.isalnum():
            messages.error(request, "must be alphanumeric")
            return redirect('FoodHome')
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been successfully created")
        return redirect('FoodHome')

    else:
        return HttpResponse('404-not fount')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request,'successfully loged in')
            return redirect('FoodHome')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('FoodHome')

    return HttpResponse('handlelogin')

def handleLogout(request):
    logout(request)
    messages.success(request,'succesfully loged out')
    return redirect('FoodHome')
    return HttpResponse('handlelogout')

def checkout(request,amt):
    context={
        'amt': amt
    }
    return render(request,'food/checkout.html',context)

def cart(request):
    a=context_processors.categories_processor(request)
    # products=[]
    # print(a)
    # for c in a['cart']:
    #     product=Dishes.objects.filter(pk=c)
    #     products.append(product)
    #     # print(product)
    products=Dishes.objects.filter(pk__in=a['cart'])
    # uid=uuid.uuid4().hex[:10].upper()

    return render(request, 'food/cart.html',{'products':products})


def cart_check_out(request):
    a=context_processors.categories_processor(request)
    text = request.POST.get('prods')
    print(text)
    text = text.replace("'",'')
    print(json.loads(text))

    for sss in json.loads(text):
        item=OrderItem(order_no=a['s_id'],dish_id=int(sss['pro_id']),quantity=sss['qty'],price=sss['sub'])
        item.save()
    context={
        'total':request.POST.get('total')
    }
    return render(request,'food/cart-checkout.html',context)

def place_order(request):
    a=context_processors.categories_processor(request)

    name      = request.POST.get('name')
    email     = request.POST.get('email')
    address   = request.POST.get('address')
    address2  = request.POST.get('address2')
    city      = request.POST.get('city')
    state     = request.POST.get('state')
    zipcode   = request.POST.get('zipcode')
    mobile    = request.POST.get('mobile')
    total     = request.POST.get('total')
    # print(total)

    new_order=OrderDetail(order_no=a['s_id'],amount=total,user_id=1,name=name,email=email,
        address=address,address2=address2,city=city,state=state,zipcode=zipcode,mobile=mobile)
    new_order.save()
    messages.success(request,'Your order placed successfully')
    cart=[]
    s_id=uuid.uuid4().hex[:10].upper()
    request.session['adyty879aaa']=cart
    request.session['s_id']=s_id

    return render(request, 'food/cart.html')
