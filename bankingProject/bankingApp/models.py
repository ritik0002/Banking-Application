from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    balance = models.FloatField(default=0)
    def __str__(self) :
        return("ID : " + str(self.id) + ", Username : " + self.email + ", Fname : " + self.first_name + ", Sname : " + self.last_name)  

    def to_dict(self):
        """Returns a dictionary of item contents"""

        return {
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
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    account = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    date=models.DateField(blank=False, null=False, default=None)
    
    def to_dict(self):
        """Returns a dictionary of item contents"""
        return {
            'amount': self.amount,
            'account' : self.account.to_dict(),
            'date':self.date,
            'type':self.type
        }