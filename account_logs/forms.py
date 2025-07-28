# account_logs/forms.py
from django import forms
from .models import Account, Transaction

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'description', 'initial_balance', 'currency']
        labels = {
            'name': 'Account Name', 
            'description': 'Description', 
            'initial_balance': 'Initial Balance',
            'currency': 'Currency',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'initial_balance': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-select'}),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        # Add 'transaction_type' to the list of fields.
        fields = ['transaction_type', 'amount', 'source_or_destination',
                  'description', 'date', 'receipt']
        labels = {
            'transaction_type': 'Type of Transaction',
            'amount': 'Amount',
            'source_or_destination': 'Source/Destination',
            'description': 'Description',
            'date': 'Date',
            'receipt': 'Attach a Receipt (Optional)',
        }
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'source_or_destination': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'receipt': forms.FileInput(attrs={'class': 'form-control'}),
        }
