
from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

# importing views from views..py 
from .views import CompteView,CompteViewById,CompteViewByTelephone
urlpatterns = [ 
    path('api/comptes/',CompteView.as_view(),name='Comptes'),
    path('api/comptes/<str:id>/',CompteViewById.as_view(),name='Compte_by_id'),
    path('api/comptes/telephone/<str:telephone>/',CompteViewByTelephone.as_view(),name='Compte_by_telephone'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
