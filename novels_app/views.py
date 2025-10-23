from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Category, Novel
from .serializers import NovelDetailSerializer, CategoryWithNovelSerializer


class CategoryWithNovelsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Category.objects.prefetch_related('novels__episodes').all()
    serializer_class=CategoryWithNovelSerializer



@api_view(['GET'])
def search_novels(request):
    query = request.GET.get('q', '')
    if not query:
        return Response({"error": "Please provide a search query ?q="}, status=400)

    novels = Novel.objects.filter(title__icontains=query) | Novel.objects.filter(about__icontains=query)
    serializer = NovelDetailSerializer(novels, many=True, context={'request': request})
    return Response(serializer.data)