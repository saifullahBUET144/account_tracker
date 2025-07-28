from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.conf import settings
from django.http import HttpResponse
import cloudinary
import os
import cloudinary.uploader

def index(request):
    """The home page for Charity Tracker."""
    return render(request, 'account_logs/index.html')

@login_required
def accounts(request):
    """Show all accounts belonging to the current user."""
    accounts = Account.objects.filter(owner=request.user).order_by('date_created')
    context = {'accounts': accounts}
    return render(request, 'account_logs/account_logs.html', context)

@login_required
def account_detail(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    if account.owner != request.user:
        raise Http404
    transactions = account.transactions.order_by('-date')
    context = {'account': account, 'transactions': transactions}
    return render(request, 'account_logs/account_detail.html', context)

@login_required
def new_account(request):
    """Add a new account owned by the current user."""
    if request.method != 'POST':
        form = AccountForm()
    else:
        form = AccountForm(data=request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.owner = request.user
            new_account.save()
            return redirect('account_logs:account_logs')

    context = {'form': form}
    return render(request, 'account_logs/new_account.html', context)

import cloudinary.uploader

@login_required
def new_transaction(request, account_id):
    """Add a new transaction for a particular account."""
    account = get_object_or_404(Account, id=account_id)
    if account.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = TransactionForm()
    else:
        form = TransactionForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # Don't save the form to the DB yet
            new_transaction = form.save(commit=False)
            new_transaction.account = account

            # Check if a new receipt was uploaded
            if 'receipt' in request.FILES:
                # Upload the file directly to Cloudinary
                uploaded_file = request.FILES['receipt']
                result = cloudinary.uploader.upload(uploaded_file, folder="receipts")
                
                # Assign the returned public_id to the receipt field
                new_transaction.receipt = result['public_id']

            # Save the transaction with the correct receipt path
            new_transaction.save()
            return redirect('account_logs:account_detail', account_id=account.id)

    context = {'account': account, 'form': form}
    return render(request, 'account_logs/new_transaction.html', context)

@login_required
def edit_transaction(request, transaction_id):
    """Edit an existing transaction."""
    transaction = get_object_or_404(Transaction, id=transaction_id)
    account = transaction.account
    if account.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = TransactionForm(instance=transaction)
    else:
        form = TransactionForm(instance=transaction, data=request.POST, files=request.FILES)
        if form.is_valid():
            # Manually handle the upload
            edited_transaction = form.save(commit=False)

            if 'receipt' in request.FILES:
                uploaded_file = request.FILES['receipt']
                result = cloudinary.uploader.upload(uploaded_file, folder="receipts")
                edited_transaction.receipt = result['public_id']
            
            edited_transaction.save()
            return redirect('account_logs:account_detail', account_id=account.id)
            
    context = {'transaction': transaction, 'account': account, 'form': form}
    return render(request, 'account_logs/edit_transaction.html', context)

@login_required
def delete_account(request, account_id):
    """Delete an existing account."""
    account = get_object_or_404(Account, id=account_id)

    if account.owner != request.user:
        raise Http404

    if request.method == 'POST':
        account.delete()
        return redirect('account_logs:account_logs')

    context = {'account': account}
    return render(request, 'account_logs/delete_account.html', context)


@login_required
def delete_transaction(request, transaction_id):
    """Delete an existing transaction."""
    transaction = get_object_or_404(Transaction, id=transaction_id)
    account = transaction.account

    # Ensure the user owns the account
    if account.owner != request.user:
        raise Http404

    if request.method == 'POST':
        # User has confirmed the deletion
        transaction.delete()
        return redirect('account_logs:account_detail', account_id=account.id)

    # Display confirmation page for a GET request
    context = {'transaction': transaction, 'account': account}
    return render(request, 'account_logs/delete_transaction.html', context)

