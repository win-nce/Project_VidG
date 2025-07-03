from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.GameListView.as_view(), name='index'),
    path('catalogue/', views.CatalogueView.as_view(), name='catalogue'),
    path('search/', views.search, name='search'),

    path('studios/', views.StudioListView.as_view(), name='studio_list'),
    path('studio/<int:pk>/', views.StudioDetailView.as_view(), name='studio_detail'),

    path('game/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),

    #Рег/Лог/Выход
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # Добавление реакции
    path('game/<int:game_id>/react/', views.add_reaction, name='add_reaction'),

    # Ревью links
    path('game/<int:game_id>/review/add/', views.ReviewCreateView.as_view(), name='add_review'),
    path('review/<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='edit_review'),
    path('review/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='delete_review'),

    # Создание жалобы
    path('game/<int:game_id>/report/', views.create_report, name='create_report'),

    # Профиль юзера
    path('profile/', views.ProfileView.as_view(), name='profile'),
]

# ничего не выводилось изначально...
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)