from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Wallet, Expense, Income, Transaction, ExpenseCategory, IncomeCategory
from .serializers import (
    WalletSerializer,
    ExpenseSerializer,
    IncomeSerializer,
    TransactionSerializer,
    ExpenseCategorySerializer,
    IncomeCategorySerializer
)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password



@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        data = request.data
        try:
            # Crée un nouvel utilisateur
            user = User.objects.create(
                username=data['username'],
                email=data['email'],
                password=make_password(data['password']),
            )
            user.save()
            
            # Crée un token JWT pour cet utilisateur
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
# Viewset pour gérer les Wallets
class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def perform_create(self, serializer):
        # Associe le wallet à l'utilisateur connecté
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Retourne uniquement les wallets de l'utilisateur connecté
        return Wallet.objects.filter(user=self.request.user)

# Viewset pour gérer les Dépenses
class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def perform_create(self, serializer):
        # Associe la dépense au wallet de l'utilisateur connecté
        wallet = Wallet.objects.get(user=self.request.user)
        serializer.save(wallet=wallet)

    def get_queryset(self):
        # Retourne uniquement les dépenses du wallet de l'utilisateur connecté
        wallet = Wallet.objects.get(user=self.request.user)
        return Expense.objects.filter(wallet=wallet)

# Viewset pour gérer les Revenus
class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def perform_create(self, serializer):
        # Associe le revenu au wallet de l'utilisateur connecté
        wallet = Wallet.objects.get(user=self.request.user)
        serializer.save(wallet=wallet)

    def get_queryset(self):
        # Retourne uniquement les revenus du wallet de l'utilisateur connecté
        wallet = Wallet.objects.get(user=self.request.user)
        return Income.objects.filter(wallet=wallet)

# Viewset pour gérer les Transactions
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        # Associe la transaction au wallet de l'utilisateur connecté
        wallet = Wallet.objects.get(user=self.request.user)
        serializer.save(wallet=wallet)

    def get_queryset(self):
        # Retourne uniquement les transactions du wallet de l'utilisateur connecté
        wallet = Wallet.objects.get(user=self.request.user)
        return Transaction.objects.filter(wallet=wallet)

# Viewset pour gérer les catégories de Dépenses
class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer

# Viewset pour gérer les catégories de Revenus
class IncomeCategoryViewSet(viewsets.ModelViewSet):
    queryset = IncomeCategory.objects.all()
    serializer_class = IncomeCategorySerializer
