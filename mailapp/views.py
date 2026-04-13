from django.shortcuts import render, redirect
from .models import Login, UserRegistration, Message, Drafts, Feedback, BlockList
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime
import datetime as dt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import pickle
import random

# ── Load ML model once at startup ──────────────────────────────────────────
pipe = pickle.load(open("Naive_model.pkl", "rb"))


# ── Helper: require logged-in user session ──────────────────────────────────
def get_user_or_redirect(request):
    """Returns (UserRegistration, image) or (None, None) if not logged in."""
    uid = request.session.get('uid')
    if not uid:
        return None, None
    try:
        userData = UserRegistration.objects.get(loginid=uid)
        return userData, userData.image
    except UserRegistration.DoesNotExist:
        return None, None


# ── Public pages ────────────────────────────────────────────────────────────

def index(request):
    return render(request, "index.html")


def logins(request):
    if request.method == "POST":
        email = request.POST["email"]
        passw = request.POST["password"]
        user  = authenticate(username=email, password=passw)
        if user is not None:
            login(request, user)
            if user.userType == "Admin":
                messages.info(request, "Login Success")
                return redirect("/adminHome")
            elif user.userType == "User":
                request.session["uid"] = user.id
                messages.info(request, "Login Success")
                return redirect("/userHome")
        else:
            messages.error(request, "Invalid Username/Password")
    return render(request, "login.html")


def register(request):
    current_date = datetime.today().strftime("%Y-%m-%d")
    if request.method == "POST":
        name     = request.POST["name"]
        email    = request.POST["email"]
        phone    = request.POST["phone"]
        dob      = request.POST["dob"]
        gender   = request.POST["gender"]
        address  = request.POST["address"]
        password = request.POST["password"]
        image    = request.FILES["image"]

        logUser = Login.objects.create_user(
            username=email, password=password,
            userType="User", viewPass=password, is_active=1,
        )
        logUser.save()

        UserRegistration.objects.create(
            name=name, email=email, phone=phone, gender=gender,
            address=address, dob=dob, loginid=logUser, image=image,
        ).save()

        messages.success(request, "Account created! Please log in.")
        return redirect("/login")

    return render(request, "register.html", {"current_date": current_date})


# ── Admin views ─────────────────────────────────────────────────────────────

def adminHome(request):
    from math import floor

    total_users       = UserRegistration.objects.count()
    blocked_users     = BlockList.objects.count()
    total_feedbacks   = Feedback.objects.count()
    total_mails       = Message.objects.count()

    # prediction_result is saved as "1" or "0" (strings) by pipe.predict()
    phishing_detected  = Message.objects.filter(prediction_result="1").count()
    safe_count         = Message.objects.filter(prediction_result="0").count()
    unclassified_count = total_mails - phishing_detected - safe_count

    def pct(part, whole):
        return round((part / whole) * 100, 1) if whole else 0

    CIRC = 377  # SVG circumference for r=60

    def arc(part, whole):
        return round((part / whole) * CIRC, 1) if whole else 0

    phishing_arc          = arc(phishing_detected, total_mails)
    safe_arc              = arc(safe_count, total_mails)
    unclassified_arc      = arc(unclassified_count, total_mails)
    phishing_and_safe_arc = round(phishing_arc + safe_arc, 1)

    recent_messages = Message.objects.select_related('fromMail').order_by('-date', '-id')[:10]

    return render(request, "ADMIN/adminHome.html", {
        "total_users":           total_users,
        "blocked_users":         blocked_users,
        "total_feedbacks":       total_feedbacks,
        "total_mails":           total_mails,
        "phishing_detected":     phishing_detected,
        "safe_count":            safe_count,
        "unclassified_count":    unclassified_count,
        "phishing_rate":         pct(phishing_detected, total_mails),
        "safe_rate":             pct(safe_count, total_mails),
        "unclassified_rate":     pct(unclassified_count, total_mails),
        "phishing_arc":          phishing_arc,
        "safe_arc":              safe_arc,
        "unclassified_arc":      unclassified_arc,
        "phishing_and_safe_arc": phishing_and_safe_arc,
        "recent_messages":       recent_messages,
    })


def viewUsers(request):
    userData         = UserRegistration.objects.select_related('loginid').all()
    total_mails      = Message.objects.count()
    phishing_detected = Message.objects.filter(prediction_result="1").count()
    return render(request, "ADMIN/viewUsers.html", {
        "userData":          userData,
        "count":             userData.count(),
        "approved":          UserRegistration.objects.filter(loginid__is_active=1).count(),
        "pending":           UserRegistration.objects.filter(loginid__is_active=0).count(),
        "total_mails":       total_mails,
        "phishing_detected": phishing_detected,
    })


def adminBlockedUsers(request):
    blockData   = BlockList.objects.all()
    total_users = UserRegistration.objects.count()
    return render(request, "ADMIN/blockedUsers.html", {
        "blockData":   blockData,
        "total_users": total_users,
    })


def restrictUser(request):
    id = request.GET["id"]
    Login.objects.filter(username=id).update(is_active=0)
    BlockList.objects.filter(blocked_user_id=id).update(status="Restricted")
    return redirect("/adminBlockedUsers")


