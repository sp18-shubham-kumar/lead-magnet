from .admin_dashboard import AdminDashboardView
from .admin_login import AdminLoginView
from .admin_logout import admin_logout_view
from .home import HomeView
from .otp import otp_list_view, OTPlistView
from .report_history import (report_history_create, report_history_delete, 
                             report_history_detail, report_history_list,
                             ReportHistoryDetailView, ReportHistoryListCreateView)
from .report_item import (report_item_create, report_item_delete, 
                          report_item_detail, report_item_update,
                          ReportItemDetailView, ReportItemListCreateView)
from .available_roles import AvailableRolesView
from .calculate import CalculateReportView
from .pending_request import PendingRequestListCreateView, pending_request_list_view
from .lead import (lead_create_view, lead_delete_view, 
                   lead_detail_view, lead_list_view, lead_update_view,
                   LeadDetailView, LeadListCreateView)
from .location import (location_create_view, location_delete_view, 
                       location_detail_view, location_list_view, location_update_view,
                       LocationDetailView, LocationListCreateView, LocationBulkUploadView)
from .role import (role_create_view, role_delete_view, 
                   role_detail_view, role_list_view, role_update_view,
                   RoleDetailView, RoleListCreateView, RoleBulkUploadView)
from .rolecost import (rolecost_create_view, rolecost_delete_view, 
                       rolecost_detail_view, rolecost_list_view, rolecost_update_view,
                       RoleCostDetailView, RoleCostListCreateView, rolecost_bulk_upload_view)
from .email import SendOTPView, SendReportView, VerifyOTPView
from .pending_request_otp import PendingSendOTPView, PendingVerifyOTPView
from .prev_reports import PrevReportsView
