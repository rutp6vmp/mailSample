from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from mailApp.models import Mail, Feedback

# 僅允許超級管理員訪問
def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def message_list(request):
    """
    訊息列表，帶有篩選與分頁功能。
    """
    # 篩選條件
    status_filter = request.GET.get('status')
    messages = Mail.objects.select_related('feedback').all()
    if status_filter:
        messages = messages.filter(feedback__is_answered=status_filter)

    # 分頁處理，每頁顯示 10 條
    paginator = Paginator(messages, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'adminApp/message_list.html', {'messages': page_obj})

@login_required
@user_passes_test(is_admin)
def respond_message(request, uuid):
    """
    處理單條訊息的回應。
    """
    message = get_object_or_404(Mail, uuid=uuid)
    feedback = Feedback.objects.filter(mail=message).first()

    if request.method == 'POST':
        answer = request.POST.get('answer')
        if feedback:
            feedback.answer = answer
            feedback.is_answered = 1  # 標記為已回答
            feedback.save()
        else:
            Feedback.objects.create(
                mail=message,
                answer=answer,
                is_answered=1
            )
        return redirect('message_list')

    return render(request, 'adminApp/respond_message.html', {'message': message, 'feedback': feedback})
