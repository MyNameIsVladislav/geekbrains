from django.urls import path

from accounts import views


app_name = 'auth'

urlpatterns = [
               path("login/", views.login_view, name="login"),
               path('logout/', views.logout, name='logout'),
               path('register/', views.register, name='register'),
               path('verify/<str:email>/<str:activation_key>', views.verify, name='verify'),
               path('edit/user/', views.edit_user, name='edit'),
               path('edit/profile/', views.edit_profile, name='profile'),
               path('valid_pass', views.valid_password, name='valid_password')
    ]
