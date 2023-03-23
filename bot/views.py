from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializer import BotVerificationSerializer
from bot.tg.client import TgClient


class VerificationView(GenericAPIView):
    model = TgUser
    permission_classes = [IsAuthenticated]
    serializer_class = BotVerificationSerializer

    def patch(self, request: Request, *args, **kwargs) -> Response:
        s: BotVerificationSerializer = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)

        s.tg_user.user = request.user
        s.tg_user.save()

        TgClient().send_message(s.tg_user.chat_id, "Verifictaion have completed")
        TgClient().send_message(s.tg_user.chat_id, "Enter command with '/' in the end")

        return Response(self.get_serializer(s.tg_user).data)
