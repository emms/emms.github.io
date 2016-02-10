from django.shortcuts import loader, redirect, get_object_or_404, render_to_response
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.template import RequestContext, Context
from django.contrib.auth import authenticate, login, logout
from urllib.request import urlopen, quote
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from app.forms import UserForm, UserProfileForm
from django.core import serializers

import json
import logging

from app.models import Message, IssueSubscription
from app.models import Issue
from app.models import MessageVote
from app.models import UserWithProfile

# Create your views here.


@ensure_csrf_cookie
def index(request):
    t = loader.get_template('index.html')
    c = RequestContext(request)
    issueId = request.GET.get('issueId')
    if issueId is not None:
        c = RequestContext(request, {'issueId' : issueId})

    if request is not None:
        c['request'] = request
    c.update(csrf(request))
    return render_to_response('index.html', c)


def get_subscription_dict(userID):
    jsonDict = {}
    subscriptions = IssueSubscription.objects.filter(user=userID)
    for subscription in subscriptions:
        jsonDict[str(subscription.issue_id)] = {'id':subscription.issue_id, 'title': subscription.issue.title}
    return jsonDict


def login_view(request):
    if request.method != 'POST':
        return HttpResponse('Only POST is accepted', status=405)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return JsonResponse({"id": request.user.id, "name": request.user.username, "subscriptions": get_subscription_dict(user.id)});
        else:
            return HttpResponse('Account no longer active')
    else:
        return HttpResponse('Invalid password or username', status=403)


def register(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
            new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, new_user)
            return HttpResponseRedirect('/user/')
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return JsonResponse({'errors': {'profile': profile_form.errors, 'user': user_form.errors}}, status=422);


def current_user(request):
    if request.user.is_authenticated():
        subscriptions = request.user.subscriptions.all()
        userdata = {"id": request.user.id, "name": request.user.username}
        subs = []
        userdata['subscriptions'] = subs
        for s in subscriptions:
            subs.append({'issueId': s.issue.id, 'title': s.issue.title})
        return JsonResponse(userdata)
    else:
        return JsonResponse({'id': 0, 'subscriptions': []})


def user_picture(request, userID):
    if userID == '0':
        return HttpResponseRedirect('/static/img/avatar-placeholder.jpg')
    else:
        user = get_object_or_404(UserWithProfile, user=userID)
        return HttpResponse(user.picture.file, content_type='text/plain')


@login_required
def update_user_picture(request):
    if request.method != 'POST':
        return HttpResponseBadRequest({'error': 'Only POST is accepted'})

    user = get_object_or_404(UserWithProfile, user=request.user.id)
    profile_form = UserProfileForm(data=request.POST)

    if profile_form.is_valid():
        profile = profile_form.save(commit=False)
        profile.user = user.user
        if 'picture' in request.FILES:
            profile.picture = request.FILES['picture']
        profile.save()
        return JsonResponse({'message': 'Profile picture updated'})
    else:
        return HttpResponseBadRequest({'error': 'No picture received from POST files'})



def user_profile(request, userID):
    if request.user.is_authenticated():
        user = get_object_or_404(UserWithProfile, user=userID)
        return render_to_response('static/profile.html',
                           {'user': user},
                           RequestContext(request))
    else:
        return HttpResponseRedirect("/")


def logout_view(request):
    logout(request)
    return HttpResponse('Logged out')


def get_paging_info(request):
    page = request.GET.get('page')
    page_size = request.GET.get('pageSize')
    if page is None or page_size is None:
        return ""
    else:
        return "&page=%s&limit=%s" % (page, page_size)


def get_url_as_string(url):
    json_str = urlopen(url).read().decode('utf-8')
    return json_str


def get_url_as_json(url):
    return json.loads(get_url_as_string(url))


def get_issue_as_json(issueId):
    return get_url_as_json(url = 'http://dev.hel.fi/paatokset/v1/issue/%s/?format=json' % issueId)


