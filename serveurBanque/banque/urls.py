
from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

# importing views from views..py 
from .views import CompteView,CompteViewById
urlpatterns = [ 
    path('api/comptes/',CompteView.as_view(),name='Comptes'),
    path('api/comptes/<str:id>/',CompteViewById.as_view(),name='Compte_by_id'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
