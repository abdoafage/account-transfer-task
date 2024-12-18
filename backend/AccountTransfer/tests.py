import re
from django.test import TestCase
from AccountTransfer.models import Account

# Create your tests here.


class AccountTestCase(TestCase):
    def setUp(self):
        Account.objects.create(account_id="1", name="Alice", balance=1000)
        Account.objects.create(account_id="2", name="Bob", balance=500)

    def test_import_accounts(self):
        """Test importing accounts."""
        with open("./accounts.csv", "rb") as f:
            account_file = f.read().decode("utf-8").splitlines()

        response = self.client.post(
            "/api/import_accounts/", {"file": open("./accounts.csv", "rb")}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            Account.objects.count(), 1002
        )  # 2 accounts already exist and 1000 accounts are imported from the CSV file

    def test_list_accounts(self):
        """Test listing accounts."""
        response = self.client.get("/api/accounts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_get_account(self):
        """Test retrieving a single account."""
        response = self.client.get("/api/accounts/1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Alice")
        self.assertEqual(response.json()["balance"], 1000)

        response = self.client.get("/api/accounts/2/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Bob")
        self.assertEqual(response.json()["balance"], 500)

    def test_transfer_funds(self):
        """Test transferring funds."""
        response = self.client.post(
            "/api/transfer_funds/",
            {"sender_id": "1", "recipient_id": "2", "amount": 200},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        alice = Account.objects.get(account_id="1")
        bob = Account.objects.get(account_id="2")
        self.assertEqual(alice.balance, 800)
        self.assertEqual(bob.balance, 700)

    def test_transfer_insufficient_funds(self):
        """Test transferring funds with insufficient balance."""
        response = self.client.post(
            "/api/transfer_funds/",
            {"sender_id": "2", "recipient_id": "1", "amount": 600},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Insufficient funds", response.json()["error"])
        bob = Account.objects.get(account_id="2")
        alice = Account.objects.get(account_id="1")
        self.assertEqual(bob.balance, 500)
        self.assertEqual(alice.balance, 1000)
