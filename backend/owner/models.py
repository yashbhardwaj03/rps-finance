from django.db import models
import json

class Owner(models.Model):
    owner_name = models.CharField(max_length=255,default="Owner")
    UPI_Id = models.CharField(max_length=255, unique=True)  # UPI Id (In case of multiple UPI accounts)
    isActive = models.BooleanField(default=False) 

    max_safe_limit = models.IntegerField(default=100000)    # A warning type to switch the account
    min_safe_limit = models.IntegerField(default=1000)    # A warning type to switch the account
    Transaction_history = models.TextField(default="")  # Transaction_history []
    Total_transaction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total_transaction_amount (On Yearly or monthly basis)
    Overall_income_gain = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Overall_income_gain (Amount the owner is going to have in his UPI_Id)

    def __str__(self):
        return self.UPI_Id

    def add_transaction(self, transaction):
        transaction_history = self.Transaction_history.split('<sep>')
        transaction_history.append(transaction)
        self.Transaction_history = '<sep>'.join(transaction_history)
        self.save()

    def update_total_transaction_amount(self, amount):
        self.Total_transaction_amount += amount
        self.save()

    def update_overall_income_gain(self, amount):
        self.Overall_income_gain += amount
        self.save()

    def get_transaction_history(self):
        return self.Transaction_history.split('<sep>')

    def update_max_safe_limit(self,limit):
        self.max_safe_limit = limit
        self.save()

    def update_min_safe_limit(self,limit):
        self.min_safe_limit = limit
        self.save()

class Token(models.Model):
    user_id = models.ForeignKey('UserDetails', on_delete=models.CASCADE)  # User Id
    onwer_id = models.ForeignKey(Owner,on_delete=models.CASCADE) # Owner Id associated with it
    community_id = models.ForeignKey('Community', on_delete=models.CASCADE)  # Community Id

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')  # Status (Pending / Approved / Rejected)

    TRANSACTION_CHOICES = [
        ('Savings Payment', 'Savings Payment'),
        ('Loan Payment', 'Loan Payment'),
        ('Withdraw', 'Withdraw'),
    ]
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_CHOICES)  # Transaction Type

    ROLE_CHOICES = [
        ('Reciever','reciever'),
        ('Sender','sender')
    ]
    onwer_role = models.CharField(max_length=10,choices=ROLE_CHOICES)
    user_role = models.CharField(max_length=10,choices=ROLE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount

    # In case of Owner paying to user (as Loans) the UPI Id of the user will appear here.
    upi_id = models.CharField(max_length=255)  # UPI Id (Active UPI_Id is used here.)

    def save(self, *args, **kwargs):
        # Ensure that owner_role and user_role cannot have the same value
        if self.owner_role == self.user_role:
            raise ValueError("Owner role and user role cannot be the same.")
        
        # If owner_role is 'Receiver,' set user_role to 'Sender'
        if self.owner_role == 'Receiver':
            self.user_role = 'Sender'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Token ID: {self.pk}, Status: {self.status}"

    def update_token_status(self,status):
        """
        Approve the token (change status to Approved).
        """
        self.status = status
        self.save()

class Loans(models.Model):
    loan_id = models.AutoField(primary_key = True)
    amount = models.DecimalField(decimal_places=2,default=0.00)
    user = models.ForeignKey('UserDetails',on_delete=models.CASCADE)
    interest_rate = models.DecimalField(decimal_places=2,defualt=0.00)  # In %

############################################
# Problems
############################################
'''
1. Signaling system needs to be implemented.
2. Updating the user and owner tokens in transaction_history.
3. Loans model clarification.
'''