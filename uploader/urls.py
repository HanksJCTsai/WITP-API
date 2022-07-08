from django.urls import path

from . import views

app_name = "uploader"

urlpatterns = [
    path("", views.index, name="index"),
    path("getBudnBudLnId", views.getBudIdnBudLnId, name="getBudIdnBudLnId"),
    path("create_user", views.create_user, name="create user"),
    path("copyBud2PRF", views.copyBud2PRF, name="copy Budget project to PRF"),
    path("uploadPRFByExcel", views.uploadPRFByExcel, name="upload to PRF"),
    path("copyPRF2IB", views.copyPRF2IB, name="copy PRF to IB"),
    #path("generatePRFPDF", views.generate_PRF_PDF, name="generate PRF's PDF document")
    path("getCheckingReport",views.getCheckingReport, name ="Get Checking Report")
]
