from django.urls import path
from .views import register, EventView, TicketPurchaseView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('register/', register, name='register'),
    path('events/', EventView.as_view(), name='events'),
    path('events/<int:id>/purchase/', TicketPurchaseView.as_view(), name='purchase'),
    path('login/',obtain_auth_token,name='login'),
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('refresh/',TokenRefreshView.as_view(),name='token_refresh')
]  