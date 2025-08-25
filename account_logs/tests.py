from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Account, Transaction
from decimal import Decimal
import datetime

# HELPER FUNCTIONS

def create_user(username='testuser', password='password'):
    """Helper function to create a user."""
    return User.objects.create_user(username=username, password=password)

def create_account(owner, name='Test Account', initial_balance=1000.00):
    """Helper function to create an account."""
    return Account.objects.create(
        owner=owner,
        name=name,
        initial_balance=Decimal(initial_balance)
    )

def create_transaction(account, trans_type='Expense', amount=100.00, days_ago=0):
    """Helper function to create a transaction."""
    return Transaction.objects.create(
        account=account,
        transaction_type=trans_type,
        amount=Decimal(amount),
        source_or_destination='Test Source',
        description='Test Transaction',
        date=datetime.date.today() - datetime.timedelta(days=days_ago)
    )

# MODEL TESTS

class AccountModelTests(TestCase):
    """Tests for the Account model."""

    def setUp(self):
        """Set up a user and an account for testing."""
        self.user = create_user()
        self.account = create_account(self.user, initial_balance='5000.50')

    def test_account_creation(self):
        """Test if an account is created successfully."""
        self.assertEqual(self.account.name, 'Test Account')
        self.assertEqual(self.account.owner, self.user)
        self.assertEqual(self.account.initial_balance, Decimal('5000.50'))
        self.assertEqual(str(self.account), 'Test Account')

    def test_current_balance_no_transactions(self):
        """Test the current_balance property with no transactions."""
        self.assertEqual(self.account.current_balance, self.account.initial_balance)

    def test_current_balance_with_inflows(self):
        """Test the current_balance property with inflow transactions."""
        create_transaction(self.account, trans_type='Inflow', amount='1000.00')
        create_transaction(self.account, trans_type='Inflow', amount='500.25')
        expected_balance = Decimal('5000.50') + Decimal('1000.00') + Decimal('500.25')
        self.assertEqual(self.account.current_balance, expected_balance)

    def test_current_balance_with_expenses(self):
        """Test the current_balance property with expense transactions."""
        create_transaction(self.account, trans_type='Expense', amount='250.00')
        create_transaction(self.account, trans_type='Expense', amount='75.50')
        expected_balance = Decimal('5000.50') - Decimal('250.00') - Decimal('75.50')
        self.assertEqual(self.account.current_balance, expected_balance)

    def test_current_balance_mixed_transactions(self):
        """Test the current_balance property with both inflows and expenses."""
        create_transaction(self.account, trans_type='Inflow', amount='1000.00')
        create_transaction(self.account, trans_type='Expense', amount='300.00')
        expected_balance = Decimal('5000.50') + Decimal('1000.00') - Decimal('300.00')
        self.assertEqual(self.account.current_balance, expected_balance)

    def test_currency_symbol(self):
        """Test the currency_symbol property."""
        self.account.currency = 'USD'
        self.account.save()
        self.assertEqual(self.account.currency_symbol, '$')
        
        self.account.currency = 'EUR'
        self.account.save()
        self.assertEqual(self.account.currency_symbol, '€')

class TransactionModelTests(TestCase):
    """Tests for the Transaction model."""

    def setUp(self):
        """Set up a user, account, and transaction for testing."""
        self.user = create_user()
        self.account = create_account(self.user)
        self.transaction = create_transaction(self.account)

    def test_transaction_creation(self):
        """Test if a transaction is created successfully."""
        self.assertEqual(self.transaction.account, self.account)
        self.assertEqual(self.transaction.transaction_type, 'Expense')
        self.assertEqual(self.transaction.amount, Decimal('100.00'))
        self.assertIn('Test Transaction', str(self.transaction))

# VIEW TESTS

class AccountLogsViewTests(TestCase):
    """Tests for the views in the account_logs app."""

    def setUp(self):
        """Set up a client, users, and accounts for view testing."""
        self.client = Client()
        self.user1 = create_user(username='user1')
        self.user2 = create_user(username='user2')
        self.account1 = create_account(self.user1, name='User1 Account')
        self.transaction1 = create_transaction(self.account1)

    def test_index_view(self):
        """Test the index (home page) view."""
        response = self.client.get(reverse('account_logs:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_logs/index.html')

    def test_accounts_list_view_unauthenticated(self):
        """Test that unauthenticated users are redirected from the accounts list."""
        response = self.client.get(reverse('account_logs:account_logs'))
        self.assertEqual(response.status_code, 302) # 302 is a redirect
        self.assertRedirects(response, '/users/login/?next=/account_logs/')

    def test_accounts_list_view_authenticated(self):
        """Test that authenticated users can see their own accounts."""
        self.client.login(username='user1', password='password')
        response = self.client.get(reverse('account_logs:account_logs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_logs/account_logs.html')
        self.assertContains(response, 'User1 Account')
        self.assertNotContains(response, 'User2 Account') # Make sure user1 can't see user2's accounts

    def test_account_detail_view_owner(self):
        """Test that an account owner can view their account details."""
        self.client.login(username='user1', password='password')
        response = self.client.get(reverse('account_logs:account_detail', args=[self.account1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_logs/account_detail.html')
        self.assertContains(response, 'User1 Account')
        self.assertContains(response, 'Test Transaction')

    def test_account_detail_view_not_owner(self):
        """Test that a user cannot view another user's account details."""
        self.client.login(username='user2', password='password')
        response = self.client.get(reverse('account_logs:account_detail', args=[self.account1.id]))
        self.assertEqual(response.status_code, 404) # Should raise Http404

    def test_new_account_view_post(self):
        """Test creating a new account via a POST request."""
        self.client.login(username='user1', password='password')
        data = {
            'name': 'New Savings Account',
            'initial_balance': '2500',
            'currency': 'BDT'
        }
        response = self.client.post(reverse('account_logs:new_account'), data)
        self.assertEqual(response.status_code, 302) # Redirects on success
        self.assertTrue(Account.objects.filter(name='New Savings Account').exists())

    def test_delete_transaction_view(self):
        """Test deleting a transaction."""
        self.client.login(username='user1', password='password')
        response = self.client.post(reverse('account_logs:delete_transaction', args=[self.transaction1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Transaction.objects.filter(id=self.transaction1.id).exists())
