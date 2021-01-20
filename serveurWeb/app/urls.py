
from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

# importing views from views..py 
from .views import shop_view,detail_view,panier_view,commande_view,login_view,register_view,logout_view,UserView,UserViewById, PanierView,PanierViewById,CommandeView,CommandeViewById
urlpatterns = [ 
    path('shop', shop_view),
    path('login', login_view), 
    path('logout', logout_view),
    path('register', register_view),
    path('detail/<int:id>',detail_view),
    path('commande',commande_view),
    path('panier',panier_view),
    path('api/paniers/',PanierView.as_view(),name='Paniers'),
    path('api/paniers/<str:id>/',PanierViewById.as_view(),name='Panier_by_id'),
    path('api/commandes/',CommandeView.as_view(),name='Commandes'),
    path('api/commandes/<str:id>/',CommandeViewById.as_view(),name='Commande_by_id'),
    path('api/users/',UserView.as_view(),name='users'),
    path('api/users/<str:id>/',UserViewById.as_view(),name='user_by_id'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
