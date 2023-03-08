import json
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm,NewUserForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import *
import numpy as np
from Pyfhel import Pyfhel



def sessionUser(request):
    """checks to see if user is logged in"""
    
    if request.method == 'GET':
        userId = request.session.get('_auth_user_id')
        try:
            sessionUser = User.objects.filter(id=userId)[0]
        except IndexError:
            return JsonResponse({
                'User': "None"
            })
        
        return JsonResponse({
            'User':
                sessionUser.to_dict()
        })

    return HttpResponse("")

def users_api(request):
    """API handling all users. GET request returns JSON of all objects. POST request adds new user record and returns it."""
    # if request.method == 'GET':
    #     return JsonResponse({
    #         'user': [
    #             user.to_dict()
    #             for user in User.objects.all()
    #         ]
    #     })

    # elif request.method == 'POST':
    # return HttpResponse("")
    pass


# Create your views here.
def encrypt_data(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        p = Pyfhel()
        encrypted_data = p.encrypt(data)
        return JsonResponse({'encrypted_data': encrypted_data})



def transaction_api(request):
    HE = Pyfhel() # Create a Pyfhel object
    HE.load_context("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/Banking-Application/bankingProject/bankingApp/context") # Load context from file
    HE.load_public_key("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/Banking-Application/bankingProject/bankingApp/public.key") # Load context from file
    HE.load_secret_key("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/Banking-Application/bankingProject/bankingApp/secret.key") # Load context from file
    # HE.load_public_key("public.key") # Load public key from file
    # HE.load_secret_key("secret.key") # Load secret key from file
    if request.method == 'GET':
        val=np.array([1499], dtype=np.int64)

        encrypted_data=HE.encryptInt(val)
        decrypted_data =HE.decryptInt(encrypted_data)[0]
        decrypted_data=decrypted_data/100
    
        
        return JsonResponse({
            'encrypted_data':str(encrypted_data),
            'decrypted_data':str(decrypted_data),
            'Transaction': [
                # Gives the data for the object
                Transaction.to_dict()
                # Transportation.object.all() gets all the transportation objects
                for Transaction in Transaction.objects.all()
            ]
        })

    elif request.method == 'POST':
        # gets the json data from the frontend
        data = json.loads(request.body)
        # Creates new object and adds it to the existing object
        userId = request.session.get('_auth_user_id')

        transaction=Transaction.objects.create(
            type=data['type'],
            amount=data['amount'],
            date=data['date'],
            account=get_object_or_404(User,id=userId)
        )
        return JsonResponse({
            'transaction':[transaction.to_dict()]
            })
        

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')    
        # print(username,password)    
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            response = redirect('http://127.0.0.1:5173/')          
            return response
    return render(request, 'login.html')
    

def logout_view(request):
    logout(request)
    return redirect('login')


def register(request):
    context = {}
    if request.POST:
        form = NewUserForm(request.POST)
        if form.is_valid():
            account = form.save()
            login(request, account)
            response = redirect('http://127.0.0.1:5173/') 
            return response      
        else:
            context['register'] = form
    else:
        form = NewUserForm()
        context['register'] = form
    return render(request, 'register.html', context)   

