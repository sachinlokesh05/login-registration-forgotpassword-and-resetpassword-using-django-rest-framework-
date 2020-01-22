from django.shortcuts import render
from .models import Note, Label
from .serializer import NoteSerializer, LabelSerializer
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from rest_framework.generics import GenericAPIView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .permissions import IsOwnerOrReadOnly
from rest_framework import generics
from django.utils.decorators import method_decorator
from rest_framework import permissions, authentication
from .decorator import login_decorator, super_user_only, superuser_only, timeit, user_can_write_a_review
# Create your views here.


@method_decorator(superuser_only, name='dispatch')
class CreateNoteAPIView(generics.CreateAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()


@method_decorator(login_decorator, name='dispatch')
class NoteCreate(GenericAPIView):
    """
        Summary:
        --------
            Note class will let authorized user to create and get notes.
        Methods:
        --------
            get: User will get all the notes.
            post: User will able to create new note.
    """
    serializer_class = NoteSerializer

    def get(self, request):
        """
           Summary:
           --------
                All the notes will be fetched for the user.
           Exception:
           ----------
               PageNotAnInteger: object
               EmptyPage: object
           Returns:
           --------
               Html_page: pagination.html    Jinja-arg=['notes']
        """
        notes_list = Note.objects.all()
        page = request.GET.get('page')
        paginator = Paginator(notes_list, 1)
        user = request.user
        try:
            notes = paginator.page(page)
        except PageNotAnInteger:
            notes = paginator.page(1)
        except EmptyPage:
            notes = paginator.page(paginator.num_pages)
        return render(request, 'pagination.html', {'notes': notes}, status=200)

    # parser_classes = (FormParser,FileUploadParser)
    @staticmethod
    def post(request):
        """
             Summary:
             --------
                 New note will be create by the User.
             Exception:
             ----------
                 KeyError: object
             Returns:
             --------
                 response: SMD format of note create message or with error message
        """

        user = request.user
        try:
            # data is taken from user
            # pdb.set_trace()
            data = request.data
            if len(data) == 0:
                raise KeyError
            user = request.user
            # empty coll  list is formed where data is input is converted to id
            collaborator_list = []
            try:
                # for loop is used for the getting label input and coll input ids
                data["label"] = [Label.objects.filter(user_id=user.id, name=name).values()[0]['id'] for name in
                                 data["label"]]
            except KeyError:
                pass
            try:
                collaborator = data['collaborators']
                # for loop is used for the getting label input and coll input ids
                for email in collaborator:
                    email_id = User.objects.filter(email=email)
                    user_id = email_id.values()[0]['id']
                    collaborator_list.append(user_id)
                data['collaborators'] = collaborator_list
                print(data['collaborators'])
            except KeyError:
                pass
            serializer = NotesSerializer(data=data, partial=True)
            if serializer.is_valid():
                note_create = serializer.save(user_id=user.id)
                response = {'success': True,
                            'message': "note created", 'data': []}
                if serializer.data['is_archive']:
                    cache.hmset(str(user.id) + "is_archive",
                                {note_create.id: str(json.dumps(serializer.data))})  # created note is cached in redis

                    return HttpResponse(json.dumps(response, indent=2), status=201)
                else:
                    if serializer.data['reminder']:
                        cache.hmset("reminder",
                                    {note_create.id: str(json.dumps({"email": user.email, "user": str(user),
                                                                     "note_id": note_create.id,
                                                                     "reminder": serializer.data["reminder"]}))})
                    cache.hmset(str(user.id) + "note",
                                {note_create.id: str(json.dumps(serializer.data))})

                    return HttpResponse(json.dumps(response, indent=2), status=201)
            response = {'success': False,
                        'message': "note was not created", 'data': []}
            return HttpResponse(json.dumps(response, indent=2), status=400)
        except KeyError as e:
            print(e)

            response = {'success': False,
                        'message': "one of the field is empty ", 'data': []}
            return Response(response, status=400)
        except Exception as e:
            print(e)

            response = {'success': False,
                        'message': "something went wrong", 'data': []}
            return Response(response, status=400)


class CreateLabelAPIView(generics.CreateAPIView):
    serializer_class = LabelSerializer
    queryset = Label.objects.all()


@method_decorator(timeit, name='dispatch')
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


@method_decorator(user_can_write_a_review, name='dispatch')
class RetrieveUpdateNoteAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
