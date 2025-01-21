from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from mailApp.models import Mail
import uuid
import qrcode
import base64
from io import BytesIO

def index(request):
    return render(request, "mainApp/index.html")


def form_submit_view(request):
    if request.method == "POST":
        if_anonymous = request.POST.get("ifAnonymous")
        text = request.POST.get("text")
        user_name = request.POST.get("userName") if if_anonymous == "1" else None

        if not text:
            return render(request, "mainApp/form.html", {"error": "訊息內容不能為空"})

        # 生成 UUID 並構建回覆查詢的 URL
        unique_id = uuid.uuid4()
        reply_url = request.build_absolute_uri(reverse("get_reply", args=[unique_id]))

        # 保存至數據庫
        mail = Mail.objects.create(
            if_anonymous=if_anonymous,
            text=text,
            user_name=user_name,
            uuid=unique_id,
        )

        # 生成二維碼
        box_size = int(request.POST.get("qr_size", 10))  # 默认值为 10
        border = int(request.POST.get("qr_border", 5))  # 默认值为 5

        qr = qrcode.QRCode(version=1, box_size=box_size, border=border)

        
        qr.add_data(reply_url)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode()

        return render(
            request,
            "mainApp/form.html",
            {
                "success": "訊息已成功提交！",
                "uuid": unique_id,
                "qr_url": reply_url,
                "qr_base64": qr_base64,
            },
        )

    return render(request, "mainApp/form.html")


def get_reply_view(request, uuid):
    mail = get_object_or_404(Mail, uuid=uuid)
    return render(request, "mainApp/reply.html", {"mail": mail})
