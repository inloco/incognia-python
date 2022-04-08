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
    LOGIN_DECLINED: Final[str] = 'login_declined'
    VERIFIED: Final[str] = 'verified'
    IDENTITY_FRAUD: Final[str] = 'identity_fraud'
    ACCOUNT_TAKEOVER: Final[str] = 'account_takeover'
    CHARGEBACK_NOTIFICATION: Final[str] = 'chargeback_notification'
    CHARGEBACK: Final[str] = 'chargeback'
    MPOS_FRAUD: Final[str] = 'mpos_fraud'
    CHALLENGE_PASSED: Final[str] = 'challenge_passed'
    CHALLENGE_FAILED: Final[str] = 'challenge_failed'
    PASSWORD_CHANGED_SUCCESSFULLY: Final[str] = 'password_changed_successfully'
    PASSWORD_CHANGE_FAILED: Final[str] = 'password_change_failed'
    PROMOTION_ABUSE: Final[str] = 'promotion_abuse'
