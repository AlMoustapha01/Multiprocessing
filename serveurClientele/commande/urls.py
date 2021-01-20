
from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

# importing views from views..py 
from .views import login_view,logout_view ,register_view,commande_view
urlpatterns = [ 
    path('login', login_view), 
    path('logout', logout_view),
    path('register', register_view), 
    path('commandes', commande_view), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
