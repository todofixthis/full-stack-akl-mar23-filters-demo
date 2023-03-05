from datetime import date

import filters as f
from dateutil.relativedelta import relativedelta
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from importer.filters import ApplicantInfoModule, FeedbackModule, \
    LocationModule, NonEmptyString, Session, SessionPrefs, TokensModule
from importer.json import as_json
from importer.models import User as UserModel


@csrf_exempt
def ingest_applicant_info_module(request: HttpRequest) -> HttpResponse:
    """
    Using filters to validate a payload for ``applicantInfoModule``.
    """
    schema = NonEmptyString | f.JsonDecode | f.Type(dict) | f.FilterMapper(
        {
            'birthday': NonEmptyString | f.Date |
                        f.Max(date.today() - relativedelta(years=18)),
            'gender': NonEmptyString | f.Choice({'F', 'M', 'N'}),
            'utcOffset': NonEmptyString | f.Decimal |
                         f.Round('0.25') | f.Min(-12) | f.Max(14)
        },
        allow_extra_keys=False,
        allow_missing_keys=False,
    )

    runner = f.FilterRunner(schema, request.body)

    if runner.is_valid():
        return HttpResponse(
            as_json(runner.cleaned_data),
            content_type='application/json',
        )
    else:
        return HttpResponseBadRequest(
            as_json(runner.errors),
            content_type='application/json',
        )


@csrf_exempt
def ingest_full_payload(request: HttpRequest) -> HttpResponse:
    """
    Using filters to validate the entire example payload.
    """
    schema = NonEmptyString | f.JsonDecode | f.Type(dict) | f.FilterMapper(
        {
            'applicantInfoModule': f.Required | ApplicantInfoModule,
            'feedbackModule': f.Required | FeedbackModule,
            'locationModule': f.Required | LocationModule,
            'sessionPrefs': f.Required | SessionPrefs,
            'sessionUid': f.Required | Session,
            'tokensModule': f.Required | TokensModule,
            'userId': NonEmptyString | f.ext.Model(UserModel),
        },
        allow_extra_keys=False,
        allow_missing_keys=False,
    )

    runner = f.FilterRunner(schema, request.body)

    if runner.is_valid():
        return HttpResponse(
            as_json(runner.cleaned_data),
            content_type='application/json',
        )
    else:
        return HttpResponseBadRequest(
            as_json(runner.errors),
            content_type='application/json',
        )
