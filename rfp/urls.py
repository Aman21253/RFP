from django.urls import path
from . import views

urlpatterns = [
    # ---------- AUTH ----------
    path("", views.login_view, name="login"),
    path("vendor/verify-otp/", views.vendor_verify_otp, name="vendor_verify_otp"),
    path("vendor/resend-otp/", views.vendor_resend_otp, name="vendor_resend_otp"),
    path("logout/", views.logout_view, name="logout"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/", views.reset_password, name="reset_password"),

    path("signup/admin/", views.admin_signup, name="admin_signup"),
    path("signup/vendor/", views.vendor_signup, name="vendor_signup"),

    # ---------- DASHBOARDS ----------
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("vendor/dashboard/", views.vendor_dashboard, name="vendor_dashboard"),

    # ---------- ADMIN PANEL ----------
    path("panel/categories/", views.admin_categories, name="admin_categories"),
    path("panel/categories/create/", views.admin_category_create, name="admin_category_create"),
    path("panel/categories/toggle/<int:pk>/", views.admin_category_toggle, name="admin_category_toggle"),

    path("panel/vendors/", views.admin_vendors, name="admin_vendors"),
    path("panel/vendors/toggle/<int:pk>/", views.admin_vendor_toggle, name="admin_vendor_toggle"),

    path("panel/rfp/", views.admin_rfp_list, name="admin_rfp_list"),
    path("panel/rfp/select-category/", views.admin_rfp_select_category, name="admin_rfp_select_category"),
    path("panel/rfp/add/<int:category_id>/", views.admin_rfp_add, name="admin_rfp_add"),
    path("panel/rfp/toggle/<int:pk>/", views.admin_rfp_toggle, name="admin_rfp_toggle"),

    path("panel/quotes/", views.admin_quotes, name="admin_quotes"),

    # ---------- VENDOR PANEL ----------
    path("vendor/rfps/", views.vendor_rfp_list, name="vendor_rfp_list"),
    path("vendor/rfp/<int:pk>/", views.vendor_rfp_detail, name="vendor_rfp_detail"),

    path("vendor/quotes/", views.vendor_quote_list, name="vendor_quote_list"),
    path("vendor/quote/create/<int:rfp_id>/", views.vendor_quote_create, name="vendor_quote_create"),
    path("vendor/quote/submit/<int:rfp_id>/", views.vendor_quote_submit, name="vendor_quote_submit"),

    path("vendor/rfp-for-quotes/", views.vendor_rfp_for_quotes, name="vendor_rfp_for_quotes"),
    path("vendor/rfp/<int:rfp_id>/apply/", views.vendor_apply_rfp, name="vendor_apply_rfp"),

    path("panel/categories/export/", views.export_categories_excel, name="export_categories_excel"),
    path("panel/vendors/export/", views.export_vendors_excel, name="export_vendors_excel"),
    path("panel/rfp/export/", views.export_rfp_excel, name="export_rfp_excel"),
]