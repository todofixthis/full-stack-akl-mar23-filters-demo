import json
from datetime import date

import filters as f
from dateutil.relativedelta import relativedelta
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from importer.filters import NonEmptyString


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
        return HttpResponse(b'OK', charset='utf-8', content_type='text/plain')
    else:
        return HttpResponseBadRequest(
            json.dumps(runner.errors),
            charset='utf-8',
            content_type='application/json',
        )
