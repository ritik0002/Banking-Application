import json
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm,NewUserForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import *
import numpy as np
from Pyfhel import Pyfhel
import pickle


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


def users_api(request,userID):
    """API handling user balance. Fetches the balance and decrypts it."""
    if request.method == 'GET':        
        user=get_object_or_404(User,id=userID)
        if len(user.balance)==0:
            return JsonResponse({
            'user':{ 
                'balance':0
            }
        })
        else:
            # bytes_obj = user.balance.encode('utf-8')
            temp=pickle.loads(user.balance)  #turn the byte string back into object
            temp=decrypt_data(temp)[0]
            return JsonResponse({
                'user':{ 
                    'balance':str(temp)
                }
        })
   

    # elif request.method == 'POST':
    # return HttpResponse("")


# Create your views here.
def encrypt_data(val):
    '''Encrypt value'''
    HE = Pyfhel() # Create a Pyfhel object
    HE.load_context("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/Banking-Application/bankingProject/bankingApp/context") # Load context from file
    HE.load_public_key("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/Banking-Application/bankingProject/bankingApp/public.key") # Load context from file
    HE.load_secret_key("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/Banking-Application/bankingProject/bankingApp/secret.key") # Load context from file
    encrypted_data=np.array([(val*100)], dtype=np.int64)
    encrypted_data=HE.encryptInt(encrypted_data)
    return encrypted_data

def decrypt_data(val):
    '''Decrypt value'''
    HE = Pyfhel() # Create a Pyfhel object
    HE.load_context("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/Banking-Application/bankingProject/bankingApp/context") # Load context from file
    HE.load_public_key("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/Banking-Application/bankingProject/bankingApp/public.key") # Load context from file
    HE.load_secret_key("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/Banking-Application/bankingProject/bankingApp/secret.key") # Load context from file
    val=HE.decryptInt(val)/100
    return val



def transaction_filter_api(request):
    if request.method =="GET":
        withdraw = Transaction.objects.filter(type='W')
        deposit=Transaction.objects.filter(type='D')
        total1=encrypt_data(0)  # withdraw total  
        total2=encrypt_data(0)  # deposit total
        for x in withdraw:
            total1+=pickle.loads(x.amount)
        for k in deposit:
            total2+=pickle.loads(k.amount)
        total1=decrypt_data(total1)[0]
        total2=decrypt_data(total2)[0]

        return JsonResponse({
            'Transaction':{
            'withdrawals':total1,
            'deposits':total2,
            }
            
        })



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
#Withdraw Or Deposit
    elif request.method == 'POST':
        # gets the json data from the frontend
        data = json.loads(request.body)
        # Creates new object and adds it to the existing object
        userId = request.session.get('_auth_user_id')
        val=int(float(data['amount'])*100)  #Multiply by 100 as im using BFV scheme
        temp=np.array([val], dtype=np.int64)
        encrypted_data=HE.encryptInt(temp)
        transaction=Transaction.objects.create(
            type=data['type'],
            amount=pickle.dumps(encrypted_data), #turns it into binary so i can store it in Django Models..
            date=data['date'],
            account=get_object_or_404(User,id=userId)
            
        )
        user = User.objects.get(id=userId)  #get current user object

        if data['type']=='D':
            if len(user.balance)==0:
                user.balance=pickle.dumps(encrypted_data) 
                user.save()
            else:
                temp=user.balance
                # bytes_obj =temp.encode('utf-8')
                bal= pickle.loads(temp)
                bal+=encrypted_data    #adding encrypting values together!
                print("HELLLLO",(HE.noise_level((bal))))
                user.balance=pickle.dumps(bal)
                user.save()

        else:
            # Withdrawal
                temp=user.balance
                # bytes_obj =temp.encode('utf-8')
                bal= pickle.loads(temp)
                bal-=encrypted_data
                user.balance=pickle.dumps(bal)
                user.save()
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

