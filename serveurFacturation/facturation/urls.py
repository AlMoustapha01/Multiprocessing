
from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

# importing views from views..py 
from .views import OrdreView,OrdreViewById,verification_banque
urlpatterns = [ 
    path('api/verification/', verification_banque),
    path('api/ordres/',OrdreView.as_view(),name='ordres'),
    path('api/ordres/<str:id>/',OrdreViewById.as_view(),name='ordre_by_id'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
