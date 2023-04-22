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
import math
from datetime import datetime

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

def user_api(request):
    if request.method == 'GET': 
        return JsonResponse({
            'user': [
                user.to_dict()
                for user in User.objects.all()
            ]
        })

def users_api(request,userID):
    """API handling user balance. Fetches the balance and decrypts it."""
    if request.method == 'GET': 
        # return HttpResponse("checkQ",request.user.id)
        # userID=request.session.get('_auth_user_id')     
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
   
def deleteUser(request):
    data=json.loads(request.body)
    # return HttpResponse(data['username'])

    user = get_object_or_404(User, username=data['username'])
    # return HttpResponse(user)
    user.delete()
    return JsonResponse({
        'response':"user deleted!",
                         })




# Create your views here.
def encrypt_data(val):
    '''Encrypt value'''
    HE = Pyfhel() # Create a Pyfhel object
    HE.load_context("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/bankingApp/context") # Load context from file
    HE.load_public_key("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/bankingApp/public.key") # Load context from file
    HE.load_secret_key("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/bankingApp/secret.key") # Load context from file
    encrypted_data=np.array([(val*100)], dtype=np.int64)
    encrypted_data=HE.encryptInt(encrypted_data)
    return encrypted_data

def decrypt_data(val):
    '''Decrypt value'''
    HE = Pyfhel() # Create a Pyfhel object
    HE.load_context("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/bankingApp/context") # Load context from file
    HE.load_public_key("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/bankingApp/public.key") # Load context from file
    HE.load_secret_key("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/bankingApp/secret.key") # Load context from file
    val=HE.decryptInt(val)/100
    return val


def Calculator(request):
    """Handles saving Calculator """
    data=json.loads(request.body)
    #use given balance
    result=0


    if data['check']=="no":
        if float(data['balance'])>=float(data['goal']):
            return JsonResponse({
                'response':"Balance is greater or already equal to the saving goal",

            })
        # return HttpResponse(data['goal'])
        amount=float(data['goal'])-float(data['balance'])
        result=amount/float(data['amount'])
        result=math.ceil(result)  #round up
        
        return JsonResponse({
            'response':f"To achieve £{amount} it will take {result} months",

        })
    elif data['check']=="yes":
        #get current balance
        userId = request.session.get('_auth_user_id')
        user = User.objects.filter(id=userId)[0]
        if len(user.balance)==0:
            balance=0
        else:
            temp=pickle.loads(user.balance)  #turn the byte string back into object
            balance=decrypt_data(temp)[0]
        if balance>=float(data['goal']):
            return JsonResponse({
                'response':"Balance is greater or already equal to the saving goal",

            })
        else:
            amount=float(data['goal'])-balance
            result=amount/float(data['amount'])
            result=math.ceil(result)  #round up   
            return JsonResponse({
                'response':f"To achieve £{amount} it will take {result} months",

            })


def current_transaction_api(request,TransactionId:int):
    if request.method =="GET":
        transaction = get_object_or_404(Transaction, id=TransactionId)
        amount=pickle.loads(transaction.amount)
        amount=decrypt_data(amount)[0]
        return JsonResponse({
            'Transaction':{
            'amount':amount,
            }
            
        })
def transaction_filter_api(request,userID):
    if request.method =="GET":
        withdraw = Transaction.objects.filter(account__id=userID,type='W')
        deposit=Transaction.objects.filter(account__id=userID,type='D')
        transfer=Transaction.objects.filter(account__id=userID,type='T')
        total1=encrypt_data(0)  # withdraw total  
        total2=encrypt_data(0)  # deposit total
        total3=encrypt_data(0)  # deposit total

        for x in withdraw:
            total1+=pickle.loads(x.amount)
        for k in deposit:
            total2+=pickle.loads(k.amount)
        for k in transfer:
            total3+=pickle.loads(k.amount)    
        total1=decrypt_data(total1)[0]
        total2=decrypt_data(total2)[0]
        total3=decrypt_data(total3)[0]

        return JsonResponse({
            'Transaction':{
            'withdrawals':total1,
            'deposits':total2,
            'transfer':total3,
            }
            
        })



