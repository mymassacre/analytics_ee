from django.urls import path
from . import views

urlpatterns = [
    path("", views.PaginatedListView.as_view(), name="view_data_index"),
    path("<int:page>/", views.PaginatedListView.as_view(), name="view_data_index_page"),
]
