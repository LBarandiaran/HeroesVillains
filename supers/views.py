from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SuperSerializer
from .models import Super
from supers import serializers


@api_view(['GET', 'POST'])
def supers_list(request):
    if request.method == 'GET':

        hero_type = request.query_params.get('super_type')
        print(hero_type)

        supers = Super.objects.all()
        
        if hero_type:
            supers = supers.filter(hero_type=hero_type)

        serializer = SuperSerializer(supers, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SuperSerializer(data=request.data)
        if serializer.is_valid() == True:
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT'])
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

