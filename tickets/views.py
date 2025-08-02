from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, filters
from django.http import JsonResponse
from .models import Movie, Guest, Reservation

from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from rest_framework import generics, mixins, viewsets

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# without REST and no model query
def no_rest_no_model(request):
    guests = [
        {
            "id": 1,
            "name": "John Doe",
            "phone": "1234567890"
        },
    ]
    return JsonResponse(guests, safe=False)


# Without REST and with model query
def no_rest(request):
    data = Guest.objects.all()
    response = {
        "guests": list(data.values('name', 'phone'))
    }
    return JsonResponse(response, safe=False)


# Function Based Views (FBV) using REST framework
@api_view(['GET', 'POST'])
def guests(request):
    # GET
    if request.method == 'GET':
        all_guests = Guest.objects.all()
        serializer = GuestSerializer(all_guests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # POST
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def guests_fbv(request, pk):
    try:
        selected_guest = Guest.objects.get(pk=pk)
        # GET
        if request.method == 'GET':
            serializer = GuestSerializer(selected_guest)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # PUT
        elif request.method == 'PUT':
            serializer = GuestSerializer(data=request.data, instance=selected_guest)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # DELETE
        elif request.method == 'DELETE':
            selected_guest.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Guest.DoesNotExist:
        return Response({"error": "Guest not found"}, status=status.HTTP_404_NOT_FOUND)


class GuestsAPIView(APIView):
    def get(self, request):
        all_guests = Guest.objects.all()
        serializer = GuestSerializer(all_guests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GuestsAPIViewTwo(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            return None

    def get(self, request, pk):
        guest = self.get_object(pk)
        if guest is None:
            return Response({"error": "Guest not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GuestSerializer(guest)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        guest = self.get_object(pk)
        if guest is None:
            return Response({"error": "Guest not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GuestSerializer(data=request.data, instance=guest)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        if guest is None:
            return None
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Class Mixins
# GET and POST methods
class MixinsList(
    mixins.ListModelMixin,  # It will allow us to list all objects
    mixins.CreateModelMixin,  # It will allow us to create new objects
    generics.GenericAPIView  # It will be helpful to return Response objects
):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Guest.objects.all()  # for list and create
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# GET, PUT and DELETE methods
class MixinsListPk(
    mixins.RetrieveModelMixin,  # It will allow us to retrieve a single object by its primary key
    mixins.UpdateModelMixin,  # It will allow us to update an existing object
    mixins.DestroyModelMixin,  # It will allow us to delete an object
    generics.GenericAPIView
):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)

    def put(self, request, pk):
        return self.update(request, pk=pk)

    def delete(self, request, pk):
        return self.destroy(request, pk=pk)


# Generics
class GuestListCreateAPIView(generics.ListCreateAPIView):
    # For listing all guests and creating a new guest
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class GuestRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    # For retrieving, updating, or deleting a guest by primary key
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


# viewsets
class GuestsViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class MoviesViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'hall', 'duration', 'start_time']


class ReservationsViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


@api_view(['GET'])
def find_movie(request):
    selected_filters = Q()
    title = request.query_params.get('title', '').strip()
    hall = request.query_params.get('hall', '').strip()
    duration = request.query_params.get('duration', None)
    start_time = request.query_params.get('start_time', None)

    if title:
        selected_filters |= Q(title__icontains=title)
    if hall:
        selected_filters |= Q(hall__icontains=hall)
    if duration:
        selected_filters |= Q(duration=duration)
    if start_time:
        selected_filters |= Q(start_time=start_time)

    selected_movies = Movie.objects.filter(selected_filters)
    serializer = MovieSerializer(selected_movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_reservation(request):
    title = request.data.get('title', '').strip()
    name = request.data.get('name', '').strip()
    phone = request.data.get('phone', '').strip()
    seats = request.data.get('seats', 1)
    price = request.data.get('price', 0.0)

    # ✅ Check if movie exists
    try:
        selected_movie = Movie.objects.get(title__iexact=title)
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

    # ✅ Check if guest exists, if not create a new one
    try:
        selected_guest = Guest.objects.get(name__iexact=name, phone=phone)
    except Guest.DoesNotExist:
        selected_guest = Guest.objects.create(name=name, phone=phone)

    serializer = ReservationSerializer(
        data={
            'guest': selected_guest.id,
            'movie': selected_movie.id,
            'seats': seats,
            'price': price
        }
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
