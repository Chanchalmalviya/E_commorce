from django.shortcuts import render
from django.views import View
from .models import *
from django.db.models import Q

#def home(request):
# return render(request, 'app/home.html')

class ProductView(View):
 def get(self,request):
  mobile =Product.objects.filter(category="M")
  laptop =Product.objects.filter(category="L")
  topweres =Product.objects.filter(category="TW")
  bottomweres =Product.objects.filter(category="BW")
  print(bottomweres)
  return render (request,"app/home.html",
                 {"mobile":mobile,
                  "laptop":laptop,
                  "topweres":topweres,
                  "bottomweres":bottomweres   
                 },
                 )
  

class ProductDetailView(View):
 def get(self,request,pk):
  product= Product.objects.get(pk=pk)
  item_alredy_in_cart = False
  if request.user.is_authenticated:
   item_alredy_in_cart=Cart.objects.filter(
    Q(product=product.id)& Q(user = request.user)
   
   ).exists()
   return render(request,"productdetail.html",{"product":product,"item_alredy_in_cart":item_alredy_in_cart})
  else:
   return render(request,"productdetail.html",{"product":product,"item_alredy_in_cart":item_alredy_in_cart})
   

  

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
