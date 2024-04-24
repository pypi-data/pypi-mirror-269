from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.utils.timezone import localdate, localtime

import graphene
from graphene_django.types import DjangoObjectType
from guardian.shortcuts import get_objects_for_user
from reversion import create_revision, set_comment, set_user

from aleksis.apps.alsijil.util.predicates import can_edit_documentation, is_in_allowed_time_range
from aleksis.apps.chronos.models import LessonEvent
from aleksis.apps.chronos.schema import LessonEventType
from aleksis.apps.cursus.models import Subject
from aleksis.apps.cursus.schema import CourseType, SubjectType
from aleksis.core.models import Person
from aleksis.core.schema.base import (
    DjangoFilterMixin,
    PermissionsTypeMixin,
)
from aleksis.core.util.core_helpers import get_site_preferences

from ..models import Documentation


class DocumentationType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = Documentation
        fields = (
            "id",
            "course",
            "amends",
            "subject",
            "topic",
            "homework",
            "group_note",
            "datetime_start",
            "datetime_end",
            "date_start",
            "date_end",
            "teachers",
        )
        filter_fields = {
            "id": ["exact", "lte", "gte"],
            "course__name": ["exact"],
        }

    course = graphene.Field(CourseType, required=False)
    amends = graphene.Field(lambda: LessonEventType, required=False)
    subject = graphene.Field(SubjectType, required=False)

    future_notice = graphene.Boolean(required=False)

    old_id = graphene.ID(required=False)

    @staticmethod
    def resolve_teachers(root: Documentation, info, **kwargs):
        if not str(root.pk).startswith("DUMMY") and hasattr(root, "teachers"):
            return root.teachers
        elif root.amends.amends:
            if root.amends.teachers:
                return root.amends.teachers
            else:
                return root.amends.amends.teachers
        return root.amends.teachers

    @staticmethod
    def resolve_future_notice(root: Documentation, info, **kwargs):
        """Show whether the user can't edit the documentation because it's in the future."""
        return not is_in_allowed_time_range(info.context.user, root) and can_edit_documentation(
            info.context.user, root
        )

    @classmethod
    def get_queryset(cls, queryset, info):
        return get_objects_for_user(info.context.user, "alsijil.view_documentation", queryset)


class DocumentationInputType(graphene.InputObjectType):
    id = graphene.ID(required=True)
    course = graphene.ID(required=False)
    subject = graphene.ID(required=False)
    teachers = graphene.List(graphene.ID, required=False)

    topic = graphene.String(required=False)
    homework = graphene.String(required=False)
    group_note = graphene.String(required=False)


class DocumentationBatchCreateOrUpdateMutation(graphene.Mutation):
    class Arguments:
        input = graphene.List(DocumentationInputType)

    documentations = graphene.List(DocumentationType)

    @classmethod
    def create_or_update(cls, info, doc):
        _id = doc.id

        # Sadly, we can't use the update_or_create method since create_defaults
        # is only introduced in Django 5.0
        if _id.startswith("DUMMY"):
            dummy, lesson_event_id, datetime_start_iso, datetime_end_iso = _id.split(";")
            lesson_event = LessonEvent.objects.get(id=lesson_event_id)

            datetime_start = datetime.fromisoformat(datetime_start_iso).astimezone(
                lesson_event.timezone
            )
            datetime_end = datetime.fromisoformat(datetime_end_iso).astimezone(
                lesson_event.timezone
            )

            if info.context.user.has_perm(
                "alsijil.add_documentation_for_lesson_event_rule", lesson_event
            ) and (
                get_site_preferences()["alsijil__allow_edit_future_documentations"] == "all"
                or (
                    get_site_preferences()["alsijil__allow_edit_future_documentations"]
                    == "current_day"
                    and datetime_start.date() <= localdate()
                )
                or (
                    get_site_preferences()["alsijil__allow_edit_future_documentations"]
                    == "current_time"
                    and datetime_start <= localtime()
                )
            ):
                if lesson_event.amends:
                    if lesson_event.course:
                        course = lesson_event.course
                    else:
                        course = lesson_event.amends.course

                    if lesson_event.subject:
                        subject = lesson_event.subject
                    else:
                        subject = lesson_event.amends.subject

                    if lesson_event.teachers:
                        teachers = lesson_event.teachers
                    else:
                        teachers = lesson_event.amends.teachers
                else:
                    course, subject, teachers = (
                        lesson_event.course,
                        lesson_event.subject,
                        lesson_event.teachers,
                    )

                obj = Documentation.objects.create(
                    datetime_start=datetime_start,
                    datetime_end=datetime_end,
                    amends=lesson_event,
                    course=course,
                    subject=subject,
                    topic=doc.topic or "",
                    homework=doc.homework or "",
                    group_note=doc.group_note or "",
                )
                if doc.teachers is not None:
                    obj.teachers.add(*doc.teachers)
                else:
                    obj.teachers.set(teachers.all())
                obj.save()
                return obj
            raise PermissionDenied()
        else:
            obj = Documentation.objects.get(id=_id)

            if not info.context.user.has_perm("alsijil.edit_documentation_rule", obj):
                raise PermissionDenied()

            if doc.topic is not None:
                obj.topic = doc.topic
            if doc.homework is not None:
                obj.homework = doc.homework
            if doc.group_note is not None:
                obj.group_note = doc.group_note

            if doc.subject is not None:
                obj.subject = Subject.objects.get(pk=doc.subject)
            if doc.teachers is not None:
                obj.teachers.set(Person.objects.filter(pk__in=doc.teachers))

            obj.save()
            return obj

    @classmethod
    def mutate(cls, root, info, input):  # noqa
        with create_revision():
            set_user(info.context.user)
            set_comment("Updated in coursebook")
            objs = [cls.create_or_update(info, doc) for doc in input]

        return DocumentationBatchCreateOrUpdateMutation(documentations=objs)
