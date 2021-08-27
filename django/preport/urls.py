from django.conf.urls import include, url
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
    path('configuration/user/delete/<int:pk>', views.user_delete, name='user_delete'),
    # Products
    path('product/list/', views.product_list, name='product_list'),
    path('product/add/', views.product_add, name='product_add'),
    path('product/edit/<int:pk>', views.product_edit, name='product_edit'),
    path('product/delete/<int:pk>', views.product_delete, name='product_delete'),
    path('product/view/<int:pk>', views.product_view, name='product_view'),
    # Reports
    path('report/add/', views.report_add, name='report_add'),
    path('report/view/<int:pk>', views.report_view, name='report_view'),
    path('report/edit/<int:pk>', views.report_edit, name='report_edit'),
    path('report/delete/<int:pk>', views.report_delete, name='report_delete'),
    path('report/uploadsummaryfindings/<int:pk>', views.uploadsummaryfindings, name='uploadsummaryfindings'),
    path('report/download/markdown/<int:pk>', views.reportdownloadmarkdown, name='reportdownloadmarkdown'),
    path('report/download/html/<int:pk>', views.reportdownloadhtml, name='reportdownloadhtml'),
    path('report/download/pdf/<int:pk>', views.reportdownloadpdf, name='reportdownloadpdf'),
    # Findings
    path('report/findings/<int:pk>', views.reportfindings, name='reportfindings'),
    path('finding/add/<int:pk>', views.finding_add, name='finding_add'),
    path('finding/edit/<int:pk>', views.finding_edit, name='finding_edit'),
    path('finding/delete/<int:pk>', views.finding_delete, name='finding_delete'),
    path('finding/view/<int:pk>', views.finding_view, name='finding_view'),
    path('finding/open/', views.openfindings, name='openfindings'),
    path('finding/closed/', views.closedfindings, name='closedfindings'),
    path('finding/csv/<int:pk>', views.downloadfindingscsv, name='downloadfindingscsv'),
    path('findings/upload/<int:pk>', views.upload_csv_findings, name='upload_csv_findings'),
    # Appendix
    path('report/appendix/<int:pk>', views.reportappendix, name='reportappendix'),
    path('appendix/add/<int:pk>', views.appendix_add, name='appendix_add'),
    path('appendix/view/<int:pk>', views.appendix_view, name='appendix_view'),
    path('appendix/delete/<int:pk>', views.appendix_delete, name='appendix_delete'),
    path('appendix/edit/<int:pk>', views.appendix_edit, name='appendix_edit'),
    # Templates
    path('template/list/', views.template_list, name='template_list'),
    path('template/add/', views.template_add, name='template_add'),
    path('template/add/finding/<int:pk>', views.templateaddfinding, name='templateaddfinding'),
    path('template/add/report/<int:pk>/<int:reportpk>', views.templateaddreport, name='templateaddreport'),
    path('template/view/<int:pk>', views.template_view, name='template_view'),
    path('template/delete/<int:pk>', views.template_delete, name='template_delete'),
    path('template/edit/<int:pk>', views.template_edit, name='template_edit'),
    # CWE
    path('cwe/list/', views.cwe_list, name='cwe_list'),
]
