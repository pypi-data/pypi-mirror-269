"""Waylay Storage: apis."""

# import apis into api package
from .about_api import AboutApi
from .bucket_api import BucketApi
from .object_api import ObjectApi
from .subscription_api import SubscriptionApi

__all__ = [
    "AboutApi",
    "BucketApi",
    "ObjectApi",
    "SubscriptionApi",
]
