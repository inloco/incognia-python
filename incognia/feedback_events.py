from typing import Final


class FeedbackEvents:
    SIGNUP_ACCEPTED: Final[str] = 'signup_accepted'
    SIGNUP_DECLINED: Final[str] = 'signup_declined'
    PAYMENT_ACCEPTED: Final[str] = 'payment_accepted'
    PAYMENT_ACCEPTED_BY_THIRD_PARTY: Final[str] = 'payment_accepted_by_third_party'
    PAYMENT_ACCEPTED_BY_CONTROL_GROUP: Final[str] = 'payment_accepted_by_control_group'
    PAYMENT_DECLINED: Final[str] = 'payment_declined'
    PAYMENT_DECLINED_BY_RISK_ANALYSIS: Final[str] = \
        'payment_declined_by_risk_analysis'
    PAYMENT_DECLINED_BY_MANUAL_REVIEW: Final[str] = \
        'payment_declined_by_manual_review'
    PAYMENT_DECLINED_BY_BUSINESS: Final[str] = 'payment_declined_by_business'
    PAYMENT_DECLINED_BY_ACQUIRER: Final[str] = 'payment_declined_by_acquirer'
    LOGIN_ACCEPTED: Final[str] = 'login_accepted'
    LOGIN_ACCEPTED_BY_DEVICE_VERIFICATION: Final[str] = 'login_accepted_by_device_verification'
    LOGIN_ACCEPTED_BY_FACIAL_BIOMETRICS: Final[str] = 'login_accepted_by_facial_biometrics'
    LOGIN_ACCEPTED_BY_MANUAL_REVIEW: Final[str] = 'login_accepted_by_manual_review'
    LOGIN_DECLINED: Final[str] = 'login_declined'
    ACCOUNT_ALLOWED: Final[str] = 'account_allowed'
    LOGIN_DECLINED_BY_FACIAL_BIOMETRICS: Final[str] = 'login_declined_by_facial_biometrics'
    LOGIN_DECLINED_BY_MANUAL_REVIEW: Final[str] = 'login_declined_by_manual_review'
    DEVICE_ALLOWED: Final[str] = 'device_allowed'
    VERIFIED: Final[str] = 'verified'
    IDENTITY_FRAUD: Final[str] = 'identity_fraud'
    ACCOUNT_TAKEOVER: Final[str] = 'account_takeover'
    CHARGEBACK_NOTIFICATION: Final[str] = 'chargeback_notification'
    CHARGEBACK: Final[str] = 'chargeback'
    PROMOTION_ABUSE: Final[str] = 'promotion_abuse'
    RESET: Final[str] = 'reset'
