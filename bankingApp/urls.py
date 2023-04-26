from django.urls import path
from . import views

urlpatterns = [
    path('api/transaction/filter/<int:userID>/', views.transaction_filter_api, name="bank_filter_api"),

    path('api/transaction/<int:userID>/', views.transaction_api, name="transaction_api"),
    path('api/transactions/<int:TransactionId>/', views.current_transaction_api),

        #User API paths
    path('api/users/', views.user_api,),
    path('api/user/<int:userID>/', views.users_api, name="user"),
    path('api/sessionUser/', views.sessionUser, name="sessionUser"),
    path('api/superUser/',views.superUser),
    path('api/deleteUser/',views.deleteUser),
    #password reset
    path('api/password/',views.password),
    
    #support ticket
    path('api/support/',views.support,name="support"),
    #Calculator
    path('api/Calculator/', views.Calculator,name="Calculator"),
    
    #Login,register,logout,home
    path("login/", views.login_view, name="login"),
    path("", views.home, name="home"),
    # path("home/",views.)
    path('register/', views.register, name="register"),
    path("logout/",views.logout_view,name="logout")

]