def issues_bbox(request):
    if issue_location_index is None:
        issue_location_index = index.Index()

    minLat = float(request.GET.get('minLat')) - 0.005
    maxLat = float(request.GET.get('maxLat')) + 0.005
    minLong = float(request.GET.get('minLong')) - 0.005
    maxLong = float(request.GET.get('maxLong')) + 0.005
    category = request.GET.get('category')
    url = 'http://dev.hel.fi/paatokset/v1/issue/search/?bbox=%.2f,%.2f,%.2f,%.2f%s'\
          % (minLong, minLat, maxLong, maxLat, get_paging_info(request))
    if category is not None:
        url += ('&category=%s' % category)
    return JsonResponse(get_url_as_json(url))


def issues_search_text(request):
    text = request.GET.get('search')
    if text is None or len(text) < 1:
        return HttpResponse('{ "msg" : "Search term must be at least 1 character long" }', 400)
    url = 'http://dev.hel.fi/openahjo/v1/issue/search/?text=%s&format=json&order_by=-latest_decision_date%s'\
          % (quote(text), get_paging_info(request))
    return JsonResponse(get_url_as_json(url))


def recent_decisions(request):
    recent_decisions = Issue.objects.order_by('-last_decision_time')
    issuelist = {}
    issuelist['recent_decisions'] = []
    maxIssues = 50
    for issue in recent_decisions:
        issuelist['recent_decisions'].append({'issueId' : issue.id, 'issueTitle': issue.title, 'lastDecisionTime': issue.last_decision_time})
        if len(issuelist['recent_decisions']) >= maxIssues:
            break
    return JsonResponse(issuelist)



def issues_category(request, category_id):
    url = 'http://dev.hel.fi/openahjo/v1/issue/search/?category=%d&format=json%s'\
          % (int(category_id), get_paging_info(request))
    return JsonResponse(get_url_as_json(url))


def categories(request):
    url = 'http://dev.hel.fi:80/paatokset/v1/category/?level=0'
    return JsonResponse(get_url_as_json(url))


def decisions(request, issueID):
    url = 'http://dev.hel.fi/paatokset/v1/agenda_item/?issue=%s' % issueID
    return JsonResponse(get_url_as_json(url))


def issue(request, issueID):
    fetch_full_details = request.GET.get('fullDetails')
    if fetch_full_details == "true":
        details = get_issue_as_json(issueID)
    else:
        details = get_object_or_404(Issue, id=issueID)
        details = details.issue_json(include_messages=False)
    subscribed = False
    if request.user.is_authenticated():
        subscribes = IssueSubscription.objects.filter(user=request.user, issue=issueID)
        if subscribes.count() > 0:
            subscribed = True
            details['subscribed'] = True
    issuedetails = {'issueID': issueID, 'jsondetails': details, 'subscribed': subscribed}
    messages = Message.objects.filter(issue=issueID, reply_to__isnull=True)
    issuedetails['messages'] = []
    for message in messages:
        issuedetails['messages'].append(message.message_json())

    return JsonResponse(issuedetails)


def messages(request, issueID):
    messages = Message.objects.filter(issue=issueID)
    messagelist = {}
    messagelist['messages'] = []
    for message in messages:
        messagelist['messages'].append({'message': message.message_json()})
        return JsonResponse(messagelist)


def issues_with_messages(request):
    messages = Message.objects.order_by('-edited').select_related('issue')
    issuelist = {}
    issuelist['commented'] = []
    distinctIssues = []
    maxIssues = 10
    for message in messages:
        issue = message.issue
        if issue.id in distinctIssues:
            continue
        else:
            distinctIssues.append(issue.id)
        poster = message.poster.username
        votes = MessageVote.objects.filter(message=message)
        votes_counted = votes.count()
        voted = False
        if request.user.is_authenticated():
            users_votes = votes.filter(user=request.user)
            if users_votes.count() > 0:
                voted = True
        issuelist['commented'].append({'message' : message.text, 'issueId' : issue.id, 'issueTitle': issue.title, 'votes': int(votes_counted), 'voted': bool(voted), 'poster': poster})
        if len(distinctIssues) >= maxIssues:
            break
    return JsonResponse(issuelist)


