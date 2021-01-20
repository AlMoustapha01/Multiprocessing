
from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

# importing views from views..py 
from .views import OrdreView,OrdreViewById,verification_banque
urlpatterns = [ 
    path('api/verification', verification_banque),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
