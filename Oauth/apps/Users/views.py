from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
import bcrypt

from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse


class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')

@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)

def index(request):
    #Check is still logged in
    if 'user_id' in request.session:
        return redirect('/dashboard')
    return render(request, 'Users/login.html')

def registrationprocess(request):
    #Run validations
    errors = User.objects.validator(request.POST)
    #run the validation messsages
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        #if successfully pass validations, bcrypt password
        pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        #insert into database for the registered user
        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pwhash)
        #create a session that shows the user first name when logged in
        request.session['name'] = request.POST['first_name']
        #save the user ID for future needs (which is always)
        request.session['user_id'] = user.id
        #display successfu
        messages.add_message(request, messages.INFO, "Successfully logged-in!")
        return redirect('/dashboard')

def login(request):
    #check if logged in
    if 'user_id' in request.session:
        return redirect('/')
    #run validations to check for login (email and password)
    errors = User.objects.loginvalidator(request.POST)
    #pop messages if failure occurs
    if len(errors):
        for key,values in errors.items():
            messages.error(request, values)
        return redirect('/')
    else:
        #need to get user name via querying by email
        request.session['name'] = User.objects.get(email=request.POST['email']).first_name
        #also get user_id which important for everything
        request.session['user_id'] = User.objects.get(email=request.POST['email']).id
        return redirect('/dashboard')

def dashboard(request):
    #check if not logged in
    if not 'user_id' in request.session:
        return redirect('/')
    #create context to pass information to render
    context = {}
    #create a query with user to get name to render through context via show name without using sessions
    user = User.objects.get(id=request.session['user_id'])
    context['username'] = f'{user.first_name} {user.last_name}'
    return render(request,'Users/dashboard.html', context)

def logout(request):
    #delete current session
    request.session.clear()
    #display messages if logged out
    messages.add_message(request, messages.INFO, "You have been logged out.")
    return redirect('/')
