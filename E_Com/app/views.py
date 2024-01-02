from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.db.models import Q
from django.http import JsonResponse
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages

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
   return render(request,"app/productdetail.html",{"product":product,"item_alredy_in_cart":item_alredy_in_cart})
  else:
   return render(request,"app/productdetail.html",{"product":product,"item_alredy_in_cart":item_alredy_in_cart})
   

  

def add_to_cart(request):
 user = request.user
 product_id = request.GET.get("prod_id")
 product = Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect("/cart")

def showcart(request):
 if request.user.is_authenticated:
  user = request.user
  cart = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all()
                  if p.user == user]
  if cart_product:
   for p in cart_product:
    tempamount = p.quantity * p.product.discounted_price
    amount += tempamount
    total_amount = amount + shipping_amount
  return render(
   request,
   "app/addtocart.html",
   { "carts":cart,"total_amount": total_amount,"amount":amount},
  )  
 else:
  return render(request,"app/emptycart.html")
 
def plus_cart(request):
  if request.method == "GET":
   prod_id = request.GET["prod_id"]
   c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
   c.quantity += 1
   c.save()
   amount = 0.0
   shipping_amount = 70.0
   cart_product =[p for p in Cart.objects.all() if p.user == request.user]
   for p in cart_product:
    tempamount = p.quantity * p.product.discounted_price
    amount += tempamount

    data = {
     "quantity":c.quantity,
     "amount" :amount,
     "totalamount": amount + shipping_amount,
    }
    return JsonResponse(data)
   

def minus_cart(request):
  if request.method == "GET":
   prod_id = request.GET["prod_id"]
   c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
   c.quantity -= 1
   c.save()
   amount = 0.0
   shipping_amount = 70.0
   cart_product =[p for p in Cart.objects.all() if p.user == request.user]
   for p in cart_product:
    tempamount = p.quantity * p.product.discounted_price
    amount += tempamount

    data = {
     "quantity":c.quantity,
     "amount" :amount,
     "totalamount": amount + shipping_amount,
    }
    return JsonResponse(data)
    
def remove_cart(request):
  if request.method == "GET":
   prod_id = request.GET["prod_id"]
   c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
   c.delete()
   amount = 0.0
   shipping_amount = 70.0
   cart_product =[p for p in Cart.objects.all() if p.user == request.user]
   for p in cart_product:
    tempamount = p.quantity * p.product.discounted_price
    amount += tempamount

    data = {
     "amount" :amount,
     "totalamount": amount + shipping_amount,
    }
    return JsonResponse(data) 
   
def mobile(request,data=None):
 if data == None:
  mobiles = Product.objects.filter(category="M")
 elif data == "Redmi" or data == "Samsung":
  mobiles = Product.objects.filter(category="M").filter(brand=data)
 elif data == "below":
  mobiles = Product.objects.filter(category ="M").filter(discounted_price__gt=10000)
 elif data == "above":
  mobiles = Product.objects.filter(category ="M").filter(discounted_price__gt=1000)
 return render(request,"app/mobile.html",{"mobiles":mobiles})
    
def laptop(request,data=None):
 if data == None:
  laptops = Product.objects.filter(category="L")
 elif data == "HP" or data == "Lenovo":
  laptops = Product.objects.filter(category="L").filter(brand=data)
 elif data == "below":
  laptops = Product.objects.filter(category ="L").filter(discounted_price__gt=10000)
 elif data == "above":
  laptops = Product.objects.filter(category ="L").filter(discounted_price__gt=10000)
 return render(request,"app/laptop.html",{"laptops":laptops})  

def topwear(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category="TW")
    elif data == "ZARA" or data == "GUCCI":
        topwears = Product.objects.filter(category="TW").filter(brand=data)
    elif data == "below":
        topwears = Product.objects.filter(category="TW").filter(
            discounted_price__lt=1000
        )
    elif data == "above":
        topwears = Product.objects.filter(category="TW").filter(
            discounted_price__gt=1000
        )
    return render(request, "app/topwear.html", {"topwears": topwears}) 


def bottomwear(request, data=None):
    if data == None:
        bottomwears = Product.objects.filter(category="BW")
    elif data == "ZARA" or data == "GUCCI":
        bottomwears = Product.objects.filter(category="BW").filter(brand=data)
    elif data == "below":
        bottomwears = Product.objects.filter(category="BW").filter(
            discounted_price__lt=1000
        )
    elif data == "above":
        bottomwears = Product.objects.filter(category="BW").filter(
            discounted_price__gt=1000
        )
    return render(request, "app/bottomwear.html", {"bottomwears": bottomwears})


class CustomerRegistrationView(View):
  def get(self, request):
   form = CustomerRegistrationForm()
   return render(request,"app/customerregistration.html",{"form":form})
  
  def post(self, request):
   form = CustomerRegistrationForm(request.POST)
   if form.is_valid():
    messages.success(request,"Cogratulations !! Registerd Successfully")
    form.save()
   return render(request,"app/customerregistration.html",{"form":form})   
  
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,"active":"btn-primary"})  

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(
            request, "app/profile.html", {"form": form, "active": "btn-primary"}
        )

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data["name"]
            locality = form.cleaned_data["locality"]
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"]
            zipcode = form.cleaned_data["zipcode"]
            reg = Customer(
                user=usr,
                name=name,
                locality=locality,
                city=city,
                state=state,
                zipcode=zipcode,
            )
            reg.save()
            messages.success(request, "Congratulation!! Profile Updated Succesfully")
        return render(
            request, "app/profile.html", {"form": form, "active": "btn-primary"}
        )


     
def buy_now(request):
 return render(request, 'app/buynow.html')

def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    shipping_amount = 70.0
    totalamount = 0.0

    for item in cart_items:
        item.product_amount = item.quantity * item.product.discounted_price
        totalamount += item.product_amount

    totalamount += shipping_amount

    return render(
        request,
        "app/checkout.html",
        {
            "add": add,
            "totalamount": totalamount,
            "cart_items": cart_items,
        },
    )



def orders(request):
 order_placed=Orderplace.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order_placed':order_placed})

def change_password(request):
 return render(request, 'app/changepassword.html')

# def mobile(request):
#  return render(request, 'app/mobile.html')



def customerregistration(request):
 return render(request, 'app/customerregistration.html')


def payment_done(request):
  user = request.user
  custid = request.GET.get("custid")
  customer = Customer.objects.get(id=custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    Orderplace(user=user,customer=customer,product=c.product,quantity=c.quantity,).save()
    return redirect("orders")