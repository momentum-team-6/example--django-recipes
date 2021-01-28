from recipes.models import Ingredient, Recipe
from rest_framework import serializers


class IngredientCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('url', 'recipe', 'amount', 'item')


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('url', 'amount', 'item')


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    tags = serializers.SlugRelatedField(many=True,
                                        read_only=True,
                                        slug_field='tag')
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'url',
            'user',
            'title',
            'prep_time_in_minutes',
            'cook_time_in_minutes',
            'tags',
            'ingredients',
            'public',
        )
