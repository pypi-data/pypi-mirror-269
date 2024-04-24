"""Storage Service."""

from waylay.sdk import ApiClient, WaylayService

from ..api.about_api import AboutApi
from ..api.bucket_api import BucketApi
from ..api.object_api import ObjectApi
from ..api.subscription_api import SubscriptionApi


class StorageService(WaylayService):
    """Storage Service Class."""

    name = "storage"
    title = "Storage Service"

    about: AboutApi
    bucket: BucketApi
    object: ObjectApi
    subscription: SubscriptionApi

    def __init__(self, api_client: ApiClient):
        """Create the storage service."""

        super().__init__(api_client)
        self.about = AboutApi(api_client)
        self.bucket = BucketApi(api_client)
        self.object = ObjectApi(api_client)
        self.subscription = SubscriptionApi(api_client)
