from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Product, UserPayment#, Review
from .forms import ProductForm, RegisterForm, PartForm#, ReviewForm
from django.http import Http404
from .decorators import authenticated_user
from django.contrib.auth import login, authenticate
from django.conf import settings
import stripe
import time
from django.views.decorators.csrf import csrf_exempt

# Create your views here.



def account(request):
    context = {}



    return render(request, "main/account.html", context)

def success(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    if request.user.is_authenticated:
        user_id = request.user.id
        user_payment = UserPayment.objects.get(user=user_id)
        user_payment.stripe_checkout_id = checkout_session_id
        user_payment.save()
    return render(request, "main/success.html", {'customer':customer})

def cancel(response):
    context = {}
    return render(response, "main/cancel.html", context)

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        user_payment.payment_bool = True
        user_payment.save()
    return HttpResponse(status=200)



def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            
            return redirect("/login")
        else:
            pass
    else:
        form = RegisterForm()

    context = {'form' : form}
    return render(response, "main/register.html", context)

def loginPage(response):

    required = False
    if response.method == "POST":
        username = response.POST.get('username')
        password = response.POST.get('password')

        user = authenticate(response, username=username, password=password)
        if user is not None:
            login(response, user)
            return redirect('/')
    else:
        if 'required' in response.GET:
            required = True

    return render(response, "main/login.html", {"required":required})

'''
@authenticated_user
def reviewPage(response, slug=None):

    obj = None
    if slug is not None:
        try:
            obj = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404
        except Product.MultipleObjectsReturned:
            obj = Product.objects.filter(slug=slug).first()
        except:
            raise Http404
        
    product = Product.objects.get(slug=slug)

    if response.method == "POST":
        form = ReviewForm(response.POST, response.FILES)
        
        if form.is_valid():

            instance = form.save(commit=False)
            instance.reviewer = response.user
            instance.product = product
            form.save()

            return redirect("productPage", slug=slug)
    else:
        form = ReviewForm(response.POST, response.FILES)

    
    return render(response, "main/review_page.html", {"form": form})
'''



def productPage(response, slug=None):
    obj = None
    if slug is not None:
        try:
            obj = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404
        except Product.MultipleObjectsReturned:
            obj = Product.objects.filter(slug=slug).first()
        except:
            raise Http404   
    none = False

    stripe.api_key = settings.STRIPE_SECRET_KEY
    if response.method == "POST":
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items = [{
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                        'name': obj.product_name
                    },
                    'unit_amount': obj.price_in_pence
                },
                'quantity': 1,
                },
            ],
            mode = 'payment',
            customer_creation = 'always',
            success_url = settings.REDIRECT_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
			cancel_url = settings.REDIRECT_DOMAIN + '/cancel',
        )
        return redirect(checkout_session.url, code=303)


    context = {"product": obj, "none":none}

    return render(response, "main/product_page.html", context)







def add(request):

    submitted = False
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()

    
            return redirect("/add?submitted=True")
    else:
        form = ProductForm(request.POST, request.FILES)

        if 'submitted' in request.GET:
            submitted = True

    return render(request, "main/add.html", {"form": form,
    'submitted':submitted})



def addpart(request):

    submitted = False
    if request.method == "POST":
        form = PartForm(request.POST)
        
        if form.is_valid():
            form.save()

    
            return redirect("/addpart?submitted=True")
    else:
        form = PartForm(request.POST)

        if 'submitted' in request.GET:
            submitted = True

    return render(request, "main/addpart.html", {"form": form,
    'submitted':submitted})



def index(response):

    return render(response, "main/index.html", {})

def products(response):

    if "datenewest" in response.GET:
        products = Product.objects.order_by("-id")
    elif "priceasc" in response.GET:
        products = Product.objects.order_by("price_in_pence")
    elif "pricedesc" in response.GET:
        products = Product.objects.order_by("-price_in_pence")
    else:
        products = Product.objects.all()
    max = len(products)

    if max != 0:
        if max % 3 == 0:
            rows = max // 3
        else:
            rows = (max // 3) +1
        prev=0
        left = max
        newproducts=[]
        for j in range(rows):
            if left < 3:
                newproducts.append(products[prev:prev+left])
                break
            else:
                newproducts.append(products[prev:prev+3])
                prev = prev+3
            left-=3
            
        for list in newproducts:
            for item in list:

                print(item.product_name)

        dict = {"newproducts": newproducts, "nothing": False}
    else:
        dict={"newproducts": [], "nothing": True}

    return render(response, "main/products.html", dict)




