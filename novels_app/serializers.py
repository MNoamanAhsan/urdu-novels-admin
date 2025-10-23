from rest_framework import serializers
from .models import Category, Novel, Episode


class EpisodeSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Episode
        fields = ['id', 'episode_number', 'title', 'file_url']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
    

class NovelDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    episodes = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Novel
        fields = ['id', 'title', 'author','about', 'summary', 'cover_image', 'category_name', 'episodes']




class CategoryWithNovelSerializer(serializers.ModelSerializer):
    novels=NovelDetailSerializer(many=True, read_only=True)

    class Meta:
        model=Category
        fields=['id', 'name', 'novels']