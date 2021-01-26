from recipes.models import Recipe
from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    tags = serializers.SlugRelatedField(many=True,
                                        read_only=True,
                                        slug_field='tag')

    class Meta:
        model = Recipe
        fields = (
            'pk',
            'user',
            'title',
            'prep_time_in_minutes',
            'cook_time_in_minutes',
            'tags',
            'public',
        )
