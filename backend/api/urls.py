from django.urls import path
from .views import search_and_store, RepoListView

urlpatterns = [
    path('search/', search_and_store, name='search_and_store'),
    path('repos/', RepoListView.as_view(), name='repo_list'),
]