def transaction_api(request,userID):
    user=get_object_or_404(User,id=userID)
    HE = Pyfhel() # Create a Pyfhel object
    HE.load_context("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/bankingApp/context") # Load context from file
    HE.load_public_key("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/bankingApp/public.key") # Load context from file
    HE.load_secret_key("C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/bankingApp/secret.key") # Load context from file
    # HE.load_public_key("public.key") # Load public key from file
    # HE.load_secret_key("secret.key") # Load secret key from file
    if request.method == 'GET':
        # val=np.array([1499], dtype=np.int64)
        # encrypted_data=HE.encryptInt(val)
        # decrypted_data =HE.decryptInt(encrypted_data)[0]
        # decrypted_data=decrypted_data/100

        
        return JsonResponse({
            # 'encrypted_data':str(encrypted_data),
            # 'decrypted_data':str(decrypted_data),
            'Transaction': [
                # Gives the data for the object
                Transaction.to_dict()
                # Transportation.object.all() gets all the transportation objects
                for Transaction in (Transaction.objects.filter(account__id=userID).order_by('-date'))
            ]
        })
#Withdraw Or Deposit
    elif request.method == 'POST':
        # gets the json data from the frontend
        data = json.loads(request.body)
        # Creates new object and adds it to the existing object
        userId = userID
        val=int(float(data['amount'])*100)  #Multiply by 100 as im using BFV scheme
        temp=np.array([val], dtype=np.int64)
        encrypted_data=HE.encryptInt(temp)
        transaction=Transaction.objects.create(
            type=data['type'],
            amount=pickle.dumps(encrypted_data), #turns it into binary so i can store it in Django Models..
            date=data['date'],
            account=get_object_or_404(User,id=userId),
            description=data.get('desc', ""),
        )
        user = User.objects.get(id=userID)  #get current user object

        if data['type']=='D':
            if len(user.balance)==0:
                user.balance=pickle.dumps(encrypted_data) 
                user.save()
            else:
                temp=user.balance
                # bytes_obj =temp.encode('utf-8')
                bal= pickle.loads(temp)
                bal+=encrypted_data    #adding encrypting values together!
                user.balance=pickle.dumps(bal)
                user.save()

        elif data['type']=='W':
            # Withdrawal
                temp=user.balance
                # bytes_obj =temp.encode('utf-8')
                bal= pickle.loads(temp)
                bal-=encrypted_data
                user.balance=pickle.dumps(bal)
                user.save()
        else:
            #Transfer
            #withdraw user account
            temp=user.balance
            # bytes_obj =temp.encode('utf-8')
            bal= pickle.loads(temp)
            bal-=encrypted_data
            user.balance=pickle.dumps(bal)
            user.save()
            #deposit sender account
            sender=get_object_or_404(User,username=data['username'])
            temp2=sender.balance
            bal2=pickle.loads(temp2)
            bal2+=encrypted_data
            sender.balance=pickle.dumps(bal2)
            sender.save()
          #create transfer object to sender
            transaction=Transaction.objects.create(
            type=data['type'],
            amount=pickle.dumps(encrypted_data), #turns it into binary so i can store it in Django Models..
            date=data['date'],
            description="(Recipient)\n"+data['desc'],
            account=sender
            
        )
        return JsonResponse({
            'transaction':[Transaction.objects.filter(type=data['type'])]
            })


def superUser(request):
    userId = request.session.get('_auth_user_id')
    user=get_object_or_404(User,id=userId)
    return JsonResponse({
        'check': user.is_superuser
    })
  

"""Support page"""
def support(request):
    if request.method == 'GET':
        return JsonResponse({
            # 'encrypted_data':str(encrypted_data),
            # 'decrypted_data':str(decrypted_data),
            'Tickets': [
                # Gives the data for the object
                Support.to_dict()
                for Support in Support.objects.all()

            ]
        })
    if request.method == 'POST':
        data = json.loads(request.body)
        ticket=Support.objects.create(
            subject=data['subject'],
            description=data['description'],
            account=get_object_or_404(User,username=data['username']),
            date=datetime.now(),
        )
        return JsonResponse({
            'Ticket':ticket
            })



"""" Login,logout,home pages"""
def home(request):
        return render(request, 'home.html')



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
    


def password(request):
    data = json.loads(request.body)

    user= authenticate(username=data['username'],password=data['password'])
    if user is not None:
        # The credentials are valid
        user.set_password(data['new_password'])
        user.save()
        return JsonResponse({
            'response':"password updated!",
        })
    else:
        # The credentials are invalid
        return JsonResponse({
            'response':"password is incorrect!",
        })

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

