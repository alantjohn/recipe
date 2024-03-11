from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets
from recipe.serializers import RecipeSerializer,ReviewSerializer,UserSerializer
from recipe.models import Recipe
from recipe.models import RatingAndReview
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,mixins,generics,viewsets

# Create your views here.

class RecipeList(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class Reviewrating(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = RatingAndReview.objects.all()
    serializer_class = ReviewSerializer

class CreateUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class search(APIView):
    def get(self,request):
        query=self.request.query_params.get('search')
        if (query):
            recipe=Recipe.objects.filter(Q(name__icontains=query) | Q(ingredients__icontains=query))
            serialized_recipe=RecipeSerializer(recipe,many=True)
            return Response(serialized_recipe.data)
        else:
            return Response([])

class Recipedetails(APIView):
    def get_object(self,request,pk):
        try:
            return Recipe.objects.get(pk=pk)
        except:
            raise Http404

    def get(self,request,pk):
        recipe=self.get_object(request,pk)
        s = RecipeSerializer(recipe)
        return Response(s.data)

    def delete(self,request,pk):
        recipe = self.get_object(request, pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
