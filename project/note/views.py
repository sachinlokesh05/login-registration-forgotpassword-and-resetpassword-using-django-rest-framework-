from django.shortcuts import render
from .models import Note, Label
from .serializer import NoteSerializer, LabelSerializer
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics
from django.utils.decorators import method_decorator
from rest_framework import permissions, authentication
from .decorator import login_decorator
# Create your views here.


# @method_decorator(login_decorator, name='dispatch')
class CreateNoteAPIView(generics.CreateAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()


class CreateLabelAPIView(generics.CreateAPIView):
    serializer_class = LabelSerializer
    queryset = Label.objects.all()


@method_decorator(login_decorator, name='dispatch')
class ListNoteAPIView(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]
    # authentication_classes = [authentication.TokenAuthentication]
    serializer_class = NoteSerializer
    queryset = Note.objects.all()


class DetailNoteAPIView(generics.RetrieveAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()


class DeleteNoteAPIView(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()


class DetailAndDeleteNoteAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()


class RetrieveUpdateNoteAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
