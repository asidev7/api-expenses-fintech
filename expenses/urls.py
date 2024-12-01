from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WalletViewSet,
    ExpenseViewSet,
    IncomeViewSet,
    TransactionViewSet,
    ExpenseCategoryViewSet,
    IncomeCategoryViewSet,
    register
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Créer un routeur pour enregistrer les ViewSets
router = DefaultRouter()
router.register(r'wallets', WalletViewSet, basename='wallet')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'incomes', IncomeViewSet, basename='income')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'expense-categories', ExpenseCategoryViewSet, basename='expense-category')
router.register(r'income-categories', IncomeCategoryViewSet, basename='income-category')

# Inclusion des routes du routeur dans urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Inclut toutes les routes générées par le routeur
    path('register/', register, name='register'),

    # Routes pour la gestion des tokens JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

