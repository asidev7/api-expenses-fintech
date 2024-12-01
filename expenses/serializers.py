from rest_framework import serializers
from .models import Wallet, Expense, ExpenseCategory, Income, IncomeCategory, Transaction

# Serializer pour les catégories de Dépenses
class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name']

# Serializer pour les Dépenses
class ExpenseSerializer(serializers.ModelSerializer):
    category = ExpenseCategorySerializer()  # Serializer imbriqué pour la catégorie

    class Meta:
        model = Expense
        fields = ['id', 'wallet', 'category', 'description', 'amount', 'date', 'created_at']

# Serializer pour les catégories de Revenus
class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = ['id', 'name']

# Serializer pour les Revenus
class IncomeSerializer(serializers.ModelSerializer):
    category = IncomeCategorySerializer()  # Serializer imbriqué pour la catégorie

    class Meta:
        model = Income
        fields = ['id', 'wallet', 'category', 'description', 'amount', 'date', 'created_at']

# Serializer pour les Transactions
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'description', 'amount', 'transaction_type', 'date', 'created_at']

# Serializer pour les Wallets
class WalletSerializer(serializers.ModelSerializer):
    # Inclure les transactions, dépenses et revenus d'un wallet
    expenses = ExpenseSerializer(many=True, read_only=True, source='expense_set')
    incomes = IncomeSerializer(many=True, read_only=True, source='income_set')
    transactions = TransactionSerializer(many=True, read_only=True, source='transaction_set')

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance', 'expenses', 'incomes', 'transactions', 'created_at']
