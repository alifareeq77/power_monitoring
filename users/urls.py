from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users import views

urlpatterns = [
                  path('', views.home, name='home'),
                  path('register/', views.register, name='register'),
                  path('login/', views.user_login, name='login'),
                  path('logout/', views.user_logout, name='logout'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
