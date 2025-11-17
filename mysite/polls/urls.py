from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:question_id>/choice_create/", views.choice_create, name="choice_create"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
