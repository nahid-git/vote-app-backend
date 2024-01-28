from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from authentication.serializers import EmptySerializer
from options.models import Option
from questions.models import Question
from .models import Event, Vote, VoterSelectedOption
from .serializers import EventsSerializer, SubmitVoteSerializer


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
    permission_classes = [IsAuthenticated]

    # @property
    def get_permissions(self):
        if self.action in ['destroy']:
            self.permission_classes = [IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action in ['submit_vote']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['submit_vote']:
            return SubmitVoteSerializer
        elif self.action in ['list', 'retrive']:
            return EventsSerializer
        return EmptySerializer

    @action(detail=False, methods=['GET'], url_name='my-event')
    def my_event(self, request):
        queryset = Event.objects.filter(accounts=request.user)
        serializer = EventsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_name='submit-vote')
    def submit_vote(self, request, pk=None):
        try:
            event = Event.objects.get(pk=pk)

            if event.expired_at < timezone.now():
                return Response({'non_field_errors': ['Expired event']}, status=status.HTTP_400_BAD_REQUEST)
            # check user is voted
            vote_event = Vote.objects.filter(event=event, account=request.user).first()
            if vote_event is not None:
                return Response({'non_field_errors': ['You have already voted']}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            submitted_options = []
            if request.data['submission'] is not None and len(request.data['submission']) == event.questions.count():

                for item in request.data['submission']:
                    question_instance = Question.objects.filter(pk=item['question'], options=item['answer']).first()
                    if question_instance is None:
                        return Response({'non_field_errors': ['Submitted question or option is invalid!']},
                                        status=status.HTTP_400_BAD_REQUEST)
                    submitted_options.append({'question': item['question'], 'answer': item['answer']})

                event.accounts.add(request.user)

                for item in submitted_options:
                    question = Question.objects.get(pk=item['question'])
                    option = Option.objects.get(pk=item['answer'])

                    VoterSelectedOption.objects.create(
                        vote=event.vote_set.get(account=request.user),
                        question=question,
                        selected_option=option
                    )

                return Response({'message': 'Your vote has been submitted!'}, status=status.HTTP_200_OK)
            else:
                return Response({'non_field_errors': ['Invalid submission']}, status=status.HTTP_400_BAD_REQUEST)

        except Event.DoesNotExist:
            return Response({'non_field_errors': ['Event does not exist.']}, status=status.HTTP_404_NOT_FOUND)
