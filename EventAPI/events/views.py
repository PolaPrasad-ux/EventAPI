from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import User, Event, Ticket
from .serializers import UserSerializer, EventSerializer, TicketSerializer
from django.core.exceptions import ValidationError

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    role = request.data.get('role')

    if not username or not password or not role:
        return Response({'error': 'Username, password, and role are required'}, status=400)

    if role not in ['Admin', 'User']:
        return Response({'error': 'Invalid role'}, status=400)

    try:
        User.objects.create_user(username=username, password=password, role=role)
        return Response({'message': f'{role} user registered successfully'}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


class EventView(APIView):
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != 'Admin':
            return Response({'error': 'Only admins can create events'}, status=status.HTTP_403_FORBIDDEN)
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketPurchaseView(APIView):
    def post(self,request,id):
        """
        Handles ticket purchase requests for a given event.
        """
        user = request.user  # Assumes user authentication is in place
        quantity = request.data.get('quantity')

        # Validate input: Ensure quantity is provided and is a positive integer
        if not isinstance(quantity, int) or quantity <= 0:
            return Response(
                {"error": "Invalid quantity. Must be a positive integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Retrieve the event by ID
            event = Event.objects.get(id=id)

            # Attempt to purchase tickets
            event.purchase_tickets(user=user, quantity=quantity)

            return Response(
                {"message": "Tickets purchased successfully!"},
                status=status.HTTP_201_CREATED
            )

        except Event.DoesNotExist:
            return Response(
                {"error": "Event not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
