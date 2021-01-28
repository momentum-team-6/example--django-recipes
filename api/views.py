from rest_framework.exceptions import PermissionDenied
from recipes.models import Ingredient, Recipe
from rest_framework.generics import (CreateAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from api.serializers import (IngredientCreateSerializer, IngredientSerializer,
                             RecipeSerializer)


class RecipeListCreateView(ListCreateAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return Recipe.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecipeDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return Recipe.objects.for_user(self.request.user)

        return self.request.user.recipes


class IngredientCreateView(CreateAPIView):
    serializer_class = IngredientCreateSerializer
    queryset = Ingredient.objects.all()

    def perform_create(self, serializer):
        recipe = Recipe.objects.get(pk=serializer.data['recipe'])
        if self.request.user != recipe.user:
            raise PermissionDenied(
                detail="You are not the owner of this recipe.")
        serializer.save()


class IngredientDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        # TODO need to filter down and make sure users can't update or delete
        # ingredients on recipes that don't belong to them
        return Ingredient.objects.filter(recipe__user=self.request.user)
