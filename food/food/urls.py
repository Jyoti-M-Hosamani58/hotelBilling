"""food URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from food_app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('index1',views.index1,name='index1'),

    path('admin_home',views.admin_home,name='admin_home'),
    path('admin_nav',views.admin_nav,name='admin_nav'),
    path('register',views.register,name='register'),
    path('register_list',views.register_list,name='register_list'),
    path('delete_register/<int:pk>', views.delete_register, name='delete_register'),

    path('login',views.login,name='login'),
    path('user_login/', views.user_login, name='user_login'),
    path('admin_login/', views.admin_login, name='admin_login'),

    path('add_item',views.add_item,name='add_item'),
    path('view_item', views.view_item, name='view_item'),
    path('edit_item/<int:pk>', views.edit_item, name='edit_item'),
    path('delete_item/<int:pk>', views.delete_item, name='delete_item'),

    path('add_table', views.add_table, name='add_table'),
    path('view_table', views.view_table, name='view_table'),
    path('edit_table/<int:pk>', views.edit_table, name='edit_table'),
    path('delete_table/<int:pk>', views.delete_table, name='delete_table'),

    path('add_company', views.add_company, name='add_company'),
    path('view_company', views.view_company, name='view_company'),
    path('edit_company/<int:pk>', views.edit_company, name='edit_company'),
    path('delete_company/<int:pk>', views.delete_company, name='delete_company'),

    path('add_order',views.add_order,name='add_order'),
    path('fetch_table_data/', views.fetch_table_data, name='fetch_table_data'),
    path('item/<str:item_code>/', views.fetch_item_details, name='fetch_item_details'),
    path('save_order',views.save_order,name='save_order'),

    path('exchange_tbl',views.exchange_tbl,name='exchange_tbl'),
    path('print_table',views.print_table,name='print_table'),
    path('print_bill/',views.print_bill,name='print_bill'),

    path('settle_table', views.settle_table, name='settle_table'),
    path('settle_bill/', views.settle_bill, name='settle_bill'),

    path('userHome', views.userHome, name='userHome'),
    path('add_order_user',views.add_order_user,name='add_order_user'),
    path('save_order_user',views.save_order_user,name='save_order_user'),
    path('parcel',views.parcel,name='parcel'),
    path('save_pracel_user',views.save_pracel_user,name='save_pracel_user'),
    path('print_pracel/<int:bill_no>/', views.print_pracel, name='print_pracel'),

    path('delete_print_bill/<int:bill_no>/', views.print_bill_delete, name='print_bill_delete'),
    path('settle_bill_delete/<int:bill_no>/', views.settle_bill_delete, name='settle_bill_delete'),
    path('settle_bill_delete_user/<int:bill_no>/', views.settle_bill_delete_user, name='settle_bill_delete_user'),


    path('sales_report',views.sales_report,name='sales_report'),
    path('item_report',views.item_report,name='item_report'),
    path('daily_report',views.daily_report,name='daily_report'),

    path('exchange_tbl_user',views.exchange_tbl_user,name='exchange_tbl_user'),
    path('print_table_user',views.print_table_user,name='print_table_user'),
    path('print_bill_user/',views.print_bill_user,name='print_bill_user'),

    path('settle_table_user', views.settle_table_user, name='settle_table_user'),
    path('settle_bill_user/', views.settle_bill_user, name='settle_bill_user'),

    path('checkTablesUser', views.checkTablesUser, name='checkTablesUser'),
    path('checkItemsUser/', views.checkItemsUser, name='checkItemsUser'),

    path('checkTables', views.checkTables, name='checkTables'),
    path('checkItems/', views.checkItems, name='checkItems'),

    path('addExpenses', views.addExpenses, name='addExpenses'),
    path('saveExpenses', views.saveExpenses, name='saveExpenses'),
    path('viewExpenses', views.viewExpenses, name='viewExpenses'),

    path('get_staff_name', views.get_staff_name, name='get_staff_name'),
    path('salary', views.salary, name='salary'),
    path('saveSalary', views.saveSalary, name='saveSalary'),
    path('viewSalary', views.viewSalary, name='viewSalary'),

    path('profit_report', views.profit_report, name='profit_report'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)