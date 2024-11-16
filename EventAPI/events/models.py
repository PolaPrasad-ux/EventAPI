from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import transaction

class UserManager(BaseUserManager):
    def create_user(self, username, password, role):
        if not username:
            raise ValueError("Users must have a username")

        is_staff = role == 'Admin'
        is_superuser = role == 'Admin'

        user = self.model(
            username=username,
            role=role,
            is_staff=is_staff,
            is_superuser=is_superuser
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

  

class User(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        ADMIN = 'Admin', _('Admin')
        USER = 'User', _('User')

    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=5, choices=Roles.choices)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    # Permissions-related methods
    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return self.is_superuser

class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    total_tickets = models.IntegerField()
    tickets_sold = models.IntegerField(default=0)

    def purchase_tickets(self, user, quantity):
        """
        Handles ticket purchase logic:
        - Checks if requested quantity exceeds available tickets.
        - Updates tickets_sold and creates a Ticket entry if valid.
        """
        # Validate quantity
        if quantity <= 0:
            raise ValidationError(_("Ticket quantity must be greater than zero."))
        
        # Check availability
        if self.tickets_sold + quantity > self.total_tickets:
            available = self.total_tickets - self.tickets_sold
            raise ValidationError(
                _(f"Only {available} tickets are available for this event.")
            )

        # Perform atomic transaction for consistency
        with transaction.atomic():
            # Update tickets_sold
            self.tickets_sold += quantity
            self.save()

            # Create a Ticket entry
            Ticket.objects.create(user=user, event=self, quantity=quantity)
    def __str__(self):
        return f"{self.name}"

class Ticket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.event.name} Ticket {self.id}"