from django.db import models
from django.contrib.auth.models import AbstractUser
import numpy as np
from Pyfhel import Pyfhel
import json
import pickle
import base64

# Create your models here.
class User(AbstractUser):
    balance = models.BinaryField(default=b"",blank=False, null=False)
    def __str__(self) :
        return("ID : " + str(self.id) + ", Username : " + self.email + ", Fname : " + self.first_name + ", Sname : " + self.last_name +", balance:"+str(base64.b64encode(pickle.dumps(self.balance)).decode("utf-8")))

    def to_dict(self):
        """Returns a dictionary of item contents"""

        return {
            'balance':json.dumps(base64.b64encode(pickle.dumps(self.balance)).decode("utf-8")),
            # 'balance':json.dumps(str(pickle.loads(self.balance))),
            'id': self.id,
            'username': self.username,
            'fname' : self.first_name,
            'sname': self.last_name,
        }


class Transaction(models.Model):
    Deposit= 'D'
    Withdrawal='W'
    Transfer='T'
    Type = [
        (Deposit, 'Deposit'),
        (Withdrawal, 'Withdrawal'),
         (Transfer,'Transfer'),
    ]
    type = models.CharField(
        max_length=20,
        choices=Type,
        default=Deposit,
    )
    description=models.TextField(blank=True)
    amount=models.BinaryField()
    account = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    date=models.DateTimeField(blank=False, null=False, default=None)
    def to_dict(self):
        """Returns a dictionary of item contents"""
        return {
            'id':self.id,
            # 'amount':json.dumps(base64.b64encode(pickle.dumps(self.amount)).decode("utf-8")),  #Shows the binary data
            'amount':json.dumps(str(pickle.loads(self.amount))), #returns the encrypted String value instead of binary value stored in the database

            'account' : self.account.to_dict(),
            'date':self.date,
            'type':self.type
        }