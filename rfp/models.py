from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
import random

class AuthConfig(models.Model):
    """
    Single-row config for authentication behavior.
    Edit from Django admin.
    """
    enable_vendor_2fa = models.BooleanField(default=True)
    otp_expiry_minutes = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1)])
    otp_channel = models.CharField(
        max_length=10,
        choices=[("email", "Email")],
        default="email"
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Auth Config"

    @staticmethod
    def get_solo():
        obj = AuthConfig.objects.first()
        if not obj:
            obj = AuthConfig.objects.create()
        return obj


class LoginOTP(models.Model):
    """
    Stores OTP for vendor login.
    """
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} OTP"

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    name = models.CharField(max_length=255, unique=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    def __str__(self):
        return self.name


class Vendor(TimeStampedModel):
    class ApprovalStatus(models.TextChoices):
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        PENDING = "pending", "Pending"   # ✅ better for real flow

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)

    email = models.EmailField(max_length=255, unique=True)
    contact = models.CharField(max_length=10, unique=True)

    # ✅ NEW FIELDS (as per your vendor signup screen)
    revenue_last_3_years_lakhs = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0)]
    )
    employees_count = models.PositiveIntegerField(null=True, blank=True)

    gst_no = models.CharField(max_length=30, null=True, blank=True)
    pan_no = models.CharField(max_length=20, null=True, blank=True)

    # ✅ Vendor chooses category during registration
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="vendors"
    )

    status = models.CharField(
        max_length=10, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING
    )

    def __str__(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full or self.email


class RFP(TimeStampedModel):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="rfps")
    title = models.CharField(max_length=255)

    last_date = models.DateField()

    min_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)

    assigned_vendors = models.ManyToManyField(Vendor, related_name="assigned_rfps", blank=True)

    def is_expired(self):
        return self.last_date < timezone.now().date()

    def __str__(self):
        return f"{self.title} ({self.category.name})"


class Quote(TimeStampedModel):
    rfp = models.ForeignKey(RFP, on_delete=models.CASCADE, related_name="quotes")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="quotes")

    total_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["rfp", "vendor"], name="unique_quote_per_vendor_rfp")
        ]

    def recalc_total(self):
        total = sum((item.line_total for item in self.items.all()), start=0)
        self.total_cost = total

    def __str__(self):
        return f"Quote: {self.vendor} -> {self.rfp}"


class QuoteItem(TimeStampedModel):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="items")
    item_name = models.CharField(max_length=255)

    vendor_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    line_total = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.line_total = (self.vendor_price or 0) * (self.quantity or 0)
        super().save(*args, **kwargs)

        self.quote.recalc_total()
        Quote.objects.filter(pk=self.quote.pk).update(total_cost=self.quote.total_cost)

    def __str__(self):
        return f"{self.item_name} x{self.quantity}"