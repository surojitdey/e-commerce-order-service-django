from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status, parsers, serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .serializers import OrderSerializer
from .models import Order


class LoginViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    parser_classes = [parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser]

    def get_serializer(self):
      if self.action == 'username':
        return AuthTokenSerializer()
      return serializers.Serializer()
    
    @staticmethod
    def login_user(user):
      if not user.is_active:
        return Response('User deactivated', status=401)

      token, created = Token.objects.get_or_create(user=user)
      return Response({
        'token': token.key,
        'id': user.id
      })

    @action(methods=['POST'], detail=False)
    def username(self, request):
      """
      Expects `username` and `password` fields, returns user `id` and `token`.
      """
      data = request.data.copy()
      if data.get('username'):
        data['username'] = data['username'].lower()
      serializer = AuthTokenSerializer(data=data,
                                        context={'request': request})
      try:
        serializer.is_valid(raise_exception=True)
      except ValidationError as err:
        if 'non_field_errors' in err.detail:
          return Response(status=401)
        raise err

      user = serializer.validated_data['user']
      return self.login_user(user)


class OrderViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def get_serializer(self):
      if getattr(self, 'swagger_fake_view', False):
        return serializers.Serializer()
      return OrderSerializer
    
    def list(self, request):
      orders = Order.objects.all()
      return Response(OrderSerializer(orders, many=True).data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
      order = get_object_or_404(Order, pk=pk)
      serializer = OrderSerializer(order)
      return Response(serializer.data)
    
    def create(self, request):
      self.serializer = self.get_serializer()
      data = request.data.copy()
      serializer = self.serializer(data=data,
                                        context={'request': request})
      try:
        serializer.is_valid(raise_exception=True)
      except ValidationError as err:
        if 'non_field_errors' in err.detail:
          return Response(status=401)
        raise err
      order = serializer.save()
      return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    
    @action(methods=['PUT'], detail=True)
    def update_status(self, request, pk=None):
      order = get_object_or_404(Order, pk=pk)
      if request.data.get("status") in Order.Status:
        order.status = request.data.get("status")
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
      else:
        return Response(
          {
            "message": "Invalid status"
          },
          status=status.HTTP_400_BAD_REQUEST
        )
