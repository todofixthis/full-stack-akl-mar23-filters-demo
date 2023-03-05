from datetime import date

import filters as f
from dateutil.relativedelta import relativedelta

from importer.models import Session as SessionModel


@f.filter_macro
def NonEmptyString():
    return f.Unicode | f.Strip | f.Required


@f.filter_macro
def ApplicantInfoModule():
    return f.Type(dict) | f.FilterMapper(
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


@f.filter_macro
def FeedbackModule():
    return f.Type(dict) | f.FilterMapper(
        {
            'note': f.Unicode | f.Strip,
            'starRating': NonEmptyString | f.Decimal | f.Min(0) | f.Max(5),
            'timings': f.Array | f.FilterRepeater(f.Required | f.Int),
        },
        allow_extra_keys=False,
        allow_missing_keys=False,
    )


@f.filter_macro
def LocationModule():
    return f.Type(dict) | f.FilterMapper(
        {
            'deviceGps': f.Required | f.Type(dict) | f.FilterMapper(
                {
                    'lat': NonEmptyString | f.Decimal | f.Min(-90) | f.Max(90),
                    'lon': NonEmptyString | f.Decimal | f.Min(0) | f.Max(180),
                },
                allow_extra_keys=False,
                allow_missing_keys=False,
            ),
            'city': NonEmptyString,
            'country': f.ext.Country(),
        },
        allow_extra_keys=False,
        allow_missing_keys=False,
    )


@f.filter_macro
def MarketingOptIn():
    return f.Type(dict) | f.FilterMapper(
        {
            "dev": f.Type(bool) | f.Optional(default=False),
            "nl": f.Type(bool) | f.Optional(default=False),
            "res": f.Type(bool) | f.Optional(default=False),
        },
        allow_missing_keys=True,
        allow_extra_keys=False,
    )


@f.filter_macro
def SessionPrefs():
    return f.Type(dict) | f.FilterMapper(
        {
            'language':
                f.Array | f.MinLength(1) |
                f.FilterRepeater(NonEmptyString | f.ext.Locale),
            'marketingOptIn': f.FilterRepeater(MarketingOptIn),
            'orientLandscape': f.Type(bool),
        },
        allow_extra_keys=False,
        allow_missing_keys=False,
    )


@f.filter_macro
def Session():
    return NonEmptyString | f.Uuid(version=4) | \
        f.ext.Model(SessionModel, 'session_key')


@f.filter_macro
def TokensModule():
    return f.Type(dict) | f.FilterMapper(
        {
            'honestyQuot': NonEmptyString | f.Decimal | f.Min(0) | f.Max(1),
            'timePrefQuot': NonEmptyString | f.Decimal | f.Min(0) | f.Max(1),
            'timings': f.Array | f.FilterRepeater(f.Required | f.Int),
        }
    )
