from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Cart, Customer, Product, OrderPlaced
from .forms import CustomerRegistrationForm , CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
  def get(self, request):
     Vegetables = Product.objects.filter(category='V')
     Fruits = Product.objects.filter(category='F')
     Grocery = Product.objects.filter(category='G')
     Dairy = Product.objects.filter(category='D')
     return render(request,'app/home.html',
                   {'Vegetables':Vegetables , 'Fruits':Fruits, 'Grocery':Grocery} )
     
class ProductDetailView(View):
  def get(self, request, pk):
    product = Product.objects.get(pk=pk)
    return render(request , 'app/productdetail.html', {'product':product})
      
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

def show_cart(request):
  if request.user.is_authenticated:
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.00
    shipping_amount = 5.00
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==user]
    if cart_product:
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        total_amount = "{:0.2f}".format(amount + shipping_amount) 
      return render(request, 'app/addtocart.html', {'carts':cart , 'total_amount':total_amount , 'amount':amount})
    else:
      return render(request,'app/emptycart.html')
    
def plus_cart(request):
  if request.method == 'GET':
   prod_id = request.GET['prod_id']
   c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
   c.quantity+=1
   c.save()
   amount = 0.00
   shipping_amount = 5.00
   total_amount = 0.0
   cart_product = [p for p in Cart.objects.all() if p.user==request.user]
  if cart_product:
    for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        total_amount = "{:0.2f}".format(amount + shipping_amount)   
    data = {
          'quantity': c.quantity,
          'amount': amount,
          'total_amount': amount + shipping_amount,
        }
    return JsonResponse(data)
  
def minus_cart(request):
  if request.method == 'GET':
   prod_id = request.GET['prod_id']
   c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
   c.quantity-=1
   c.save()
   amount = 0.00
   shipping_amount = 5.00
   total_amount = 0.0
   cart_product = [p for p in Cart.objects.all() if p.user==request.user]
  if cart_product:
    for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        total_amount = "{:0.2f}".format(amount + shipping_amount) 
        
    data = {
          'quantity': c.quantity,
          'amount': amount,
          'total_amount': amount + shipping_amount,
        }
    return JsonResponse(data)
  
def remove_cart(request):
  if request.method == 'GET':
   prod_id = request.GET['prod_id']
   c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
   c.delete()
   amount = 0.00
   shipping_amount = 5.00
   total_amount = 0.0
   cart_product = [p for p in Cart.objects.all() if p.user==request.user]
  if cart_product:
    for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        total_amount = "{:0.2f}".format(amount + shipping_amount) 
        
    data = {
          'amount': amount,
          'total_amount': amount + shipping_amount,
        }
    return JsonResponse(data)
 
@login_required    
def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add , 'active': 'btn-primary'})

@login_required
def orders(request):
  op = OrderPlaced.objects.filter(user=request.user)
  return render(request, 'app/orders.html' ,{'order_placed':op})


class CustomerRegistrationView(View):
  def get(self ,request):
    form = CustomerRegistrationForm()
    return render(request, 'app/customerregistration.html', {'form':form})
  
  def post(self ,request):
    form = CustomerRegistrationForm(request.POST)
    if form.is_valid():
      messages.success(request, 'congratulations!! You are successfully registered')
      form.save()
    return render(request, 'app/customerregistration.html', {'form':form})

@login_required
def checkout(request):
  user = request.user
  add = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user=user)
  amount = 0.00
  shipping_amount = 5.00
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user==request.user]
  if cart_product:
    for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
    total_amount = "{:0.2f}".format(amount + shipping_amount) 
        
  return render (request, 'app/checkout.html', {'add': add , 'total_amount': total_amount , 'cart_items':cart_items})

@login_required
def payment_done(request):
  user = request.user
  custid = request.GET.get('custid')
  customer= Customer.objects.get(id=custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user, customer=customer, product=c.product, quantity =c.quantity).save()
    c.delete()
  return redirect("orders")


def vegetables(request , data=None):
  if data == None:
   vegetables = Product.objects.filter(category= 'V')
  elif data =='below':
   vegetables = Product.objects.filter(category= 'V').filter(discounted_price__lt=2)
  elif data =='above':
   vegetables = Product.objects.filter(category= 'V').filter(discounted_price__gt=2)
  return render(request , 'app/vegetables.html', {'Vegetables': vegetables})


def fruits(request , data=None):
  if data == None:
   fruits = Product.objects.filter(category= 'F')
  elif data =='below':
   fruits = Product.objects.filter(category= 'F').filter(discounted_price__lt=2)
  elif data =='above':
   fruits = Product.objects.filter(category= 'F').filter(discounted_price__gt=2)
  return render(request , 'app/fruits.html', {'Fruits': fruits}) 


def grocery(request , data=None):
  if data == None:
   grocery = Product.objects.filter(category= 'G')
  elif data =='below':
   grocery = Product.objects.filter(category= 'G').filter(discounted_price__lt=2)
  elif data =='above':
   grocery = Product.objects.filter(category= 'G').filter(discounted_price__gt=2)
  return render(request , 'app/grocery.html', {'Grocery': grocery}) 

def dairy(request , data=None):
  if data == None:
   dairy = Product.objects.filter(category= 'D')
  elif data =='below':
   dairy = Product.objects.filter(category= 'D').filter(discounted_price__lt=2)
  elif data =='above':
   dairy = Product.objects.filter(category= 'D').filter(discounted_price__gt=2)
  return render(request , 'app/dairy.html', {'Dairy': dairy})


@method_decorator(login_required , name='dispatch')
class ProfileView(View):
  def get(self, request):
    form =CustomerProfileForm
    return render(request,'app/profile.html', {'form':form, 'active': 'btn-primary'})
  
  def post(self, request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
      usr = request.user
      name = form.cleaned_data['name']
      locality = form.cleaned_data['locality']
      city = form.cleaned_data['city']
      county = form.cleaned_data['county']
      eircode = form.cleaned_data['eircode']
      reg = Customer(user=usr, name=name,locality=locality, city=city, county=county,  eircode=eircode)
      reg.save()
      messages.success(request, 'Profile Updated Successfully!!')
    return render(request,'app/profile.html', {'form':form , 'active': 'btn-primary'})


def searchbar(request):
  if request.method == "POST":
    searched = request.POST['searched']
    products = Product.objects.filter(title__contains=searched)
    return render(request, 'app/searchbar.html' ,{'searched':searched , 'products':products})
  else:
    return render(request, 'app/searchbar.html' ,{'searched':searched})
  

def aboutus(request):
 return render(request, 'app/aboutus.html')


def support(request):
 return render(request, 'app/support.html')