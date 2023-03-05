from django.contrib import admin
from django.urls import path

from importer.views import ingest_applicant_info_module, ingest_full_payload

urlpatterns = [
    path('admin/', admin.site.urls),
    path('import/applicant_info', ingest_applicant_info_module),
    path('import/full_payload', ingest_full_payload),
]
