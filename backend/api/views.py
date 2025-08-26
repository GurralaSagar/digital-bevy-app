import os
import requests
from urllib.parse import quote_plus
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from django.db import IntegrityError

from .models import Repository
from .serializers import RepositorySerializer

GITHUB_SEARCH_URL = 'https://api.github.com/search/repositories'

def github_headers():
    token = os.getenv('GITHUB_TOKEN')
    headers = {'Accept': 'application/vnd.github+json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return headers

@api_view(['POST'])
def search_and_store(request):
    """Fetch repos by keyword from GitHub and store to DB.
    Body: { keyword: str, page?: int, per_page?: int }
    """
    keyword = (request.data.get('keyword') or '').strip()
    if not keyword:
        return Response({'error': "'keyword' is required"}, status=status.HTTP_400_BAD_REQUEST)

    page = int(request.data.get('page', 1))
    per_page = min(int(request.data.get('per_page', 10)), 50)

    params = {
        'q': quote_plus(keyword),
        'page': page,
        'per_page': per_page,
        'sort': 'stars',
        'order': 'desc',
    }

    try:
        r = requests.get(GITHUB_SEARCH_URL, params=params, headers=github_headers(), timeout=20)
        if r.status_code == 403:
            return Response(
                {'error': 'GitHub rate limit hit. Add GITHUB_TOKEN to .env or retry later.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        r.raise_for_status()
        items = r.json().get('items', [])

        created, skipped = 0, 0
        stored = []
        for it in items:
            data = {
                'keyword': keyword,
                'name': it.get('name'),
                'full_name': it.get('full_name'),
                'url': it.get('html_url'),
                'description': it.get('description'),
                'language': it.get('language'),
                'stars': it.get('stargazers_count', 0),
                'owner': (it.get('owner') or {}).get('login'),
            }
            try:
                obj = Repository.objects.create(**data)
                created += 1
                stored.append(obj)
            except IntegrityError:
                skipped += 1
        return Response(
            {
                'created': created,
                'skipped': skipped,
                'stored_sample': RepositorySerializer(stored, many=True).data,
            },
            status=status.HTTP_201_CREATED,
        )
    except requests.RequestException as e:
        return Response({'error': f'Upstream API error: {e}'}, status=status.HTTP_502_BAD_GATEWAY)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RepoListView(ListAPIView):
    serializer_class = RepositorySerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['stars', 'created_at', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Repository.objects.all()
        keyword = self.request.query_params.get('keyword')
        if keyword:
            qs = qs.filter(keyword__icontains=keyword)
        lang = self.request.query_params.get('language')
        if lang:
            qs = qs.filter(language__iexact=lang)
        return qs
