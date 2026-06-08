from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Suv, Mijoz, Haydovchi, Admin, Buyurtma
from .serializers import (
    SuvSerializer, MijozSerializer, HaydovchiSerializer,
    AdminSerializer, BuyurtmaSerializer
)
from .pagination import BuyurtmaPagination


class SuvListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: SuvSerializer(many=True)})
    def get(self, request):
        suvlar = Suv.objects.all()
        serializer = SuvSerializer(suvlar, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=SuvSerializer, responses={201: SuvSerializer})
    def post(self, request):
        serializer = SuvSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SuvDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Suv.objects.get(pk=pk)
        except Suv.DoesNotExist:
            return None

    @swagger_auto_schema(responses={200: SuvSerializer})
    def get(self, request, pk):
        suv = self.get_object(pk)
        if not suv:
            return Response({'xato': 'Topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        return Response(SuvSerializer(suv).data)

    @swagger_auto_schema(request_body=SuvSerializer, responses={200: SuvSerializer})
    def put(self, request, pk):
        suv = self.get_object(pk)
        if not suv:
            return Response({'xato': 'Topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SuvSerializer(suv, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=SuvSerializer, responses={200: SuvSerializer})
    def patch(self, request, pk):
        suv = self.get_object(pk)
        if not suv:
            return Response({'xato': 'Topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        # partial=True - faqat yuborilgan fieldlarni yangilaydi
        serializer = SuvSerializer(suv, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'O\'chirildi'})
    def delete(self, request, pk):
        suv = self.get_object(pk)
        if not suv:
            return Response({'xato': 'Topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        suv.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class MijozListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('qidiruv', openapi.IN_QUERY,
                              description="Ism yoki tel bo'yicha qidirish",
                              type=openapi.TYPE_STRING)
        ],
        responses={200: MijozSerializer(many=True)}
    )
    def get(self, request):
        mijozlar = Mijoz.objects.all()
        # 9-vazifa: ism va tel bo'yicha qidiruv
        qidiruv = request.query_params.get('qidiruv', None)
        if qidiruv:
            mijozlar = mijozlar.filter(
                ism__icontains=qidiruv
            ) | mijozlar.filter(
                tel__icontains=qidiruv
            )
        serializer = MijozSerializer(mijozlar, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=MijozSerializer, responses={201: MijozSerializer})
    def post(self, request):
        serializer = MijozSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MijozDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Mijoz.objects.get(pk=pk)
        except Mijoz.DoesNotExist:
            return None

    @swagger_auto_schema(responses={200: MijozSerializer})
    def get(self, request, pk):
        mijoz = self.get_object(pk)
        if not mijoz:
            return Response({'xato': 'Topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        return Response(MijozSerializer(mijoz).data)

    @swagger_auto_schema(request_body=MijozSerializer, responses={200: MijozSerializer})
    def put(self, request, pk):
        mijoz = self.get_object(pk)
        if not mijoz:
            return Response({'xato': 'Topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MijozSerializer(mijoz, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=MijozSerializer, responses={200: MijozSerializer})
    def patch(self, request, pk):
        mijoz = self.get_object(pk)
        if not mijoz:
            return Response({'xato': 'Topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MijozSerializer(mijoz, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'O\'chirildi'})
    def delete(self, request, pk):
        mijoz = self.get_object(pk)
        if not mijoz:
            return Response({'xato': 'Topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        mijoz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BuyurtmaListCreateView(generics.ListCreateAPIView):

    queryset = Buyurtma.objects.all()
    serializer_class = BuyurtmaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BuyurtmaPagination


    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['suv', 'mijoz']
    ordering_fields = ['sana']
    ordering = ['-sana']


class AdminListView(generics.ListAPIView):

    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated]


class AdminDetailView(generics.RetrieveAPIView):

    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated]


class HaydovchiListView(generics.ListAPIView):
    """Haydovchilar ro'yxati"""
    queryset = Haydovchi.objects.all()
    serializer_class = HaydovchiSerializer
    permission_classes = [IsAuthenticated]


class HaydovchiDetailView(generics.RetrieveAPIView):
    """Bitta haydovchi ma'lumotlari"""
    queryset = Haydovchi.objects.all()
    serializer_class = HaydovchiSerializer
    permission_classes = [IsAuthenticated]
