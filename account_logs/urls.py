"""Defines URL patterns for account_logs."""

from django.urls import path
from . import views

app_name = 'account_logs'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that shows all accounts.
    path('account_logs/', views.accounts, name='account_logs'),
    # Detail page for a single account.
    path('account_logs/<int:account_id>/', views.account_detail, name='account_detail'),
    # Page for adding a new account
    path('new_account/', views.new_account, name='new_account'),
    # Page for adding a new transaction.
    path('new_transaction/<int:account_id>/', views.new_transaction, name='new_transaction'),
    # Page for adding a new inflow.
    path('account_logs/<int:account_id>/new_transaction/', views.new_transaction, name='new_transaction'),
    # Page for editing a transaction.
    path('edit_transaction/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    # Add this new path for deleting a transaction
    path('delete_transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    # Page for deleting an existing account.
    path('delete_account/<int:account_id>/', views.delete_account, name='delete_account'),

]