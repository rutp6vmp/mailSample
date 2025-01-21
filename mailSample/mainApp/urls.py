from django.urls import path

from .views import index,form_submit_view,get_reply_view

urlpatterns = [
    path('', index, name='index'),  # 設置首頁路由
    path('submit-form/', form_submit_view, name='submit_form'),
    path("get-reply/<uuid:uuid>/", get_reply_view, name="get_reply"),
]
