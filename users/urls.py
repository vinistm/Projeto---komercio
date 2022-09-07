from django.urls import path

from users.views import ListCreateUserView,LoginView,ListNewestUserView,UpdateUserStatusView,UpdateUserDetailsView
urlpatterns = [
    path('accounts/', ListCreateUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('accounts/newest/<int:num>/', ListNewestUserView.as_view()),
    path('accounts/<pk>/', UpdateUserDetailsView.as_view()),
    path('accounts/<pk>/management/', UpdateUserStatusView.as_view())
]