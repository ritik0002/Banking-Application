from django.urls import path
from . import views

urlpatterns = [
    path('api/transaction/filter/<int:userID>/', views.transaction_filter_api, name="bank_filter_api"),

    path('api/transaction/<int:userID>/', views.transaction_api, name="bank_api"),
    path('api/transactions/<int:TransactionId>/', views.current_transaction_api),

        #User API paths
    path('api/users/', views.user_api,),
    path('api/user/<int:userID>/', views.users_api, name="user"),
    path('api/sessionUser/', views.sessionUser, name="sessionUser"),
    
    
    #Login,register,logout
    path("login/", views.login_view, name="login"),
    path("", views.login_view, name="home"),
    path('register/', views.register, name="register"),
    path("logout/",views.logout_view,name="logout")

]
