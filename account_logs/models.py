from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
import os

# Create your models here.

class Account(models.Model):
    """A financial account for a project."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # Currency choices
    class Currency(models.TextChoices):
        BDT = 'BDT', 'Taka (BDT)'
        USD = 'USD', 'US Dollar (USD)'
        EUR = 'EUR', 'Euro (EUR)'
        GBP = 'GBP', 'Pound Sterling (GBP)'
        OTHER = 'OTHER', 'Other'

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(
        max_length=5,
        choices=Currency.choices,
        default=Currency.BDT
    )

    def __str__(self):
        """Return a string representation of the model."""
        return self.name
    
    @property
    def current_balance(self):
        """
        Calculates the current balance by taking the initial balance and
        applying all associated transactions.
        """
        inflows = self.transactions.filter(
            transaction_type='Inflow'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        expenses = self.transactions.filter(
            transaction_type='Expense'
        ).aggregate(total=Sum('amount'))['total'] or 0

        current_balance = self.initial_balance + inflows - expenses
        return current_balance
    
    @property
    def currency_symbol(self):
        symbols = {
            'BDT': '৳',
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'OTHER': '',  # No symbol for "Other"
        }
        return symbols.get(self.currency, '')

class Transaction(models.Model):
    """An inflow or expense record for an account."""
    
    TRANSACTION_TYPE_CHOICES = [
        ('Inflow', 'Inflow'),
        ('Expense', 'Expense'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(
        max_length=7,
        choices=TRANSACTION_TYPE_CHOICES,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source_or_destination = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    receipt = models.FileField(upload_to='receipts/', blank=True, null=True)

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.date}: {self.description[:50]}..."
    
    @property
    def get_cloudinary_url(self):
        """
        Manually constructs the Cloudinary URL.
        """
        if self.receipt:
            cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
            public_id = self.receipt.name
            
            # Construct the full URL
            return f"https://res.cloudinary.com/{cloud_name}/image/upload/f_auto,q_auto/{public_id}"
        return None
