from datetime import date, datetime
from django.db import models
from django.conf import settings
# Create your models here.


class UserWithProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()
    picture = models.ImageField(upload_to='image_uploads', default='defaults/default_profile.jpg')


class Issue(models.Model):
    title = models.TextField()
    summary = models.TextField(default="")
    category_name = models.TextField(default="")
    modified_time = models.DateTimeField(null=True)
    last_decision_time = models.DateTimeField(null=True, blank=True)

    def issue_json(self, include_messages=False):
        json = {'id': self.id, 'subject': self.title, 'last_decision_time': self.last_decision_time,
                'summary': self.summary, 'category_name': self.category_name }
        if include_messages:
            messages = self.messages
            json['messages'] = []
            for message in messages.all():
                json['messages'].append(message.message_json())
        return json


class Message(models.Model):
    text = models.TextField()
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reply_to = models.ForeignKey('self', blank=True, null=True, related_name='replies')
    issue = models.ForeignKey(Issue, related_name='messages')
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def message_json(self, get_replies=True):
        json = {'id': self.id, 'text': self.text, 'poster': {'username' : self.poster.username, 'id': self.poster.id}, 'reply_to': self.reply_to_id, 'issue': self.issue.id, 'created': self.created, 'edited': self.edited}
        json['liked_by'] = []
        likes = MessageVote.objects.filter(message_id=self.id).values_list('user_id', flat=True)
        for liker_id in likes:
            json['liked_by'].append(liker_id)

        if get_replies > 0:
            json['replies'] = []
            for reply in self.replies.all():
                json['replies'].append(reply.message_json(False))
        return json


class MessageVote(models.Model):
    message = models.ForeignKey(Message)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    vote_value = models.IntegerField()

    class Meta:
        unique_together = (("message", "user"),)


class IssueSubscription(models.Model):
    issue = models.ForeignKey(Issue)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="subscriptions")

    class Meta:
        unique_together = (("issue", "user"),)
