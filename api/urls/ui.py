from django.urls import path
from ..views import (admin_logout_view, lead_create_view, lead_delete_view, lead_detail_view,
                     lead_list_view, lead_update_view, role_delete_view, rolecost_list_view,
                     role_list_view, role_create_view, role_detail_view, role_update_view,
                     rolecost_update_view, rolecost_create_view, rolecost_delete_view, rolecost_detail_view,
                     location_update_view, location_list_view, location_create_view, location_delete_view,
                     report_item_update, report_history_create, report_history_delete, report_history_detail,
                     report_item_create, report_item_delete, report_item_detail, otp_list_view,
                     rolecost_bulk_upload_view, location_detail_view, report_history_list, pending_request_list_view,
                     )

urlpatterns = [
    path("custom-admin/logout/", admin_logout_view, name="admin-logout"),

    path("roles/", role_list_view, name="role-list"),
    path("roles/create/", role_create_view, name="role-create"),
    path("roles/<int:pk>/", role_detail_view, name="role-detail"),
    path("roles/<int:pk>/edit/", role_update_view, name="role-update"),
    path("roles/<int:pk>/delete/", role_delete_view, name="role-delete"),


    path("locations/", location_list_view, name="location-list"),
    path("locations/create/", location_create_view, name="location-create"),
    path("locations/<int:pk>/", location_detail_view, name="location-detail"),
    path("locations/<int:pk>/edit/", location_update_view, name="location-update"),
    path("locations/<int:pk>/delete/",
         location_delete_view, name="location-delete"),


    path("rolecosts/", rolecost_list_view, name="rolecost-list"),
    path("rolecosts/add/", rolecost_create_view, name="rolecost-create"),
    path("rolecosts/<int:pk>/", rolecost_detail_view, name="rolecost-detail"),
    path("rolecosts/<int:pk>/edit/", rolecost_update_view, name="rolecost-update"),
    path("rolecosts/<int:pk>/delete/",
         rolecost_delete_view, name="rolecost-delete"),
    path("rolecosts/bulk-upload/",
         rolecost_bulk_upload_view, name="rolecost-bulkupload"),


    path("leads/", lead_list_view, name="lead-list"),
    path("leads/create/", lead_create_view, name="lead-create"),
    path("leads/<int:pk>/edit/", lead_update_view, name="lead-update"),
    path("leads/<int:pk>/delete/", lead_delete_view, name="lead-delete"),
    path("leads/<int:pk>/", lead_detail_view, name="lead-detail"),


    path("reports/", report_history_list, name="reporthistory-list"),
    path("reports/create/", report_history_create,
         name="reporthistory-create"),
    path("reports/<int:pk>/", report_history_detail,
         name="reporthistory-detail"),
    path("reports/<int:pk>/delete/", report_history_delete,
         name="reporthistory-delete"),


    path("reports/<int:report_history_id>/items/create/",
         report_item_create, name="reportitem-create"),
    path("reports/<int:report_history_id>/items/<int:pk>/",
         report_item_detail, name="reportitem-detail"),
    path("reports/<int:report_history_id>/items/<int:pk>/edit/",
         report_item_update, name="reportitem-update"),
    path("reports/<int:report_history_id>/items/<int:pk>/delete/",
         report_item_delete, name="reportitem-delete"),


    path("pending-requests/", pending_request_list_view,
         name="pending-requests-list"),

    path("otp/", otp_list_view, name="otp-list"),
]
