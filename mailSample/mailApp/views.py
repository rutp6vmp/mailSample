from django.shortcuts import render

# Create your views here.
import uuid
import qrcode
import base64
from io import BytesIO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Mail, Feedback
from .serializers import MailSerializer, FeedbackSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Mail, Feedback
from .serializers import MailSerializer, FeedbackSerializer
class SendInfoView(APIView):
    @swagger_auto_schema(
        operation_description="提交郵件信息並生成二維碼",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "ifAnonymous": openapi.Schema(type=openapi.TYPE_INTEGER, description="是否匿名 (0: 匿名, 1: 不匿名)"),
                "text": openapi.Schema(type=openapi.TYPE_STRING, description="投遞內容"),
                "userName": openapi.Schema(type=openapi.TYPE_STRING, description="提問者用戶名 (不匿名時必填)", nullable=True),
                "urlBefore": openapi.Schema(type=openapi.TYPE_STRING, description="前端跳轉地址"),
                "QRWidth": openapi.Schema(type=openapi.TYPE_INTEGER, description="二維碼寬度 (默認 300)", nullable=True),
                "QRHeight": openapi.Schema(type=openapi.TYPE_INTEGER, description="二維碼高度 (默認 300)", nullable=True),
            },
            required=["ifAnonymous", "text", "urlBefore"],
        ),
        responses={
            201: openapi.Response(
                description="成功",
                examples={
                    "application/json": {
                        "code": "0000",
                        "msg": "好了，本喵收到了，退下吧！",
                        "uuid": "2C633273FF694399A24304DCF38DC336",
                        "url": "http://www.baidu.com/?uuid=2C633273FF694399A24304DCF38DC336",
                        "base64": "二維碼的Base64數據"
                    }
                },
            ),
            400: "錯誤的請求參數",
        },
    )
    def post(self, request):
        data = request.data
        if 'ifAnonymous' not in data:
            return Response({"code": "0002", "msg": "你是社牛還是社恐（指ifAnonymous不能為空）"}, status=status.HTTP_400_BAD_REQUEST)
        if data['ifAnonymous'] == 1 and 'userName' not in data:
            return Response({"code": "0003", "msg": "你是社牛還不告訴我你叫什麼名字,八嘎!"}, status=status.HTTP_400_BAD_REQUEST)
        if not data.get('text'):
            return Response({"code": "0001", "msg": "Xiber你倒是說句話啊(指使用者上傳的text不能為空)"}, status=status.HTTP_400_BAD_REQUEST)

        # 創建消息
        mail = Mail.objects.create(
            if_anonymous=data['ifAnonymous'],
            text=data['text'],
            user_name=data.get('userName'),
            url_before=data['urlBefore'],
            qr_width=data.get('QRWidth', 300),
            qr_height=data.get('QRHeight', 300),
            uuid=uuid.uuid4()
        )

        # 生成二維碼
        qr_data = f"{data['urlBefore']}?uuid={mail.uuid}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode()

        return Response({
            "code": "0000",
            "msg": "好了，本喵收到了，退下吧！",
            "uuid": str(mail.uuid),
            "url": qr_data,
            "base64": qr_base64
        }, status=status.HTTP_201_CREATED)

class GetMsgView(APIView):
    @swagger_auto_schema(
        operation_description="根據 UUID 獲取主播回信",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "uuid": openapi.Schema(type=openapi.TYPE_STRING, description="提交接口返回的唯一識別碼"),
            },
            required=["uuid"],
        ),
        responses={
            200: openapi.Response(
                description="成功",
                examples={
                    "application/json": {
                        "code": "0000",
                        "msg": "本喵回复了，请拿好哦！",
                        "data": {
                            "answer": "回答內容",
                            "answerTime": "2025-01-16 17:38:28",
                            "createTime": "2025-01-16 17:38:44",
                            "liveTime": "2025-01-16 17:38:31",
                            "isAnswer": 1,
                            "ifAnonymous": 0,
                            "question": "提問內容",
                            "url": "http://www.baidu.com/?uuid=FE3ACC13D80F46EC9FA4AE02A0CFD4B3",
                            "userName": "Dobe",
                            "uuid": "FE3ACC13D80F46EC9FA4AE02A0CFD4B3"
                        }
                    }
                },
            ),
            404: "找不到 UUID",
        },
    )
    def post(self, request):
        data = request.data
        uuid_value = data.get('uuid')
        if not uuid_value:
            return Response({"code": "0006", "msg": "uuid不能為空"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            mail = Mail.objects.get(uuid=uuid_value)
            feedback = Feedback.objects.get(mail=mail)
            feedback_data = FeedbackSerializer(feedback).data
            return Response({"code": "0000", "msg": "本喵回覆了，請拿好哦！", "data": feedback_data})
        except Mail.DoesNotExist:
            return Response({"code": "0007", "msg": "本喵沒有找到你的提問"}, status=status.HTTP_404_NOT_FOUND)
        except Feedback.DoesNotExist:
            return Response({"code": "0007", "msg": "本喵還沒有回覆你的問題"}, status=status.HTTP_404_NOT_FOUND)
