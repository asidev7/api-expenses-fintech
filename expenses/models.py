from django.db import models
from django.contrib.auth.models import User

# Modèle pour gérer le Wallet d'un utilisateur
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet - Balance: {self.balance}"

# Modèle pour gérer les Transactions dans le wallet (dépenses et revenus)
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('EXPENSE', 'Dépense'),
        ('INCOME', 'Revenu'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount}"

    def save(self, *args, **kwargs):
        # Met à jour le solde du wallet lors de l'ajout d'une transaction
        if self.pk is None:
            if self.transaction_type == 'INCOME':
                self.wallet.balance += self.amount
            elif self.transaction_type == 'EXPENSE':
                self.wallet.balance -= self.amount
            self.wallet.save()
        super().save(*args, **kwargs)

# Modèle pour les catégories de Dépenses
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Modèle pour gérer les Dépenses avec des catégories
class Expense(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"

    def save(self, *args, **kwargs):
        # Déduit le montant de la dépense du solde du wallet
        if self.pk is None:
            self.wallet.balance -= self.amount
            self.wallet.save()
        super().save(*args, **kwargs)

# Modèle pour les catégories de Revenu
class IncomeCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Modèle pour gérer les Revenus avec des catégories
class Income(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    category = models.ForeignKey(IncomeCategory, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"

    def save(self, *args, **kwargs):
        # Ajoute le montant du revenu au solde du wallet
        if self.pk is None:
            self.wallet.balance += self.amount
            self.wallet.save()
        super().save(*args, **kwargs)
