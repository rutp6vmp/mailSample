"""
URL configuration for mailSample project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Dobe Mail API",
        default_version="v1",
        description="Dobe Mail API 文檔說明",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include('mainApp.urls')),  # 包含 mainApp 的路由
    path("admin/", admin.site.urls),
    path('adminApp/', include('adminApp.urls')),  # 包含 adminApp 的路由
    path("dobe-mail/DobeApi/", include("mailApp.urls")),  # 包含 mailApp 的路由
    path('accounts/', include('django.contrib.auth.urls')),  # 登入
    path(
        "swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"
    ),  # Swagger UI
    path(
        "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),  # Redoc UI
]
