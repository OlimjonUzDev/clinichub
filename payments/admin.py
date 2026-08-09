from django.contrib import admin

from .models import Payment, PaymentTransaction


class PaymentTransactionInline(admin.TabularInline):
    """PaymentTransaction yozuvlarini Payment admin sahifasida jadval ko'rinishida ko'rsatadi."""

    model = PaymentTransaction
    extra = 0
    readonly_fields = ['raw_data', 'created_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Payment (to'lov) modeli uchun admin panel sozlamalari."""

    list_display = ['id', 'patient', 'provider', 'amount', 'currency', 'status', 'created_at', 'paid_at']
    list_filter = ['provider', 'status', 'created_at']
    search_fields = ['patient__name_uz', 'transaction_id']
    readonly_fields = ['transaction_id', 'paid_at', 'created_at']
    inlines = [PaymentTransactionInline]


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    """PaymentTransaction (to'lov tizimidan kelgan webhook logi) modeli uchun admin panel sozlamalari."""

    list_display = ['id', 'payment', 'created_at']
    readonly_fields = ['raw_data', 'created_at']
