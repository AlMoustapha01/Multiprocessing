
from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

# importing views from views..py 
from .views import login_view,logout_view ,register_view,stocks_view, ArticleView,ArticleViewById
urlpatterns = [ 
    path('login', login_view), 
    path('logout', logout_view),
    path('register', register_view), 
    path('stocks', stocks_view), 
    path('api/articles/',ArticleView.as_view(),name='Articles'),
    path('api/articles/<str:id>/',ArticleViewById.as_view(),name='Article_by_id'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
