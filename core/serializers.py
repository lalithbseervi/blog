from rest_framework import serializers
from .models import BlogPost, Category

choices = {
    True: 'true',
    False: 'false'
}

class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class BlogPostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=255)
    body = serializers.CharField(style={'base_template': 'textarea.html'})
    created_on = serializers.DateTimeField()
    last_modified = serializers.DateTimeField()
    share_token = serializers.UUIDField(format='hex_verbose')
    password_protect = serializers.BooleanField(default=False, choices=choices)
    require_table_of_contents = serializers.BooleanField(default=False, choices=choices)
    slug = serializers.SlugField(max_length=255)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance