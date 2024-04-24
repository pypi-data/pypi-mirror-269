from datetime import date, datetime
from typing import Optional, Union
from urllib.parse import urlparse

from django.db import models
from django.db.models import QuerySet
from django.db.models.constraints import CheckConstraint
from django.db.models.query_utils import Q
from django.http import HttpRequest
from django.urls import reverse
from django.utils.formats import date_format
from django.utils.translation import gettext_lazy as _

from calendarweek import CalendarWeek
from colorfield.fields import ColorField

from aleksis.apps.alsijil.data_checks import (
    ExcusesWithoutAbsences,
    LessonDocumentationOnHolidaysDataCheck,
    NoGroupsOfPersonsSetInPersonalNotesDataCheck,
    NoPersonalNotesInCancelledLessonsDataCheck,
    PersonalNoteOnHolidaysDataCheck,
)
from aleksis.apps.alsijil.managers import (
    GroupRoleAssignmentManager,
    GroupRoleAssignmentQuerySet,
    GroupRoleManager,
    GroupRoleQuerySet,
    LessonDocumentationManager,
    LessonDocumentationQuerySet,
    PersonalNoteManager,
    PersonalNoteQuerySet,
)
from aleksis.apps.chronos.managers import GroupPropertiesMixin
from aleksis.apps.chronos.mixins import WeekRelatedMixin
from aleksis.apps.chronos.models import Event, ExtraLesson, LessonEvent, LessonPeriod, TimePeriod
from aleksis.apps.chronos.util.format import format_m2m
from aleksis.apps.cursus.models import Course, Subject
from aleksis.apps.kolego.models import Absence as KolegoAbsence
from aleksis.apps.kolego.models import AbsenceReason
from aleksis.core.data_checks import field_validation_data_check_factory
from aleksis.core.mixins import ExtensibleModel, GlobalPermissionModel
from aleksis.core.models import CalendarEvent, Group, SchoolTerm
from aleksis.core.util.core_helpers import get_site_preferences
from aleksis.core.util.model_helpers import ICONS


def isidentifier(value: str) -> bool:
    return value.isidentifier()


class ExcuseType(ExtensibleModel):
    """An type of excuse.

    Can be used to count different types of absences separately.
    """

    short_name = models.CharField(max_length=255, unique=True, verbose_name=_("Short name"))
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))

    count_as_absent = models.BooleanField(
        default=True,
        verbose_name=_("Count as absent"),
        help_text=_(
            "If checked, this excuse type will be counted as a missed lesson. If not checked,"
            "it won't show up in the absence report."
        ),
    )

    def __str__(self):
        return f"{self.name} ({self.short_name})"

    @property
    def count_label(self):
        return f"excuse_type_{self.id}_count"

    class Meta:
        ordering = ["name"]
        verbose_name = _("Excuse type")
        verbose_name_plural = _("Excuse types")


lesson_related_constraint_q = (
    Q(
        lesson_period__isnull=False,
        event__isnull=True,
        extra_lesson__isnull=True,
        week__isnull=False,
        year__isnull=False,
    )
    | Q(
        lesson_period__isnull=True,
        event__isnull=False,
        extra_lesson__isnull=True,
        week__isnull=True,
        year__isnull=True,
    )
    | Q(
        lesson_period__isnull=True,
        event__isnull=True,
        extra_lesson__isnull=False,
        week__isnull=True,
        year__isnull=True,
    )
)


class RegisterObjectRelatedMixin(WeekRelatedMixin):
    """Mixin with common API for lesson documentations and personal notes."""

    @property
    def register_object(
        self: Union["LessonDocumentation", "PersonalNote"],
    ) -> Union[LessonPeriod, Event, ExtraLesson]:
        """Get the object related to this lesson documentation or personal note."""
        if self.lesson_period:
            return self.lesson_period
        elif self.event:
            return self.event
        else:
            return self.extra_lesson

    @property
    def register_object_key(self: Union["LessonDocumentation", "PersonalNote"]) -> str:
        """Get a unique reference to the related object related."""
        if self.week and self.year:
            return f"{self.register_object.pk}_{self.week}_{self.year}"
        else:
            return self.register_object.pk

    @property
    def calendar_week(self: Union["LessonDocumentation", "PersonalNote"]) -> CalendarWeek:
        """Get the calendar week of this lesson documentation or personal note.

        .. note::

            As events can be longer than one week,
            this will return the week of the start date for events.
        """
        if self.lesson_period:
            return CalendarWeek(week=self.week, year=self.year)
        elif self.extra_lesson:
            return self.extra_lesson.calendar_week
        else:
            return CalendarWeek.from_date(self.register_object.date_start)

    @property
    def school_term(self: Union["LessonDocumentation", "PersonalNote"]) -> SchoolTerm:
        """Get the school term of the related register object."""
        if self.lesson_period:
            return self.lesson_period.lesson.validity.school_term
        else:
            return self.register_object.school_term

    @property
    def date(self: Union["LessonDocumentation", "PersonalNote"]) -> Optional[date]:
        """Get the date of this lesson documentation or personal note.

        :: warning::

            As events can be longer than one day,
            this will return `None` for events.
        """
        if self.lesson_period:
            return super().date
        elif self.extra_lesson:
            return self.extra_lesson.date
        return None

    @property
    def date_formatted(self: Union["LessonDocumentation", "PersonalNote"]) -> str:
        """Get a formatted version of the date of this object.

        Lesson periods, extra lessons: formatted date
        Events: formatted date range
        """
        return (
            date_format(self.date)
            if self.date
            else f"{date_format(self.event.date_start)}–{date_format(self.event.date_end)}"
        )

    @property
    def period(self: Union["LessonDocumentation", "PersonalNote"]) -> TimePeriod:
        """Get the date of this lesson documentation or personal note.

        :: warning::

            As events can be longer than one day,
            this will return `None` for events.
        """
        if self.event:
            return self.event.period_from
        else:
            return self.register_object.period

    @property
    def period_formatted(self: Union["LessonDocumentation", "PersonalNote"]) -> str:
        """Get a formatted version of the period of this object.

        Lesson periods, extra lessons: formatted period
        Events: formatted period range
        """
        return (
            f"{self.period.period}."
            if not self.event
            else f"{self.event.period_from.period}.–{self.event.period_to.period}."
        )

    def get_absolute_url(self: Union["LessonDocumentation", "PersonalNote"]) -> str:
        """Get the absolute url of the detail view for the related register object."""
        return self.register_object.get_alsijil_url(self.calendar_week)


class PersonalNote(RegisterObjectRelatedMixin, ExtensibleModel):
    """A personal note about a single person.

    Used in the class register to note absences, excuses
    and remarks about a student in a single lesson period.
    """

    data_checks = [
        NoPersonalNotesInCancelledLessonsDataCheck,
        NoGroupsOfPersonsSetInPersonalNotesDataCheck,
        PersonalNoteOnHolidaysDataCheck,
        ExcusesWithoutAbsences,
    ]

    objects = PersonalNoteManager.from_queryset(PersonalNoteQuerySet)()

    person = models.ForeignKey("core.Person", models.CASCADE, related_name="personal_notes")
    groups_of_person = models.ManyToManyField("core.Group", related_name="+")

    week = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(verbose_name=_("Year"), blank=True, null=True)

    lesson_period = models.ForeignKey(
        "chronos.LessonPeriod", models.CASCADE, related_name="personal_notes", blank=True, null=True
    )
    event = models.ForeignKey(
        "chronos.Event", models.CASCADE, related_name="personal_notes", blank=True, null=True
    )
    extra_lesson = models.ForeignKey(
        "chronos.ExtraLesson", models.CASCADE, related_name="personal_notes", blank=True, null=True
    )

    absent = models.BooleanField(default=False)
    tardiness = models.PositiveSmallIntegerField(default=0)
    excused = models.BooleanField(default=False)
    excuse_type = models.ForeignKey(
        ExcuseType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Excuse type"),
    )

    remarks = models.CharField(max_length=200, blank=True)

    extra_marks = models.ManyToManyField("ExtraMark", blank=True, verbose_name=_("Extra marks"))

    def save(self, *args, **kwargs):
        if self.excuse_type:
            self.excused = True
        if not self.absent:
            self.excused = False
            self.excuse_type = None
        super().save(*args, **kwargs)

    def reset_values(self):
        """Reset all saved data to default values.

        .. warning ::

            This won't save the data, please execute ``save`` extra.
        """
        defaults = PersonalNote()

        self.absent = defaults.absent
        self.tardiness = defaults.tardiness
        self.excused = defaults.excused
        self.excuse_type = defaults.excuse_type
        self.remarks = defaults.remarks
        self.extra_marks.clear()

    def __str__(self) -> str:
        return f"{self.date_formatted}, {self.lesson_period}, {self.person}"

    def get_absolute_url(self) -> str:
        """Get the absolute url of the detail view for the related register object."""
        return urlparse(super().get_absolute_url())._replace(fragment="personal-notes").geturl()

    class Meta:
        verbose_name = _("Personal note")
        verbose_name_plural = _("Personal notes")
        ordering = [
            "year",
            "week",
            "lesson_period__period__weekday",
            "lesson_period__period__period",
            "person__last_name",
            "person__first_name",
        ]
        constraints = [
            CheckConstraint(
                check=lesson_related_constraint_q, name="one_relation_only_personal_note"
            ),
            models.UniqueConstraint(
                fields=("week", "year", "lesson_period", "person"),
                name="unique_note_per_lp",
            ),
            models.UniqueConstraint(
                fields=("week", "year", "event", "person"),
                name="unique_note_per_ev",
            ),
            models.UniqueConstraint(
                fields=("week", "year", "extra_lesson", "person"),
                name="unique_note_per_el",
            ),
        ]


class LessonDocumentation(RegisterObjectRelatedMixin, ExtensibleModel):
    """A documentation on a single lesson period.

    Non-personal, includes the topic and homework of the lesson.
    """

    objects = LessonDocumentationManager.from_queryset(LessonDocumentationQuerySet)()

    data_checks = [LessonDocumentationOnHolidaysDataCheck]

    week = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(verbose_name=_("Year"), blank=True, null=True)

    lesson_period = models.ForeignKey(
        "chronos.LessonPeriod", models.CASCADE, related_name="documentations", blank=True, null=True
    )
    event = models.ForeignKey(
        "chronos.Event", models.CASCADE, related_name="documentations", blank=True, null=True
    )
    extra_lesson = models.ForeignKey(
        "chronos.ExtraLesson", models.CASCADE, related_name="documentations", blank=True, null=True
    )

    topic = models.CharField(verbose_name=_("Lesson topic"), max_length=200, blank=True)
    homework = models.CharField(verbose_name=_("Homework"), max_length=200, blank=True)
    group_note = models.CharField(verbose_name=_("Group note"), max_length=200, blank=True)

    def carry_over_data(self, all_periods_of_lesson: LessonPeriod):
        """Carry over data to given periods in this lesson if data is not already set.

        Both forms of carrying over data can be deactivated using site preferences
        ``alsijil__carry_over_next_periods`` and ``alsijil__allow_carry_over_same_week``
        respectively.
        """
        for period in all_periods_of_lesson:
            lesson_documentation = period.get_or_create_lesson_documentation(
                CalendarWeek(week=self.week, year=self.year)
            )

            changed = False

            if not lesson_documentation.topic:
                lesson_documentation.topic = self.topic
                changed = True

            if not lesson_documentation.homework:
                lesson_documentation.homework = self.homework
                changed = True

            if not lesson_documentation.group_note:
                lesson_documentation.group_note = self.group_note
                changed = True

            if changed:
                lesson_documentation.save(carry_over_next_periods=False)

    def __str__(self) -> str:
        return f"{self.lesson_period}, {self.date_formatted}"

    def save(self, carry_over_next_periods=True, *args, **kwargs):
        if (
            get_site_preferences()["alsijil__carry_over_next_periods"]
            and (self.topic or self.homework or self.group_note)
            and self.lesson_period
            and carry_over_next_periods
        ):
            self.carry_over_data(
                LessonPeriod.objects.filter(
                    lesson=self.lesson_period.lesson,
                    period__weekday=self.lesson_period.period.weekday,
                )
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Lesson documentation")
        verbose_name_plural = _("Lesson documentations")
        ordering = [
            "year",
            "week",
            "lesson_period__period__weekday",
            "lesson_period__period__period",
        ]
        constraints = [
            CheckConstraint(
                check=lesson_related_constraint_q,
                name="one_relation_only_lesson_documentation",
            ),
            models.UniqueConstraint(
                fields=("week", "year", "lesson_period"),
                name="unique_documentation_per_lp",
            ),
            models.UniqueConstraint(
                fields=("week", "year", "event"),
                name="unique_documentation_per_ev",
            ),
            models.UniqueConstraint(
                fields=("week", "year", "extra_lesson"),
                name="unique_documentation_per_el",
            ),
        ]


class ExtraMark(ExtensibleModel):
    """A model for extra marks.

    Can be used for lesson-based counting of things (like forgotten homework).
    """

    short_name = models.CharField(max_length=255, unique=True, verbose_name=_("Short name"))
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))

    colour_fg = ColorField(verbose_name=_("Foreground colour"), blank=True)
    colour_bg = ColorField(verbose_name=_("Background colour"), blank=True)

    show_in_coursebook = models.BooleanField(default=True, verbose_name=_("Show in coursebook"))

    def __str__(self):
        return f"{self.name}"

    @property
    def count_label(self):
        return f"extra_mark_{self.id}_count"

    class Meta:
        ordering = ["short_name"]
        verbose_name = _("Extra mark")
        verbose_name_plural = _("Extra marks")


class Documentation(CalendarEvent):
    """A documentation on teaching content in a freely choosable time frame.

    Non-personal, includes the topic and homework of the lesson.
    """

    # FIXME: DataCheck

    course = models.ForeignKey(
        Course,
        models.PROTECT,
        related_name="documentations",
        blank=True,
        null=True,
        verbose_name=_("Course"),
    )

    subject = models.ForeignKey(
        Subject, models.PROTECT, related_name="+", blank=True, null=True, verbose_name=_("Subject")
    )

    teachers = models.ManyToManyField(
        "core.Person",
        related_name="documentations_as_teacher",
        blank=True,
        null=True,
        verbose_name=_("Teachers"),
    )

    topic = models.CharField(verbose_name=_("Lesson Topic"), max_length=255, blank=True)
    homework = models.CharField(verbose_name=_("Homework"), max_length=255, blank=True)
    group_note = models.CharField(verbose_name=_("Group Note"), max_length=255, blank=True)

    def get_subject(self) -> str:
        if self.subject:
            return self.subject
        if self.amends:
            if self.amends.subject:
                return self.amends.subject
            if self.amends.course:
                return self.amends.course.subject
        if self.course:
            return self.course.subject

    def get_groups(self) -> QuerySet[Group]:
        if self.amends:
            return self.amends.actual_groups
        if self.course:
            return self.course.groups.all()

    def __str__(self) -> str:
        start_datetime = CalendarEvent.value_start_datetime(self)
        end_datetime = CalendarEvent.value_end_datetime(self)
        return (
            f"{format_m2m(self.get_groups())} {self.get_subject()}"
            + f" {start_datetime} - {end_datetime}"
        )

    class Meta:
        verbose_name = _("Documentation")
        verbose_name_plural = _("Documentations")
        # should check if object has either course or amends,
        # which is not possible via constraint, because amends is not local to Documentation

    @classmethod
    def get_for_coursebook(
        cls,
        own: bool,
        date_start: datetime,
        date_end: datetime,
        request: HttpRequest,
        obj_type: Optional[str] = None,
        obj_id: Optional[str] = None,
        incomplete: Optional[bool] = False,
    ) -> list:
        """Get all the documentations for an object and a time frame.

        obj_type may be one of TEACHER, GROUP, ROOM, COURSE
        """

        # 1. Find all LessonEvents for all Lessons of this Course in this date range
        event_params = {
            "own": own,
        }
        if obj_type is not None and obj_id is not None:
            event_params.update(
                {
                    "type": obj_type,
                    "id": obj_id,
                }
            )

        events = LessonEvent.get_single_events(
            date_start,
            date_end,
            request,
            event_params,
            with_reference_object=True,
        )

        # 2. For each lessonEvent → check if there is a documentation
        # if so, add the documentation to a list, if not, create a new one
        docs = []
        for event in events:
            if incomplete and event["STATUS"] == "CANCELLED":
                continue

            event_reference_obj = event["REFERENCE_OBJECT"]
            existing_documentations = event_reference_obj.amended_by.filter(
                datetime_start=event["DTSTART"].dt,
                datetime_end=event["DTEND"].dt,
            )

            if existing_documentations.exists():
                doc = existing_documentations.first()
                if incomplete and doc.topic:
                    continue
                docs.append(doc)
            else:
                if event_reference_obj.amends:
                    if event_reference_obj.course:
                        course = event_reference_obj.course
                    else:
                        course = event_reference_obj.amends.course

                    if event_reference_obj.subject:
                        subject = event_reference_obj.subject
                    else:
                        subject = event_reference_obj.amends.subject
                else:
                    course, subject = event_reference_obj.course, event_reference_obj.subject

                docs.append(
                    cls(
                        pk=f"DUMMY;{event_reference_obj.id};{event['DTSTART'].dt.isoformat()};{event['DTEND'].dt.isoformat()}",
                        amends=event_reference_obj,
                        course=course,
                        subject=subject,
                        datetime_start=event["DTSTART"].dt,
                        datetime_end=event["DTEND"].dt,
                    )
                )

        return docs


class ParticipationStatus(CalendarEvent):
    """A participation or absence record about a single person.

    Used in the class register to note participation or absence of a student
    in a documented unit (e.g. a single lesson event or a custom time frame; see Documentation).
    """

    # FIXME: DataChecks

    person = models.ForeignKey(
        "core.Person", models.CASCADE, related_name="participations", verbose_name=_("Person")
    )
    groups_of_person = models.ManyToManyField(
        "core.Group", related_name="+", verbose_name=_("Groups of Person")
    )

    related_documentation = models.ForeignKey(
        Documentation,
        models.CASCADE,
        related_name="participations",
        verbose_name=_("Documentation"),
    )

    # Absence part
    absent = models.BooleanField(verbose_name=_("Absent"))
    absence_reason = models.ForeignKey(
        AbsenceReason, verbose_name=_("Absence Reason"), on_delete=models.PROTECT
    )

    base_absence = models.ForeignKey(
        KolegoAbsence,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="absences",
        verbose_name=_("Base Absence"),
    )

    def __str__(self) -> str:
        return f"{self.related_documentation}, {self.person}"

    class Meta:
        verbose_name = _("Participation Status")
        verbose_name_plural = _("Participation Status")
        ordering = [
            "related_documentation",
            "person__last_name",
            "person__first_name",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("related_documentation", "person"),
                name="unique_participation_status_per_documentation",
            ),
        ]


class NewPersonalNote(ExtensibleModel):
    person = models.ForeignKey(
        "core.Person", models.CASCADE, related_name="new_personal_notes", verbose_name=_("Person")
    )

    documentation = models.ForeignKey(
        Documentation,
        models.CASCADE,
        related_name="personal_notes",
        verbose_name=_("Documentation"),
        blank=True,
        null=True,
    )

    note = models.TextField(blank=True, verbose_name=_("Note"))
    extra_mark = models.ForeignKey(
        ExtraMark, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_("Extra Mark")
    )

    def __str__(self) -> str:
        return f"{self.person}, {self.note}, {self.extra_mark}"

    class Meta:
        verbose_name = _("Personal Note")
        verbose_name_plural = _("Personal Notes")
        constraints = [
            models.CheckConstraint(
                check=~Q(note="") | Q(extra_mark__isnull=False),
                name="unique_absence_per_documentation",
            ),
        ]


class GroupRole(ExtensibleModel):
    data_checks = [field_validation_data_check_factory("alsijil", "GroupRole", "icon")]

    objects = GroupRoleManager.from_queryset(GroupRoleQuerySet)()

    name = models.CharField(max_length=255, verbose_name=_("Name"), unique=True)
    icon = models.CharField(max_length=50, blank=True, choices=ICONS, verbose_name=_("Icon"))
    colour = ColorField(blank=True, verbose_name=_("Colour"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Group role")
        verbose_name_plural = _("Group roles")
        permissions = (("assign_group_role", _("Can assign group role")),)

    def get_absolute_url(self) -> str:
        return reverse("edit_group_role", args=[self.id])


class GroupRoleAssignment(GroupPropertiesMixin, ExtensibleModel):
    objects = GroupRoleAssignmentManager.from_queryset(GroupRoleAssignmentQuerySet)()

    role = models.ForeignKey(
        GroupRole,
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name=_("Group role"),
    )
    person = models.ForeignKey(
        "core.Person",
        on_delete=models.CASCADE,
        related_name="group_roles",
        verbose_name=_("Assigned person"),
    )
    groups = models.ManyToManyField(
        "core.Group",
        related_name="group_roles",
        verbose_name=_("Groups"),
    )
    date_start = models.DateField(verbose_name=_("Start date"))
    date_end = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("End date"),
        help_text=_("Can be left empty if end date is not clear yet"),
    )

    def __str__(self):
        date_end = date_format(self.date_end) if self.date_end else "?"
        return f"{self.role}: {self.person}, {date_format(self.date_start)}–{date_end}"

    @property
    def date_range(self) -> str:
        if not self.date_end:
            return f"{date_format(self.date_start)}–?"
        else:
            return f"{date_format(self.date_start)}–{date_format(self.date_end)}"

    class Meta:
        verbose_name = _("Group role assignment")
        verbose_name_plural = _("Group role assignments")


class AlsijilGlobalPermissions(GlobalPermissionModel):
    class Meta:
        managed = False
        permissions = (
            ("view_lesson", _("Can view lesson overview")),
            ("view_week", _("Can view week overview")),
            ("view_full_register", _("Can view full register")),
            ("register_absence", _("Can register absence")),
            ("list_personal_note_filters", _("Can list all personal note filters")),
        )
