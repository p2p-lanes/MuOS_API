# Import all models here to ensure SQLAlchemy can set up relationships correctly
from app.api.access_tokens.models import AccessToken
from app.api.account_clusters.models import AccountClusterMember, ClusterJoinRequest
from app.api.achievements.models import Achievement
from app.api.applications.models import Application
from app.api.attendees.models import Attendee
from app.api.authorized_third_party_apps.models import AuthorizedThirdPartyApp
from app.api.check_in.models import CheckIn
from app.api.citizens.models import Citizen
from app.api.coupon_codes.models import CouponCode
from app.api.email_logs.models import EmailLog
from app.api.groups.models import Group
from app.api.organizations.models import Organization
from app.api.payments.models import Payment, PaymentProduct
from app.api.popup_city.models import PopUpCity
from app.api.products.models import Product
from app.api.world_builders.models import WorldBuilder

# Re-export all models
__all__ = [
    'AccountClusterMember',
    'AccessToken',
    'Achievement',
    'Application',
    'Attendee',
    'AuthorizedThirdPartyApp',
    'CheckIn',
    'Citizen',
    'ClusterJoinRequest',
    'CouponCode',
    'EmailLog',
    'Group',
    'Organization',
    'Payment',
    'PaymentProduct',
    'PopUpCity',
    'Product',
    'WorldBuilder',
]
