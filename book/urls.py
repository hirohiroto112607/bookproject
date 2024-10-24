from django.urls import path
from . import views

urlpatterns = [
    path("",views.index_view,name="index"),##func
    path("book/",views.ListBookView.as_view(),name="list-book"),##class
    path("book/detail/<int:pk>/", views.DetailBookView.as_view(),name="detail-book"),##class
    path("book/create/", views.CreateBookView.as_view(),name="create-book"),##class
    path("book/<int:pk>/delete/",views.DeleteBookView.as_view(),name="delete-book"),##class
    path("book/<int:pk>/update/",views.UpdateBookView.as_view(),name="update-book"),##class
    ##path("logout",views.logout_view,name="logout")##func
    path("book/<int:book_id>/review/",views.CreateReviewView.as_view(),name="review-book"),
              ]