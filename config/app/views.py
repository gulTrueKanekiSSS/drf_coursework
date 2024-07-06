from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Habits
from .serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnly


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Habits.objects.filter(user=self.request.user)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habits.objects.filter(is_public=True)
