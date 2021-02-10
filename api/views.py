from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from recipes.models import Ingredient, Recipe, User
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.generics import (CreateAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     get_object_or_404)
from rest_framework.pagination import PageNumberPagination

from api.serializers import (IngredientCreateSerializer, IngredientSerializer,
                             RecipeSerializer)


class RecipeListCreateView(ListCreateAPIView):
    serializer_class = RecipeSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

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
        recipe = serializer.validated_data['recipe']
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


class RecipesForUserView(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        queryset = user.recipes.filter(public=True)
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = RecipeSerializer(page,
                                      many=True,
                                      context={'request': request})
        return paginator.get_paginated_response(serializer.data)
