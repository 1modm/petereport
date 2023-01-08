from django.conf.urls import include
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    # Auth
    path('accounts/', include('django.contrib.auth.urls')),
    # Configuration
    path('configuration/users/', views.user_list, name='user_list'),
    path('configuration/user/add', views.user_add, name='user_add'),
    path('configuration/user/edit/<int:pk>', views.user_edit, name='user_edit'),
    path('configuration/user/delete/', views.user_delete, name='user_delete'),
    # Settings
    path('configuration/settings/', views.settings, name='settings'),
    # Customers
    path('customer/list/', views.customer_list, name='customer_list'),
    path('customer/add/', views.customer_add, name='customer_add'),
    path('customer/edit/<int:pk>', views.customer_edit, name='customer_edit'),
    path('customer/delete/', views.customer_delete, name='customer_delete'),
    path('customer/view/<int:pk>', views.customer_view, name='customer_view'),
    # Products
    path('product/list/', views.product_list, name='product_list'),
    path('product/add/', views.product_add, name='product_add'),
    path('product/edit/<int:pk>', views.product_edit, name='product_edit'),
    path('product/delete/', views.product_delete, name='product_delete'),
    path('product/view/<int:pk>', views.product_view, name='product_view'),
    # Reports
    path('report/list/', views.report_list, name='report_list'),
    path('report/add/', views.report_add, name='report_add'),
    path('report/view/<int:pk>', views.report_view, name='report_view'),
    path('report/edit/<int:pk>', views.report_edit, name='report_edit'),
    path('report/delete/', views.report_delete, name='report_delete'),
    path('report/duplicate/', views.report_duplicate, name='report_duplicate'),
    path('report/uploadsummaryfindings/<int:pk>', views.uploadsummaryfindings, name='uploadsummaryfindings'), # prepend a language code in ajax
    path('report/download/markdown/<int:pk>', views.reportdownloadmarkdown, name='reportdownloadmarkdown'),
    path('report/download/html/<int:pk>', views.reportdownloadhtml, name='reportdownloadhtml'),
    path('report/download/pdf/<int:pk>', views.reportdownloadpdf, name='reportdownloadpdf'),
    path('report/download/jupyter/<int:pk>', views.reportdownloadjupyter, name='reportdownloadjupyter'),
    # Findings
    path('report/findings/<int:pk>', views.reportfindings, name='reportfindings'),
    path('finding/add/<int:pk>', views.finding_add, name='finding_add'),
    path('finding/edit/<int:pk>', views.finding_edit, name='finding_edit'),
    path('finding/delete/', views.finding_delete, name='finding_delete'),
    path('finding/view/<int:pk>', views.finding_view, name='finding_view'),
    path('finding/open/', views.openfindings, name='openfindings'),
    path('finding/closed/', views.closedfindings, name='closedfindings'),
    path('finding/csv/<int:pk>', views.downloadfindingscsv, name='downloadfindingscsv'),
    path('findings/upload/<int:pk>', views.upload_csv_findings, name='upload_csv_findings'),
    path('findings/defectdojo/products/<int:pk>', views.defectdojo_products, name='defectdojo_products'),
    path('findings/defectdojo/import/<int:pk>/<int:ddpk>', views.defectdojo_import, name='defectdojo_import'),
    # Custom Fields
    path('field/add/<int:pk>', views.field_add, name='field_add'),
    path('finding/customfields/<int:pk>', views.fields, name='fields'),
    path('field/delete/', views.field_delete, name='field_delete'),
    path('field/edit/<int:pk>', views.field_edit, name='field_edit'),
    # Appendix
    path('report/appendix/<int:pk>', views.reportappendix, name='reportappendix'),
    path('appendix/add/<int:pk>', views.appendix_add, name='appendix_add'),
    path('appendix/view/<int:pk>', views.appendix_view, name='appendix_view'),
    path('appendix/delete/', views.appendix_delete, name='appendix_delete'),
    path('appendix/edit/<int:pk>', views.appendix_edit, name='appendix_edit'),
    # Templates
    path('template/list/', views.template_list, name='template_list'),
    path('template/add/', views.template_add, name='template_add'),
    path('template/add/finding/<int:pk>', views.templateaddfinding, name='templateaddfinding'),
    path('template/add/report/<int:pk>/<int:reportpk>', views.templateaddreport, name='templateaddreport'),
    path('template/view/<int:pk>', views.template_view, name='template_view'),
    path('template/delete/', views.template_delete, name='template_delete'),
    path('template/edit/<int:pk>', views.template_edit, name='template_edit'),
    # CWE
    path('cwe/list/', views.cwe_list, name='cwe_list'),
    path('cwe/add/', views.cwe_add, name='cwe_add'),
    path('cwe/edit/<int:pk>', views.cwe_edit, name='cwe_edit'),
    path('cwe/delete/', views.cwe_delete, name='cwe_delete'),
    # Attack Flows
    path('report/attackflow/<int:pk>', views.reportattackflow, name='reportattackflow'),
    path('attackflow/add/<int:pk>', views.attackflow_add, name='attackflow_add'),
    path('attackflow/add_flow/<int:pk>/<int:finding_pk>', views.attackflow_add_flow, name='attackflow_add_flow'),
    path('attackflow/edit/<int:pk>', views.attackflow_edit_flow, name='attackflow_edit_flow'),
    path('attackflow/add_afb/<int:pk>/<int:finding_pk>', views.attackflow_add_afb, name='attackflow_add_afb'),
    path('attackflow/edit_afb/<int:pk>', views.attackflow_edit_afb, name='attackflow_edit_afb'),
    path('attackflow/delete/', views.attackflow_delete, name='attackflow_delete'),
]
