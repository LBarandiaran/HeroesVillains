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

@api_view(['GET'])
def super_detail(request, pk):
    try:
        result = Super.objects.get(pk=pk)
        serializer = SuperSerializer(result);
        return Response(serializer.data)

    except Super.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND);
