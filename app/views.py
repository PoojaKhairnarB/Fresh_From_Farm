from django.shortcuts import render
from django.views import View
from .models import Cart, Customer, Product, OrderPlaced

class ProductView(View):
  def get(self, request):
     Vegetables = Product.objects.filter(category='V')
     Fruits = Product.objects.filter(category='F')
     Grocery = Product.objects.filter(category='G')
     Dairy = Product.objects.filter(category='D')
     return render(request,'app/home.html',
                   {'Vegetables':Vegetables , 'Fruits':Fruits, 'Grocery':Grocery, 'Dairy':Dairy} )
     
def product_detail(request):
  return render(request, 'app/productdetail.html')
      
def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request):
 return render(request, 'app/mobile.html')

def login(request):
 return render(request, 'app/login.html')

def customerregistration(request):
 return render(request, 'app/customerregistration.html')

def checkout(request):
 return render(request, 'app/checkout.html')
