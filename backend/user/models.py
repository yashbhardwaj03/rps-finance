from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

# Create your models here.
class UserDetails(AbstractUser):
    # Password field is provided By Default from User model of Django. (SHA256 hashing)
    # Email (default provided from Django user model)

    # Customizing the username field. (Not using default username as it is unique=True)
    username = models.CharField(max_length=255,null=True,unique=False,blank=False) 
    user_id = models.AutoField(primary_key=True)

    # No two account can have these details as same
    upi_id = models.CharField( max_length=255,unique=True,blank=False) 
    pan = models.CharField(max_length=255,unique=True,blank=False)
    aadhar = models.CharField(max_length=255,unique=True,blank=False)
    kyc_verified = models.BooleanField(default=False)

    # Nominee Detials
    nominee_name = models.CharField(max_length=255,null=True,unique=False,blank=False)
    nominee_pan = models.CharField(max_length=255,blank=False)
    nominee_aadhar = models.CharField(max_length=255,blank=False)

    # Array Based Fields (use <sep> as seperator between the list items.)
    transaction_history = models.TextField(default="")
    communities = models.TextField(default="")
    loans = models.TextField(default="")

    # These fields will be calculated on user usage.
    credit_score = models.IntegerField(default=0)   # Rating from 0 to 1000

    # Update the KYC verification status
    def update_user_kyc(self, new_val):
        self.kyc_verified = new_val
        self.save()

    # Update the username
    def update_username(self, name):
        self.username = name
        self.save()

    # Update the user's password (provide the new password as plain text)
    def update_password(self, new_password):
        self.password = make_password(new_password)
        self.save()

    # Add a transaction to the user's transaction history
    def add_transaction(self, transaction):
        if self.transaction_history == "":
            self.transaction_history = transaction
        else:
            self.transaction_history += f"<sep>{transaction}"
        self.save()

    # Get the user's transaction history as a list
    def get_transaction_history(self):
        return self.transaction_history.split("<sep>") if self.transaction_history != "" else []

    # Add a community to the user's communities
    def add_community(self, community):
        if self.communities == "":
            self.communities = community
        else:
            self.communities += f"<sep>{community}"
        self.save()

    # Get the user's communities as a list
    def get_communities(self):
        return self.communities.split("<sep>") if self.communities != "" else []

    # Add a loan to the user's loans
    def add_loan(self, loan):
        if self.loans == "":
            self.loans = loan
        else:
            self.loans += f"<sep>{loan}"
        self.save()

    # Get the user's loans as a list
    def get_loans(self):
        return self.loans.split("<sep>") if self.loans != "" else []

    # Calculate and update the user's credit score based on usage
    def update_credit_score(self):
        self.save()

    # Calculate the credit score based on user's details
    def update_credit_score(self):
        # Initialize the credit score
        credit_score = 0

        # Factor 1: Nominee Information
        if self.nominee_name and self.nominee_pan and self.nominee_aadhar:
            credit_score += 100  # Full points for complete nominee information
        # Factor 2: Transaction History
        transaction_history = self.get_transaction_history()
        if len(transaction_history) >= 3:
            credit_score += 100  # Full points for having at least 3 transactions
        # Factor 3: Community Participation
        communities = self.get_communities()
        if len(communities) >= 2:
            credit_score += 100  # Full points for participating in at least 2 communities

        # Factor 4: Loan History (Weighted 600 points)
        loans = self.get_loans()
        if len(loans) == 0:
            credit_score += 600  # Full points for no outstanding loans
        else:
            # Calculate points for loans based on some criteria (you can define your own logic)
            loan_points = 200
            credit_score += min(loan_points, 600)  # Maximum weight for loans is 600

        # Ensure the credit score is within the range [0, 1000]
        credit_score = min(max(credit_score, 0), 1000)

        # Update and save the calculated credit score
        self.credit_score = credit_score
        self.save()

        return credit_score

    # Calculate points for loans (adjust this logic based on your criteria)
    def calculate_loan_points(self, loans):
        # Example logic: Assign points based on the number of loans
        # You can replace this with your own criteria
        return min(len(loans) * 100, 600)


##################################################
# Problems
##################################################
"""
1. Is additional field needs to store loans even it they are re-paid?
2. Credit calculation ?

"""