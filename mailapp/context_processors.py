from .models import UserRegistration, Message, BlockList, Feedback ,Drafts

def admin_dashboard_data(request):
    total_users = UserRegistration.objects.count()
    total_mails = Message.objects.count()
    phishing_count = Message.objects.filter(prediction_result=1).count()
    blocked_count = BlockList.objects.count()
    feedback_count = Feedback.objects.count()
    approved_users = UserRegistration.objects.filter(loginid__is_active=1).count()
    pending_users = UserRegistration.objects.filter(loginid__is_active=0).count()

    admin_name = "Admin"
    admin_role = "SUPERUSER"

    if request.user.is_authenticated:
        admin_name = request.user.username
        admin_role = getattr(request.user, "userType", "ADMIN").upper()

    recent_messages = Message.objects.order_by('-id')[:5]
    recent_blocks = BlockList.objects.order_by('-id')[:5]
    recent_feedbacks = Feedback.objects.order_by('-id')[:5]
    
    # ⚠️ IMPORTANT: check type of prediction_result (string or int)
    phishing_detected = Message.objects.filter(prediction_result=1).count()
    # if needed:
    # phishing_detected = Message.objects.filter(prediction_result="1").count()

    return {
        "admin_name": admin_name,
        "admin_role": admin_role,
        "total_users": total_users,
        "total_mails": total_mails,
        "phishing_count": phishing_count,
        "blocked_count": blocked_count,
        "feedback_count": feedback_count,
        "recent_messages": recent_messages,
        "recent_blocks": recent_blocks,
        "recent_feedbacks": recent_feedbacks,
        "system_status": "SYSTEM OPERATIONAL",
        "system_version": "ENGINE v3.1.0 · MODEL BUILD 2026.03",
        "approved_users": approved_users,
        "pending_users": pending_users,
        "phishing_detected": phishing_detected,
    }
    
def user_dashboard_data(request):
    uid = request.session.get("uid")

    if not uid:
        return {}

    try:
        user = UserRegistration.objects.get(loginid=uid)

        inbox_count = Message.objects.filter(sendto=user.email).count()
        draft_count = Drafts.objects.filter(fromMail=user, status="Draft").count()
        blocked_count = BlockList.objects.filter(blocking_user_id=user.email).count()
        feedback_count = Feedback.objects.filter(uid=user).count()

        return {
            "current_user": user,
            "user_name": user.name,
            "user_email": user.email,
            "user_image": user.image,
            "user_role": "USER",
            "inbox_count": inbox_count,
            "draft_count": draft_count,
            "blocked_user_count": blocked_count,
            "user_feedback_count": feedback_count,
        }
    except UserRegistration.DoesNotExist:
        return {}