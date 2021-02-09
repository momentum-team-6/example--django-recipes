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
    ingredients = IngredientSerializer(many=True, required=False)

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
            'image',
        )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients_data:
            recipe.ingredients.create(amount=ingredient['amount'],
                                      item=ingredient['item'])

        return recipe
