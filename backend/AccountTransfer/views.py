from os import name
from django.db import models, transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from AccountTransfer.models import Account
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
import csv
# Create your views here.


@csrf_exempt
@api_view(['POST'])
def import_accounts(request):
    """Import accounts from a CSV file."""
    file = request.FILES["file"]

    if not file.name.endswith('.csv'):
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            Account.objects.create(
                account_id=row['ID'],
                name=row['Name'],
                balance=float(row['Balance'])
            )
        return Response({'message': 'Accounts imported successfully.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def list_accounts(request):
    """List all accounts."""
    accounts = Account.objects.all()
    
    data = [{'account_id': acc.account_id, 'name': acc.name, 'balance': acc.balance} for acc in accounts]
    return Response(data)

@api_view(['GET'])
def get_account(request, account_id):
    """Get details of a specific account."""
    
    try:
        account = Account.objects.filter(account_id=account_id).first()
        data = {'account_id': account.account_id, 'name': account.name, 'balance': account.balance}
        return Response(data)
    except Account.DoesNotExist:
        return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def transfer_funds(request):
    """Transfer funds between two accounts."""
    data = JSONParser().parse(request)
    sender_id = data.get('sender_id')
    recipient_id = data.get('recipient_id')
    amount = data.get('amount')

    if not sender_id or not recipient_id or not amount:
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            sender = Account.objects.get(account_id=sender_id)
            recipient = Account.objects.get(account_id=recipient_id)

            if sender.balance < amount:
                return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

            sender.balance -= amount
            recipient.balance += amount
            sender.save()
            recipient.save()

        return Response({'message': 'Transfer successful.'})
    except Account.DoesNotExist:
        return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])   
def delete_all(request):
    Account.objects.all().delete()
    return JsonResponse({"message": "All accounts deleted."})

def home(request):
    return render(request, 'index.html', {"accounts": Account.objects.all()})

def account_details(request, account_id):
    print(f"{account_id=}")
    try:
        account = Account.objects.filter(account_id=account_id).first()
        return render(request, 'account_details.html', {"account": account})
    except Account.DoesNotExist:
        return render(request, 'account_details.html', {"error_message": "Account not found."})