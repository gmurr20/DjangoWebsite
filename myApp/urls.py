from django.conf.urls import url
import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^photos/', views.photos, name="photos"),
    url(r'^articles/', views.blogPage, name="blogPage"),
    url(r'^ajax/search/', views.blogSearch, name="blogSearch"),
    url(r'^blogArticle/', views.blogArticle, name="blogArticle"),
    url(r'^basketball/', views.basketball, name="basketball"),
    url(r'^ajax/runScript/', views.runScript, name="runScript")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)