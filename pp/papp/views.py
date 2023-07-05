from django.shortcuts import render, redirect
from django.db.models import Q,Subquery
from .models import SignUpData,Product,cart
from .forms import ProductForm
from django.shortcuts import render, get_object_or_404
from django.contrib.sessions.models import Session

from django.core.mail import send_mail
from django.shortcuts import render
import csv
from django.http import HttpResponse

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse
from .forms import UploadFileForm
from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.
def index(request):
    return render(request,"index.html")
def about(request):
    return render(request,"about.html")
def contact(request):
    return render(request,"contact.html")
def login(request):
    return render(request,"login.html")
def registration(request):
    return render(request,"registration.html")

def SignUpDatafunction(request):
    name = request.POST['name']
    emailid = request.POST['email']
    pwd=request.POST['password']
    signobj = SignUpData(sign_name=name,sign_email=emailid,sign_password=pwd)
    SignUpData.save(signobj)
    # subject = 'Welcome to mesage'
    # message = 'bye'
    # email_from = 'amssdp@outlook.com'
    # recipient_list = [emailid]
    # send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return render(request, "login.html")
def checkuserlogin(request):
    emailid=request.POST["email"]
    pwd=request.POST["password"]
    flag=SignUpData.objects.filter(Q(sign_email=emailid) & Q(sign_password=pwd))
    if flag:
        user = SignUpData.objects.get(sign_email=emailid)
        request.session["uname"] = user.sign_name
        request.session["email"] = user.sign_email
        return render(request, "userhome.html", {"uname": user.sign_name, "user": user})
    else:
        return render(request, "logfail.html")
def logout(request):
    session_key = request.session.session_key
    Session.objects.filter(session_key=session_key).delete()
    return redirect('index')
def userhome(request):
    return render(request,"userhome.html")
def userchangepwd(request):
        uname=request.session["uname"]
        return render(request,"userchangepwd.html",{"uname":uname})
def userupdatepwd(request):
    uname=request.session["uname"]
    opwd=request.POST["opwd"]
    npwd=request.POST["npwd"]
    flag = SignUpData.objects.filter(Q(sign_name=uname)&Q(sign_password=opwd))
    if flag:
        SignUpData.objects.filter(sign_name=uname).update(sign_password=npwd)
        msg = "Password Updated Successfully"
        error="no"
        return render(request, "userchangepwd.html", {"uname": uname,"msg":msg,"error":error})
    else:
        msg = "Old Password is Incorrect"
        error = "yes"
        return render(request, "userchangepwd.html", {"uname": uname,"msg":msg,"error":error})
def viewusers(request):
    uname = request.session["uname"]
    usersdata = SignUpData.objects.all()
    userscount = SignUpData.objects.count()
    return render(request, "viewusers.html", {"users": usersdata, "count": userscount, "uname": uname})
def deleteuser(request,uid):
    SignUpData.objects.filter(id=uid).delete()
    return redirect("viewusers")
def viewprofile(request):
    uname = request.session["uname"]
    user = SignUpData.objects.get(sign_name=uname)
    return render(request, "viewprofile.html", { "uname": uname, "user": user})

def addproduct(request):
    uname = request.session["uname"]
    form = ProductForm()
    if request.method == "POST":
        formdata = ProductForm(request.POST,request.FILES)
        if formdata.is_valid():
            formdata.save()
            msg="Product Added Successfully"
            return render(request, "addproduct.html", {"uname":uname,"productform": form,"msg":msg})
        else:
            msg = "Failed to Add Product"
            return render(request, "addproduct.html", {"uname":uname,"productform": form, "msg": msg})
    return render(request,"addproduct.html",{"uname":uname,"productform":form})


def deleteproduct(request,uid):
    Product.objects.filter(id=uid).delete()
    return redirect("viewproducts")
def category(request,id):
    pro = Product.objects.filter(category=id)
    return render(request, "category.html", {"pro": pro})

def add_cart(request):
    user=request.session["email"]
    prid=request.POST["pid"]
    print(prid)
    cartobj=cart(mail=user,pid=prid)
    cart.save(cartobj)
    return redirect('/cart')
# def getcart(request):
#     user = request.session["email"]
#     pro=cart.objects.filter(mail=user)
#     pcount = cart.objects.filter(mail=user).count()
#     products = Product.objects.filter(id__in=Subquery(pro.values('pid')))
#     total = sum([Product.price for Product in products])
#     return render(request, "cart.html", {"pro": products,"count":pcount,"price":total})

def generate_invoice(products, total):
    template_path = 'invoice_template.html'  # Path to your invoice template HTML file
    context = {'pro': products, 'price': total}  # Context data for the invoice template
    invoice = get_template(template_path).render(context)

    # Generate PDF file
    result_file = 'invoice.pdf'  # Path where the PDF will be saved
    with open(result_file, 'wb') as output_file:
        pisa_status = pisa.CreatePDF(invoice, dest=output_file)

    if pisa_status.err:
        return None  # Error occurred while generating PDF

    return result_file  # Return the path to the generated PDF

def getcart(request):
    user = request.session["email"]
    user1 = SignUpData.objects.get(sign_email=user)
    pro = cart.objects.filter(mail=user)
    pcount = cart.objects.filter(mail=user).count()
    products = Product.objects.filter(id__in=Subquery(pro.values('pid')))
    total = sum([Product.price for Product in products])

    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        invoice_file = generate_invoice(products, total)
        if invoice_file:
            with open(invoice_file, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=invoice.pdf'
                return response
    return render(request, "checkout.html", {"pro": products, "count": pcount, "price": total,"user1":user1})
def checkout(request):
    return render(request,"checkout.html")

import csv
from django.http import HttpResponse
from .models import SignUpData

def generate_csv(request):
    # Get the data from the model
    queryset = SignUpData.objects.all()

    # Define the CSV file name
    file_name = 'signup_data.csv'

    # Create the HttpResponse object with CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    # Create the CSV writer.
    writer = csv.writer(response)

    # Write the CSV header.
    writer.writerow(['Name', 'Email', 'Password', 'Time'])

    # Write the data rows.
    for data in queryset:
        writer.writerow([data.sign_name, data.sign_email, data.sign_password, data.sign_time])

    return response
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})

from django.shortcuts import render
from .models import UploadedFile

def file_list(request):
    files = UploadedFile.objects.all()
    return render(request, 'file_list.html', {'files': files})
def file_detail(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    return render(request, 'file_detail.html', {'file': file})
def viewproducts(request):
    email=request.session["email"]
    p = SignUpData.objects.filter(sign_email=email)
    key = p[0].secure_key
    productlist = Product.objects.filter(secure_key=key)
    count = Product.objects.filter(secure_key=key).count()
    return render(request,"viewproducts.html",{"productlist":productlist,"count":count})

def viewproduct(request, product_id):
    product = Product.objects.get(pk=product_id)
    recently_viewed_products = None
    if 'recently_viewed' in request.session:
        if product_id in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(product_id)
        products = Product.objects.filter(pk__in=request.session['recently_viewed'])
        recently_viewed_products = sorted(products,
                                          key=lambda x: request.session['recently_viewed'].index(x.id)
                                          )
        request.session['recently_viewed'].insert(0, product_id)
        if len(request.session['recently_viewed']) > 5:
            request.session['recently_viewed'].pop()
    else:
        request.session['recently_viewed'] = [product_id]
    request.session.modified = True

    context = {'product': product, 'recently_viewed_products': recently_viewed_products}
    return render(request, 'product.html', context)


