from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from .models import User , Product , Ticket ,BuyTicket


@admin.register(User)
class UserAdmin(BaseAdmin):
    model = User
    list_display = (
        "first_name",
        "last_name",
        "phone_number",
        "is_verified",
        "ip_address",
        "register_time",)
    
    readonly_fields = ("ip_address","register_time")
    list_display_links = ("first_name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "kind",
        "status",
        "ounce",
        "quality",
        "price",
        "show_inventory",
        "inventory",
        "min_order",
        "max_order",
        "free_shipping",
        "shipping_cost",
        "is_pestina_product",
        "is_confirmed",
        "ip_address",
        "upload_time",)
    readonly_fields = ("ip_address","upload_time")
        
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("ticket_id",
                    "user",
                    "ticket_type",
                    "request_title",
                    "request_discription",
                    "ticket_time",
                    "ip_address",)
    readonly_fields = ("ticket_id","ticket_time","ip_address")

@admin.register(BuyTicket)
class BuyTicketAdmin(admin.ModelAdmin):
    list_display = ("ticket_id",
                    "buyer_namelastname",
                    "buyer_phone",
                    "pistachio",
                    "gain_product",
                    "order_discription",
                    "calculated_price",
                    "ticket_time",
                    "ip_address")
    readonly_fields = ("ticket_id","ticket_time","ip_address")




# EehsaNn8404