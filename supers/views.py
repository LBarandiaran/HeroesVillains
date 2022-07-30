from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SuperSerializer
from .models import Super
from supers import serializers


@api_view(['GET', 'POST'])
def supers_list(request):
    if request.method == 'GET':
        supers = Super.objects.all()
        heroes = supers.filter(super_type__type="Hero")
        villains = supers.filter(super_type__type="Villain")
        heroes_serialized = SuperSerializer(heroes,many=True)
        villains_serialized = SuperSerializer(villains,many=True)

        if request.query_params.get('type') == 'hero':
            custom_response = heroes_serialized.data
        elif request.query_params.get('type') == 'villain':
            custom_response = villains_serialized.data
        else:
            custom_response = {
                'heroes': heroes_serialized.data,
                'villians': villains_serialized.data
            }
               
        return Response(custom_response)
    elif request.method == 'POST':
        serializer = SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
   

@api_view(['GET', 'PUT', 'DELETE'])
def super_detail(request, pk):
    result = get_object_or_404(Super, pk=pk)
    if request.method == 'GET':
        serializer = SuperSerializer(result);
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SuperSerializer(result, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
