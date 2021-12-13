from django.urls import path

from authapp import views


app_name = 'authapp'

urlpatterns = [
               path("login/", views.LoginNewView.as_view(), name="login"),
               path('logout/', views.logout, name='logout'),
               path('register/', views.register, name='register'),
               path('verify/<str:email>/<str:activation_key>', views.verify, name='verify'),
               path('edit/user/', views.edit_user, name='edit'),
               path('edit/profile/', views.edit_profile, name='profile'),
    ]
