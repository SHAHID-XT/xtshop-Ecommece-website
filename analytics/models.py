from django.db import models
from auths.models import *
from simple_history.models import HistoricalRecords


class RequestLog(models.Model):
    ip_address = models.CharField(max_length=100)
    visit_count = models.IntegerField(default=1)
    page_url = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    history = HistoricalRecords()
    def __str__(self):
        return str(
            f"{self.ip_address} has visit {self.visit_count} times. url ={self.page_url}"
        )


class UserLoginLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    ip_address = models.CharField(max_length=100)
    login_time = models.DateTimeField(auto_now_add=True)
    login_count = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    history = HistoricalRecords()
    def __str__(self):
        return f"{self.user.username} ({self.ip_address})"


class Page(models.Model):
    url = models.URLField(unique=True)
    history = HistoricalRecords()
    def __str__(self) -> str:
        return self.url


class UserInteraction(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    page_from = models.ForeignKey(
        Page, on_delete=models.SET_NULL, null=True, blank=True, related_name="page_from"
    )
    page_to = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="page_to")
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    time_spent = models.CharField(null=True, blank=True, max_length=100)
    history = HistoricalRecords()
    browser = models.CharField(null=True, blank=True, max_length=100)
    @classmethod
    def create_interaction(cls, user, page_from, page_to, session_id, ip_address):
        interaction = cls(
            user=user,
            page_from=page_from,
            page_to=page_to,
            session_id=session_id,
            ip_address=ip_address,
        )
        interaction.save()

    def __str__(self) -> str:
        if self.user:
            return f"User '{self.user}' visited from page '{self.page_from}' to page '{self.page_to}' - Time Spent: {self.time_spent} seconds"
        else:
            return f"Anonymous user with IP '{self.ip_address}' visited from page '{self.page_from}' to page '{self.page_to}' - Time Spent: {self.time_spent} seconds"