def allowUser(request):
    id = request.GET["id"]
    Login.objects.filter(username=id).update(is_active=1)
    BlockList.objects.filter(blocked_user_id=id).update(status="Blocked")
    return redirect("/adminBlockedUsers")


def manageUser(request):
    id     = request.GET["id"]
    status = request.GET["status"]
    abc    = Login.objects.get(id=id)
    abc.is_active = int(status)
    abc.save()
    messages.success(request, "User Approved" if status == "1" else "User Rejected")
    return redirect("/viewUsers")


def viewFeedbacks(request):
    feedbackData = Feedback.objects.select_related('uid').all()
    total_users  = UserRegistration.objects.count()
    return render(request, "ADMIN/viewFeedbacks.html", {
        "feedbackData": feedbackData,
        "count":        feedbackData.count(),
        "total_users":  total_users,
    })


# ── User views ───────────────────────────────────────────────────────────────

def userHome(request):
    userData, image = get_user_or_redirect(request)
    if not userData:
        return redirect("/login")
    return render(request, "USER/userHome.html", {"image": image})


def viewProfile(request):
    userData, image = get_user_or_redirect(request)
    if not userData:
        return redirect("/login")
    # Pass as queryset so template can loop with {% for i in userData %}
    qs = UserRegistration.objects.filter(loginid=request.session['uid'])
    return render(request, "USER/profile.html", {"image": image, "userData": qs})


def updateProfile(request):
    userData, image = get_user_or_redirect(request)
    if not userData:
        return redirect("/login")

    uid          = request.session['uid']
    current_date = datetime.today().strftime("%Y-%m-%d")
    qs           = UserRegistration.objects.filter(loginid=uid)

    if request.method == "POST":
        name     = request.POST["name"]
        email    = request.POST["email"]
        phone    = request.POST["phone"]
        dob      = request.POST["dob"]
        gender   = request.POST["gender"]
        address  = request.POST["address"]
        password = request.POST["password"]

        logUser          = Login.objects.get(id=uid)
        logUser.username = email
        logUser.viewPass = password
        logUser.set_password(password)
        logUser.save()

        userReg         = UserRegistration.objects.get(loginid=uid)
        userReg.name    = name
        userReg.phone   = phone
        userReg.email   = email
        userReg.dob     = dob
        userReg.gender  = gender
        userReg.address = address

        # Only update image if a new file was uploaded
        if 'image' in request.FILES:
            userReg.image = request.FILES['image']
            image = userReg.image

        userReg.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("/viewProfile")

    return render(request, "USER/updateProfile.html", {
        "userData":     qs,
        "current_date": current_date,
        "image":        image,
    })


def compose(request):
    userData, image = get_user_or_redirect(request)
    if not userData:
        return redirect("/login")

    uid          = request.session['uid']
    mailid       = userData.email
    current_date = datetime.today().strftime("%Y-%m-%d")
    current_time = dt.datetime.now().strftime("%I:%M %p")
    count        = Message.objects.filter(sendto=mailid).count()

    if "send" in request.POST:
        toaddress = request.POST['to']
        subject   = request.POST['subject']
        desc      = request.POST['desc']

        # Block self-send
        if toaddress == mailid:
            messages.warning(request, "⚠ You cannot send mail to yourself")
            return redirect("/compose")

        # Block check
        if BlockList.objects.filter(blocking_user_id=toaddress, blocked_user_id=mailid).exists():
            messages.error(request, "You are blocked by this user")
            return render(request, 'USER/compose.html', {"image": image, "count": count})

        msg = Message.objects.create(
            fromMail=userData, sendto=toaddress,
            subject=subject, description=desc,
            date=current_date, time=current_time,
        )
        msg.save()

        output = pipe.predict([desc])[0]
        msg.prediction_result = str(output)   # store as "1" or "0" string
        msg.save()

        return render(request, 'USER/compose.html', {
            "image": image, "count": count, "prediction": output
        })

    elif "draft" in request.POST:
        toaddress = request.POST['to']
        subject   = request.POST['subject']
        desc      = request.POST['desc']
        Drafts.objects.create(
            fromMail=userData, sendto=toaddress,
            subject=subject, description=desc,
            date=current_date, time=current_time,
        ).save()
        messages.success(request, "Added to Drafts")

    return render(request, 'USER/compose.html', {"image": image, "count": count})


def inbox(request):
    userData, image = get_user_or_redirect(request)
    if not userData:
        return redirect("/login")

    email     = userData.email
    inboxData = Message.objects.filter(
        Q(sendto=email) & Q(status="Sent")
    ).order_by("id")

    # Auto-block phishing senders
    for d in inboxData:
        if str(d.prediction_result) == "1":
            fromm = d.fromMail.email
            _, created = BlockList.objects.get_or_create(
                blocking_user_id=email,
                blocked_user_id=fromm,
            )
            if created:
                messages.success(request, f"{fromm} auto-blocked (phishing detected)")

    count = Message.objects.filter(sendto=email).count()
    return render(request, 'USER/inbox.html', {
        "image": image, "inboxData": inboxData, "count": count
    })


