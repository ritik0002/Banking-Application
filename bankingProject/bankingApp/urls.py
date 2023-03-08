from django.urls import path
from . import views

urlpatterns = [
    path('api/test/', views.transaction_api, name="bank_api"),
        #User API paths
    # path('api/users/', views.users_api, name="users"),
    # path('api/users/<int:userID>/', views.user_api, name="user"),
    path('api/sessionUser/', views.sessionUser, name="sessionUser"),
    
    
    #Login,register,logout
    path("login/", views.login_view, name="login"),
    path("", views.login_view, name="home"),
    path('register/', views.register, name="register"),
    path("logout/",views.logout_view,name="logout")

]