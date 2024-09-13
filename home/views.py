from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate ,login,logout
from userlog1 import settings
from django.core.mail import send_mail,EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode ,urlsafe_base64_decode
from django.utils.encoding import force_bytes , force_str
from .tokens import generate_token
from home.models import Contact
# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect('/login')
    return render(request,'index.html')
def loginuser(request):
    if request.method=="POST":
        username=request.POST.get('email') 
        password=str(request.POST.get('password')) 
        user = authenticate(username=username , password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request,user)
            
            return redirect('/')
        else:   
            messages.error(request,"Bad Credentials!")
            # No backend authenticated the credentials
            return render(request,'login.html')
    return render(request,'login.html')
def logoutuser(request):
    logout(request)
    return redirect('/login')
def signup(request):
    if request.method=="POST":
        username=request.POST.get('username')
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        contact=Contact(username=username, cpassword=cpassword)
        contact.save()
        if User.objects.filter(username=username):
            messages.error(request,"Username already exist,Try new username!")
            return redirect('/signup')
        if len(username)>10:
            messages.error(request,"Username must be less than 10 characters")
            return redirect('/signup')
        if(password!=cpassword):
            messages.error(request,"Password not Matching!")
            return redirect('/signup')
        user = User.objects.create_user(username,email, password)
        messages.success( request , "Account Created Successfully!\nWe have sent u a confirmation email,Please confirm your email address in order to activate your account.")
        user.is_active=False
        user.save()
        #welcome email
        subject="welcome to Prinve59 -Django Login"
        message="Hello "+ user.username + "!!\n"+"Welcome to Prinve59.\nThank you for visiting our Website!\nWe have sent u a confirmation email,Please confirm your email address in order to activate your account.\n\n\nThanking you!\n Prince"
        from_email=settings.EMAIL_HOST_USER     
        to_list=[user.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)
        

        current_site=get_current_site(request)
        email_subject="Confirm your email"
        message2=render_to_string('email_confirmation.html',{
            'name':user.username,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user),
        })
        email=EmailMessage(
            email_subject,  
            message2,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.fails_silently=True
        email.send()
    return render(request,"signup.html")

def activate(request , uidb64 , token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    
    if user is not None and generate_token.check_token(user,token):
        user.is_active=True
        user.save()
        login(request,user)
        return redirect('home')
    else:
        return render(request,'activation_failed.html')