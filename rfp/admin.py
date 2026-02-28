from django.contrib import admin
from .models import Category, Vendor, RFP, Quote, QuoteItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("name",)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "contact", "status")
    list_filter = ("status","first_name")
    search_fields = ("first_name", "last_name", "email", "contact")
    actions = ["approve_vendors", "reject_vendors"]

    @admin.action(description="Approve selected vendors")
    def approve_vendors(self, request, queryset):
        queryset.update(status="approved")

    @admin.action(description="Reject selected vendors")
    def reject_vendors(self, request, queryset):
        queryset.update(status="rejected")


class QuoteInline(admin.TabularInline):
    model = Quote
    extra = 0


@admin.register(RFP)
class RFPAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "last_date", "status", "created_at")
    list_filter = ("status", "category")
    search_fields = ("title",)
    filter_horizontal = ("assigned_vendors",)  # M2M selection in admin


class QuoteItemInline(admin.TabularInline):
    model = QuoteItem
    extra = 0


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("id", "rfp", "vendor", "total_cost", "created_at")
    list_filter = ("rfp", "vendor")
    inlines = [QuoteItemInline]


@admin.register(QuoteItem)
class QuoteItemAdmin(admin.ModelAdmin):
    list_display = ("id", "quote", "item_name", "vendor_price", "quantity", "line_total", "created_at")
    list_filter = ("quote__rfp", "quote__vendor")
    search_fields = ("item_name",)