def readMail(request):
    userData, image = get_user_or_redirect(request)
    if not userData:
        return redirect("/login")

    mid     = request.GET['id']
    msgData = Message.objects.get(id=mid)
    email   = userData.email
    count   = Message.objects.filter(sendto=email).count()

    # VADER sentiment
    con      = msgData.description
    analyser = SentimentIntensityAnalyzer()
    scores   = analyser.polarity_scores(con)
    cnt      = scores['pos']
    cntn     = scores['neg'] * 100

    # URL match check (first 50 rows only)
    try:
        data = pd.read_csv("phishing_site_urls.csv")
        for i, cd in enumerate(data["URL"]):
            if i >= 50:
                break
            if con == cd:
                cntn = random.randint(60, 99)
                break
    except Exception:
        pass

    rem = 100 - cntn

    return render(request, 'USER/readMail.html', {
        "image":   image,
        "msgData": msgData,
        "count":   count,
        "cnt":     cnt,
        "cntn":    cntn,
        "rem":     rem,
    })


def deleteMail(request):
    # Guard session
    if 'uid' not in request.session:
        return redirect("/login")
    id = request.GET['id']
    Message.objects.filter(id=id).delete()
    return redirect("/outBox")


def outBox(request):
    userData, image = get_user_or_redirect(request)
    if not userData:
        return redirect("/login")

    uid        = request.session['uid']
    outBoxData = Message.objects.filter(
        Q(fromMail_id__loginid=uid) & Q(status="Sent")
    ).order_by('-date', '-time')

    # Pass count for inbox nav badge
    count = Message.objects.filter(sendto=userData.email).count()

    return render(request, "USER/outBox.html", {
        "outBoxData": outBoxData,
        "image":      image,
        "count":      count,
    })


def drafts(request):
    userData, image = get_user_or_redirect(request)
    if not userData:
        return redirect("/login")

    uid       = request.session['uid']
    draftData = Drafts.objects.filter(
        Q(fromMail_id__loginid=uid) & Q(status="Draft")
    ).order_by('-date', '-time')
    count = Message.objects.filter(sendto=userData.email).count()

    return render(request, "USER/drafts.html", {
        "draftData": draftData,
        "image":     image,
        "count":     count,
    })


def readDraft(request):
    userData, image = get_user_or_redirect(request)
    if not userData:
        return redirect("/login")

    mid          = request.GET['id']
    msgData      = Drafts.objects.get(id=mid)
    count        = Message.objects.filter(sendto=userData.email).count()
    current_time = dt.datetime.now().strftime("%I:%M %p")
    current_date = datetime.today().strftime("%Y-%m-%d")

    if request.method == "POST":
        toaddress = request.POST['to']
        subject   = request.POST['subject']
        desc      = request.POST['desc']
        Message.objects.create(
            fromMail=userData, sendto=toaddress,
            subject=subject, description=desc,
            date=current_date, time=current_time,
        ).save()
        Drafts.objects.filter(id=mid).delete()
        return redirect("/outBox")

    return render(request, 'USER/readDrafts.html', {
        "image":   image,
        "msgData": msgData,
        "count":   count,
    })


def addFeedback(request):
    userData, image = get_user_or_redirect(request)
    if not userData:
        return redirect("/login")

    count = Message.objects.filter(sendto=userData.email).count()

    if request.method == "POST":
        subject  = request.POST.get('subject', '').strip()
        feedback = request.POST.get('desc', '').strip()
        if subject and feedback:
            Feedback.objects.create(
                subject=subject, feedback=feedback, uid=userData
            ).save()
            messages.success(request, "Feedback submitted successfully!")
        else:
            messages.error(request, "Please fill in all fields.")

    return render(request, "USER/addFeedback.html", {
        "image": image,
        "count": count,
    })


def blockUser(request):
    if 'uid' not in request.session:
        return redirect("/login")
    fromm = request.GET['from']
    to    = request.GET['to']
    BlockList.objects.create(blocking_user_id=to, blocked_user_id=fromm).save()
    messages.success(request, f"{fromm} Blocked")
    return redirect("/inbox")


def unblockUser(request):
    if 'uid' not in request.session:
        return redirect("/login")
    fromm = request.GET['from']
    to    = request.GET['to']
    BlockList.objects.filter(
        blocking_user_id=to, blocked_user_id=fromm
    ).delete()
    messages.success(request, f"{fromm} Unblocked Successfully")
    return redirect("/blockedUsers")


def blockedUsers(request):
    userData, image = get_user_or_redirect(request)
    if not userData:
        return redirect("/login")

    blocked = BlockList.objects.filter(blocking_user_id=userData.email)
    count   = Message.objects.filter(sendto=userData.email).count()

    return render(request, "USER/blockedUsers.html", {
        "blocked": blocked,
        "image":   image,
        "count":   count,
    })
    
    
def userHeader(request):
    return render(request, "USER/userHeader.html")

def adminHeader(request):
    return render(request, "ADMIN/adminHeader.html")