def edit_message(request, messageID):
    if request.user is None or request.user.is_anonymous():
        return HttpResponseForbidden()
    if request.method == 'PUT':
        message = get_object_or_404(Message, poster=request.user, id=messageID)
        message.text = request.PUT['messagefield']
        message.save()
        return JsonResponse(message)
    elif request.method == 'DELETE':
        message = get_object_or_404(Message, poster=request.user, id=messageID)
        message.delete()
        return HttpResponse('Deleted')
    else:
        return HttpResponseBadRequest('Only PUT and DELETE methods are allowed')


def post_message(request, issueID):
    if request.method == 'GET':
        messages = Message.objects.filter(issue=issueID)
        response = {}
        response['messages'] = []
        if request.user.is_authenticated():
            votes = MessageVote.objects.filter(user=request.user)
        else:
            votes = None

        for m in messages:
            message = m.message_json()
            if votes is not None:
                message['liked'] = votes.filter(message=m).count() > 0
            else:
                message['liked'] = False
            response['messages'].append(message)

        for m in messages:
            replies = Message.objects.filter(reply_to=m)
            response['messages'].append({'replies':replies})

        return JsonResponse(response)
    elif request.user is None or request.user.is_anonymous():
        return HttpResponseForbidden('Please login before posting')
    elif request.method == 'POST':
        issue = Issue.objects.get_or_create(id=issueID)
        if issue[1] is True:
            issue[0].save()
            logging.info("Created object with id %s" % issueID)

        m = Message(text=request.POST['messagefield'], poster=request.user, issue_id=issueID)
        m.save()
        response = m.message_json()
        return JsonResponse(response)
    else:
        return HttpResponseBadRequest("Only POST and GET methods are allowed")


def reply_to_message(request, messageID):
    if request.method == 'POST':
        m = Message(text=request.POST['replyfield'], poster=request.user,
                    reply_to=get_object_or_404(Message, id=messageID),
                    issue_id=get_object_or_404(Message, id=messageID).issue.id)
        m.save()
        response = m.message_json(False)
        return JsonResponse(response)


@login_required
def vote_message(request, messageID):
    if request.method == 'POST':
        value = request.POST['value']
        value = min(int(value), 1)  # only +1 or 0 votes for now
        data = MessageVote.objects.get_or_create(user=request.user, message_id=messageID, vote_value=value)
        vote = data[0]
        vote.save()
        return JsonResponse({'messageId': vote.message.id, 'user': vote.user.username, 'value': vote.vote_value})

    elif request.method == 'DELETE':
        vote = get_object_or_404(MessageVote, user=request.user, message_id=messageID)
        vote.delete()
        return JsonResponse({'commentId': vote.id})

@login_required
def subscribe_issue(request, issueID):

    if request.method == 'POST':
        issue = get_object_or_404(Issue, id=issueID)
        #issue = Issue.objects.get_or_create(id=issueID)
        #if issue[1] is True:
        #    issue[0].title = get_issue_as_json(issueID)['subject']
        #    issue[0].save()
        #    logging.info("Created object with id %s" % issueID)
        data = IssueSubscription.objects.get_or_create(user=request.user, issue_id=issueID)
        subscribe = data[0]
        subscribe.save()
        return JsonResponse({'issueId' : subscribe.issue.id, 'title' : subscribe.issue.title})
    elif request.method == 'DELETE':
        subscribe = get_object_or_404(IssueSubscription, user = request.user, issue_id = issueID)
        subscribe.delete()
        return JsonResponse({'subId' : subscribe.id})


def get_issue_subscriptions(request, userID=None):
    if userID is None:
        if request.user.is_authenticated():
            userID = request.user.id
        else:
            return JsonResponse({'subscriptions': {}})
    list = {'subscriptions' : get_subscription_dict(userID)}
    return JsonResponse(list)

