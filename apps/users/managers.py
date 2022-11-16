from django.db.models import Manager
from django.db.models.query import QuerySet


class UserQuerySet(QuerySet):
    def query_user_by_email(self, email):
        return self.filter(email__icontains=email)

    def query_user_by_first_name(self, first_name):
        return self.filter(first_name__icontains=first_name)

    def get_user_page_info(self, offset, limit):
        return self[offset:offset + limit]


class UserManager(Manager):
    def get_queryset(self):
        return UserQuerySet(self.model)

    def get_user_count(self):
        return self.all().count()

    def get_user_by_email(self, email):
        return self.filter(email__icontains=email)

    def get_user_by_first_name(self, first_name):
        return self.filter(first_name__icontains=first_name)

