"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from myapp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

from myapp.views import get_progress, home, logged_home, next_step_panel, previous_step_panel, profile, remove_panel_prod, remove_project_prod, send_panel_prod, send_project_prod, user_files, delete_file, file_explorer_view, download_file_view, panelizer_kicad, user_panels
from myapp.views import open_ticket_panel, gerber_result, gerber_edit, panel_edit

from django.contrib.auth.views import LogoutView

from django.urls import path, include
import django_cas_ng.views

handler500 = 'myapp.views.error_handler'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('gerber-upload/', views.gerber_upload, name='gerber_upload'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logged_home/', logged_home, name='logged_home'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('accounts/login', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('accounts/logout', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),

    path('user-files/', user_files, name='user_files'),
    path('panelizer_kicad/', panelizer_kicad, name='panelizer_kicad'),

    path('delete_file/', delete_file, name='delete_file'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),

    path('view_file/<int:file_id>/<str:file_type>/', views.view_file, name='view_file'),

    path('run_script', views.run_script, name='run_script'),

    path('file-explorer/', file_explorer_view, name='file_explorer'),

    path('download-file/', download_file_view, name='download_file'),

    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/create/', views.create_ticket, name='ticket_create'),
    path('tickets/create/<int:file_id>/', views.create_ticket_from, name='ticket_create'),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/<int:ticket_id>/answer/', views.ticket_answer, name='ticket_answer'),
    path('tickets/<int:ticket_id>/resolve/', views.ticket_resolve, name='ticket_resolve'),

    path('open_ticket/<int:file_id>/', views.open_ticket, name='open_ticket'),
    path('open_ticket_panel/<int:file_id>/', views.open_ticket_panel, name='open_ticket_panel'),
    path('tickets/create_ticket_panel/<int:file_id>/', views.create_ticket_panel, name='create_ticket_panel'),

    path('user-panels/', user_panels, name='user_panels'),

    path('ticket/<int:ticket_id>/delete/', views.ticket_delete, name='ticket_delete'),

    path('gerber_result', views.gerber_result, name='gerber_result'),

    path('gerber_edit/<int:file_id>/', gerber_edit, name='gerber_edit'),
    path('gerber_edit/<int:file_id>/<int:ticket_id>/', gerber_edit, name='gerber_edit'),

    path('panel_edit/<int:file_id>/', panel_edit, name='panel_edit'),
    path('panel_edit/<int:file_id>/<int:ticket_id>/', panel_edit, name='panel_edit'),

    path('get_progress', get_progress, name='get_progress'),

    path('send_project_prod/<int:project_id>/', send_project_prod, name='send_project_prod'),
    path('next_step_panel/<int:panel_id>/', next_step_panel, name='next_step_panel'),

    path('remove_project_prod/<int:project_id>/', remove_project_prod, name='remove_project_prod'),
    path('previous_step_panel/<int:panel_id>/', previous_step_panel, name='previous_step_panel'),

    path('send_panel_prod/<int:panel_id>/', send_panel_prod, name='send_panel_prod'),
    path('remove_panel_prod/<int:panel_id>/', remove_panel_prod, name='remove_panel_prod'),

]
    

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

