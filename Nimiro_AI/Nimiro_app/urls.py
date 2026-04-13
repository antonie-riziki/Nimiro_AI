from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.landing_page, name='landing-page'),
    path('auth/', views.auth_page, name='auth-page'),
    path('dashboard/', views.dashboard_page, name='dashboard-page'),
    path('farming_guide/', views.farming_guide, name='farming-guide'),
    path('market_intelligence/', views.market_intelligence, name='market-intelligence'),
    path('profile_page/', views.profile_page, name='profile-page'),
    path('landmap/', views.landmap, name='landmap-page'),
    path('analysis/', views.analysis_page, name='analysis-page'),
    path('credit_score/', views.credit_score, name='credit-score'),
    path('crop_calendar/', views.crop_calendar, name='crop-calendar'),
    path('reels/', views.reels, name='reels'),
    path('chatbot-response/', views.chatbot_response, name='chatbot-response')

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)