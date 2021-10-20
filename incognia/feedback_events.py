from typing import Final

FeedbackEventType = str


class FeedbackEvents:
    SIGNUP_ACCEPTED: Final[FeedbackEventType] = 'signup_accepted'
    SIGNUP_DECLINED: Final[FeedbackEventType] = 'signup_declined'
    PAYMENT_ACCEPTED: Final[FeedbackEventType] = 'payment_accepted'
    PAYMENT_ACCEPTED_BY_THIRD_PARTY: Final[FeedbackEventType] = 'payment_accepted_by_third_party'
    PAYMENT_DECLINED: Final[FeedbackEventType] = 'payment_declined'
    PAYMENT_DECLINED_BY_RISK_ANALYSIS: Final[FeedbackEventType] = \
        'payment_declined_by_risk_analysis'
    PAYMENT_DECLINED_BY_MANUAL_REVIEW: Final[FeedbackEventType] = \
        'payment_declined_by_manual_review'
    PAYMENT_DECLINED_BY_BUSINESS: Final[FeedbackEventType] = 'payment_declined_by_business'
    PAYMENT_DECLINED_BY_ACQUIRER: Final[FeedbackEventType] = 'payment_declined_by_acquirer'
    LOGIN_ACCEPTED: Final[FeedbackEventType] = 'login_accepted'
    LOGIN_DECLINED: Final[FeedbackEventType] = 'login_declined'
    VERIFIED: Final[FeedbackEventType] = 'verified'
    IDENTITY_FRAUD: Final[FeedbackEventType] = 'identity_fraud'
    ACCOUNT_TAKEOVER: Final[FeedbackEventType] = 'account_takeover'
    CHARGEBACK: Final[FeedbackEventType] = 'chargeback'
    MPOS_FRAUD: Final[FeedbackEventType] = 'mpos_fraud'
