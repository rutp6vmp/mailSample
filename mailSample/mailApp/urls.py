from django.urls import path
from .views import SendInfoView, GetMsgView

urlpatterns = [
    path('sendInfo', SendInfoView.as_view(), name='send_info'),
    path('GetMsg', GetMsgView.as_view(), name='get_msg'),
]
