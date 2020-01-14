from .views import (
    CreateNoteAPIView,
    ListNoteAPIView,
    DetailNoteAPIView,
    DeleteNoteAPIView,
    DetailAndDeleteNoteAPIView,
    CreateLabelAPIView,
    RetrieveUpdateNoteAPIView
)
from django.urls import path

urlpatterns = [
    path('create-note', CreateNoteAPIView.as_view(), name='create-note'),
    path('create-label', CreateLabelAPIView.as_view(), name='label-note'),
    path('list/', ListNoteAPIView.as_view(), name='list-note'),
    path('get/<int:pk>', DetailNoteAPIView.as_view(), name='get-note'),
    path('delete/<int:pk>', DeleteNoteAPIView.as_view(), name='delete-note'),
    path('delete-get/<int:pk>', DetailAndDeleteNoteAPIView.as_view(),
         name='get-delete-note'),
    path('update/<int:pk>', RetrieveUpdateNoteAPIView.as_view(), name='note-update'),

]
