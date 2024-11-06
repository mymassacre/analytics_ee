from django.urls import path
from . import views

urlpatterns = [
    path("", views.transfer_files_to_model_index, name="transfer_files_to_model_index"),
]
