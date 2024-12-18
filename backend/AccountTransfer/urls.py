from django.urls import path
from .views import account_details, delete_all, import_accounts, list_accounts, get_account, transfer_funds,home

urlpatterns = [
    path('api/import_accounts/', import_accounts, name='transfer'),
    path('api/accounts/', list_accounts, name='accounts'),
    path('api/accounts/<str:account_id>/', get_account, name='account-detail'),
    path('api/transfer_funds/', transfer_funds, name='transfer_funds'),
    path("api/delete_all/", delete_all, name="delete_all"),
    path('home/', home, name='home'),
    path('account_details/<str:account_id>/', account_details, name='account_details'),
]