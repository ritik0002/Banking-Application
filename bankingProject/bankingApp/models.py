from django.db import models
from django.contrib.auth.models import AbstractUser
import numpy as np
from Pyfhel import Pyfhel
import json
import pickle
# Create your models here.
class User(AbstractUser):
    balance = models.BinaryField(default=b"",blank=False, null=False)
    def __str__(self) :
        return("ID : " + str(self.id) + ", Username : " + self.email + ", Fname : " + self.first_name + ", Sname : " + self.last_name +", balance:"+self.balance)  

    def to_dict(self):
        """Returns a dictionary of item contents"""

        return {
            # 'balance':json.dumps(self.balance, ensure_ascii=True),
            'balance':json.dumps(str(pickle.loads(self.balance))),
            'id': self.id,
            'username': self.username,
            'fname' : self.first_name,
            'sname': self.last_name,
        }


class Transaction(models.Model):
    Deposit= 'D'
    Withdrawal='W'
    Type = [
        (Deposit, 'Deposit'),
        (Withdrawal, 'Withdrawal'),
    ]
    type = models.CharField(
        max_length=20,
        choices=Type,
        default=Deposit,
    )
    amount=models.BinaryField()
    account = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    date=models.DateField(blank=False, null=False, default=None)
    def to_dict(self):
        """Returns a dictionary of item contents"""
        return {
            # 'amount':json.dumps(self.amount, ensure_ascii=True),
            'amount':json.dumps(str(pickle.loads(self.amount))),

            'account' : self.account.to_dict(),
            'date':self.date,
            'type':self.type
        }