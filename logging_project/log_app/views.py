from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PersonSerializer
from .models import Person
import logging
import datetime
from django.shortcuts import get_object_or_404

logger = logging.getLogger("loggers")


class PersonAPI(APIView):

    def get(self, request):
        objs = Person.objects.all()
        serializer = PersonSerializer(objs, many=True)
        logger.warning(f'get method was called {datetime.datetime.now()}')
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            logger.info(f"Person saved with id {obj.pk} {datetime.datetime.now()}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f'Person data not valid {datetime.datetime.now()}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PersonDetailAPI(APIView):

    def get(self, request, pk):
        obj = get_object_or_404(Person, pk=pk)
        serializer = PersonSerializer(obj)
        logger.info(f'get method was called of userid {obj.pk} {datetime.datetime.now()}')
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        obj = get_object_or_404(Person, pk=pk)
        serializer = PersonSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.warning(f"Person updated with id {obj.pk} {datetime.datetime.now()}")
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        logger.error(f'Person data not valid {datetime.datetime.now()}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        obj = get_object_or_404(Person, pk=pk)
        serializer = PersonSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.warning(f"Person updated with id {obj.pk} {datetime.datetime.now()}")
            return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
        logger.error(f'Person data not valid {datetime.datetime.now()}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        obj = get_object_or_404(Person, pk=pk)
        logger.warning(f'User {obj.id} has been deleted')
        obj.delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)