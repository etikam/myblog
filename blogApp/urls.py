from django.urls import path
from .views import (ArticleListCreateView, 
                    ArticleDeleteView, 
                    ArticleUpdateView,
                    ArticleCreateView,
                    ArticleDetailView,
                    CommentDeleteView,
                    CommentUpdateView,
                    )
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', ArticleListCreateView.as_view(), name="home"),
    path('deleteArticle/<int:pk>/', ArticleDeleteView.as_view(), name='del-article'),
    path('deleteComment/<int:pk>/', CommentDeleteView.as_view(), name='del-comment'),
    path('editArticle/<int:pk>/', ArticleUpdateView.as_view(), name='edit-article'),
    path('editComment/<int:pk>/', CommentUpdateView.as_view(), name='edit-comment'),
    path('create-article/', ArticleCreateView.as_view(), name='article-create'),
    path('detail-article/<int:pk>/',ArticleDetailView.as_view(),name="detail-article"),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
