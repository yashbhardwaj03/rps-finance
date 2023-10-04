from django.db import models

# Create your models here.
class CommunityType(models.Model):
    name = models.CharField(max_length=255,unique=True)
    min_limit = models.DecimalField(decimal_places=2,default=0.00)
    max_limit = models.DecimalField(decimal_places=2,default=0.00)
    savings_interest = models.DecimalField(decimal_places=2,default=0.00) # In %
    loans_interest = models.DecimalField(decimal_places=2,default=0.00) # In %
    

class Community(models.Model):
    commnuity_id = models.AutoField(primary_key=True)
    users = models.ManyToManyField('UserDetails')

    balance = models.DecimalField(decimal_places=2,default=0.00)

    # To maintain a record of who has paid the monthly savings.
    monthly_savings_payments = models.ManyToManyField('UserDetails')

    user_wise_stake = models.TextField(default="")    # Tuples in string. (user1:3000)

    # The users who haven't taken any loan and also not paying the minimum savings
    ineffective_users = models.TextField(default="")    # Tuples in string. (user1:3000)

    transactions = models.TextField(default="") # <sep> token to seperate the transactions

    community_type = models.ForeignKey(CommunityType,on_delete=models.CASCADE)

    overall_credit_score = models.IntegerField(default=0)   # 0 to 1000

    loans = models.ManyToManyField('Loans') # To keep the record of loans in this community


##################################################
# Problems
##################################################
"""
1. No functions defined
2. No specific clarification in CommunityTypes
3. Undecidability of using ManytoMany or TextField with <sep>
4. Undecidability for loans
"""