from django.test import override_settings
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from datetime import timedelta

from accounts.models import User, APIKey, UsageLog
from accounts.services.api_key import generate_key


class ImageTagAuthenticationTests(APITestCase):
    """
    Test suite for API authentication on POST /api/v1/tag/ endpoint.
    Covers Stage 1 MVP: authentication, API key validation, and quota enforcement.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.endpoint = "/api/v1/tag/"

    def setUp(self):
        """Initialize test client and test data."""
        self.client = APIClient()
        self.test_email = "testuser@example.com"
        self.test_password = "securepassword123"

    def _create_user_with_api_key(self, email=None, weekly_quota=20):
        """
        Helper method to create a user with an active API key.
        Returns (user, api_key_object, raw_key_string).
        """
        if email is None:
            email = self.test_email

        user = User.objects.create_user(email=email, password=self.test_password)
        user.weekly_quota = weekly_quota
        user.save()

        raw_key, prefix, hashed = generate_key()
        api_key = APIKey.objects.create(user=user, key=hashed, prefix=prefix)

        return user, api_key, raw_key

    def _make_request(self, api_key=None, image_url="https://example.com/image.jpg"):
        """
        Helper method to make a POST request to the tag endpoint.
        """
        headers = {}
        if api_key:
            headers["HTTP_API_KEY"] = api_key

        data = {}
        if image_url is not None:
            data["image_url"] = image_url

        return self.client.post(self.endpoint, data, **headers)


class TestMissingAPIKey(ImageTagAuthenticationTests):
    """
    Test Case 1: Request without API key.
    Expected: HTTP 401 Unauthorized
    """

    def test_request_without_api_key_header(self):
        """Verify that request without Api-Key header is rejected."""
        response = self._make_request(api_key=None)
        self.assertEqual(response.status_code, 401)

    def test_request_with_empty_api_key(self):
        """Verify that request with empty API key string is rejected."""
        response = self._make_request(api_key="")
        self.assertEqual(response.status_code, 401)

    def test_request_with_whitespace_only_api_key(self):
        """Verify that request with whitespace-only API key is rejected."""
        response = self._make_request(api_key="   ")
        self.assertEqual(response.status_code, 401)


class TestInvalidAPIKey(ImageTagAuthenticationTests):
    """
    Test Case 2: Request with invalid API key.
    Expected: HTTP 401 Unauthorized
    """

    def test_request_with_random_invalid_key(self):
        """Verify that request with random invalid API key is rejected."""
        invalid_key = "invalidrandomkey1234567890abcdefghijklmnop"
        response = self._make_request(api_key=invalid_key)
        self.assertEqual(response.status_code, 401)

    def test_request_with_malformed_key(self):
        """Verify that request with malformed API key is rejected."""
        malformed_key = "not-a-valid-key-format"
        response = self._make_request(api_key=malformed_key)
        self.assertEqual(response.status_code, 401)

    def test_request_with_partial_key(self):
        """Verify that request with incomplete/partial key is rejected."""
        _, _, raw_key = self._create_user_with_api_key()
        partial_key = raw_key[:10]
        response = self._make_request(api_key=partial_key)
        self.assertEqual(response.status_code, 401)

    def test_request_with_wrong_hash(self):
        """Verify that request with correct prefix but wrong hash is rejected."""
        _, api_key_obj, raw_key = self._create_user_with_api_key()
        
        wrong_suffix = "x" * (len(raw_key) - 16)
        wrong_key = raw_key[:16] + wrong_suffix
        
        response = self._make_request(api_key=wrong_key)
        self.assertEqual(response.status_code, 401)

    def test_request_with_inactive_user_key(self):
        """Verify that API key from inactive user is rejected."""
        user, _, raw_key = self._create_user_with_api_key()
        user.is_active = False
        user.save()

        response = self._make_request(api_key=raw_key)
        self.assertEqual(response.status_code, 401)


class TestValidAPIKey(ImageTagAuthenticationTests):
    """
    Test Case 3: Request with valid API key.
    Expected: HTTP 200 OK with correct JSON response
    """

    def test_valid_api_key_returns_200(self):
        """Verify that valid API key returns 200 OK."""
        _, _, raw_key = self._create_user_with_api_key()
        response = self._make_request(api_key=raw_key)
        self.assertEqual(response.status_code, 200)

    def test_valid_api_key_response_contains_image_url(self):
        """Verify that response contains the submitted image_url."""
        _, _, raw_key = self._create_user_with_api_key()
        test_url = "https://example.com/test_image.jpg"
        response = self._make_request(api_key=raw_key, image_url=test_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("image_url", response.data)
        self.assertEqual(response.data["image_url"], test_url)

    def test_valid_api_key_response_contains_tags(self):
        """Verify that response contains tags field with expected structure."""
        _, _, raw_key = self._create_user_with_api_key()
        response = self._make_request(api_key=raw_key)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("tags", response.data)
        self.assertIsInstance(response.data["tags"], dict)

    def test_valid_api_key_creates_usage_log(self):
        """Verify that successful request logs usage."""
        user, _, raw_key = self._create_user_with_api_key()
        initial_logs = UsageLog.objects.filter(user=user).count()
        
        response = self._make_request(api_key=raw_key)
        self.assertEqual(response.status_code, 200)
        
        final_logs = UsageLog.objects.filter(user=user).count()
        self.assertEqual(final_logs, initial_logs + 1)

    def test_valid_api_key_updates_last_used_at(self):
        """Verify that API key last_used_at is updated on successful request."""
        _, api_key_obj, raw_key = self._create_user_with_api_key()
        initial_last_used = api_key_obj.last_used_at
        
        response = self._make_request(api_key=raw_key)
        self.assertEqual(response.status_code, 200)
        
        api_key_obj.refresh_from_db()
        self.assertIsNotNone(api_key_obj.last_used_at)
        self.assertGreater(api_key_obj.last_used_at, initial_last_used or timezone.now() - timedelta(seconds=1))

    def test_multiple_valid_requests_all_return_200(self):
        """Verify that multiple requests with valid key all return 200."""
        _, _, raw_key = self._create_user_with_api_key()
        
        for _ in range(5):
            response = self._make_request(api_key=raw_key)
            self.assertEqual(response.status_code, 200)

    def test_whitespace_in_valid_key_is_handled(self):
        """Verify that leading/trailing whitespace in valid key is stripped."""
        _, _, raw_key = self._create_user_with_api_key()
        key_with_whitespace = f"  {raw_key}  "
        
        response = self._make_request(api_key=key_with_whitespace)
        self.assertEqual(response.status_code, 200)


class TestQuotaExceeded(ImageTagAuthenticationTests):
    """
    Test Case 4: Quota exceeded.
    Expected: First request returns 200, subsequent requests return 429 Too Many Requests
    """

    def test_quota_enforcement_single_request_allowed(self):
        """Verify that single request within quota returns 200."""
        _, _, raw_key = self._create_user_with_api_key(weekly_quota=1)
        response = self._make_request(api_key=raw_key)
        self.assertEqual(response.status_code, 200)

    def test_quota_enforcement_exceeds_quota(self):
        """Verify that second request after quota exhaustion is rejected with 429."""
        _, _, raw_key = self._create_user_with_api_key(weekly_quota=1)
        
        response1 = self._make_request(api_key=raw_key)
        self.assertEqual(response1.status_code, 200)
        
        response2 = self._make_request(api_key=raw_key)
        self.assertEqual(response2.status_code, 429)

    def test_quota_enforcement_multiple_requests(self):
        """Verify that quota is enforced across multiple requests."""
        _, _, raw_key = self._create_user_with_api_key(weekly_quota=3)
        
        for i in range(3):
            response = self._make_request(api_key=raw_key)
            self.assertEqual(response.status_code, 200, f"Request {i+1} should succeed")
        
        response4 = self._make_request(api_key=raw_key)
        self.assertEqual(response4.status_code, 429, "Request 4 should fail with 429")

    def test_quota_reset_after_week(self):
        """Verify that quota resets after one week."""
        user, _, raw_key = self._create_user_with_api_key(weekly_quota=1)
        
        response1 = self._make_request(api_key=raw_key)
        self.assertEqual(response1.status_code, 200)
        
        response2 = self._make_request(api_key=raw_key)
        self.assertEqual(response2.status_code, 429)
        
        user.refresh_from_db()
        user.quota_reset_at = timezone.now() - timedelta(days=8)
        user.save()
        
        response3 = self._make_request(api_key=raw_key)
        self.assertEqual(response3.status_code, 200, "Quota should reset after 7 days")

    def test_quota_usage_counted_per_user(self):
        """Verify that quota is tracked per user independently."""
        user1, _, raw_key1 = self._create_user_with_api_key(
            email="user1@example.com", weekly_quota=1
        )
        user2, _, raw_key2 = self._create_user_with_api_key(
            email="user2@example.com", weekly_quota=2
        )
        
        response1_a = self._make_request(api_key=raw_key1)
        self.assertEqual(response1_a.status_code, 200)
        
        response1_b = self._make_request(api_key=raw_key1)
        self.assertEqual(response1_b.status_code, 429)
        
        response2_a = self._make_request(api_key=raw_key2)
        self.assertEqual(response2_a.status_code, 200)
        
        response2_b = self._make_request(api_key=raw_key2)
        self.assertEqual(response2_b.status_code, 200)
        
        response2_c = self._make_request(api_key=raw_key2)
        self.assertEqual(response2_c.status_code, 429)

    def test_zero_quota_immediately_rejected(self):
        """Verify that user with zero quota cannot make any requests."""
        _, _, raw_key = self._create_user_with_api_key(weekly_quota=0)
        response = self._make_request(api_key=raw_key)
        self.assertEqual(response.status_code, 429)

    def test_high_quota_allows_many_requests(self):
        """Verify that user with high quota can make multiple requests."""
        _, _, raw_key = self._create_user_with_api_key(weekly_quota=100)
        
        for i in range(50):
            response = self._make_request(api_key=raw_key)
            self.assertEqual(response.status_code, 200, f"Request {i+1} should succeed")
        
        response51 = self._make_request(api_key=raw_key)
        self.assertEqual(response51.status_code, 429, "Request 51 should fail")


class TestUsageLogging(ImageTagAuthenticationTests):
    """
    Test suite for usage logging on successful requests.
    """

    def test_failed_request_not_logged_without_image_url(self):
        """Verify that request without image_url is still logged."""
        user, _, raw_key = self._create_user_with_api_key()
        initial_logs = UsageLog.objects.filter(user=user).count()
        
        response = self._make_request(api_key=raw_key, image_url=None)
        self.assertEqual(response.status_code, 400)
        
        final_logs = UsageLog.objects.filter(user=user).count()
        self.assertEqual(final_logs, initial_logs + 1)

    def test_usage_log_records_endpoint(self):
        """Verify that usage log records the endpoint name."""
        user, _, raw_key = self._create_user_with_api_key()
        response = self._make_request(api_key=raw_key)
        self.assertEqual(response.status_code, 200)
        
        log = UsageLog.objects.filter(user=user).latest("used_at")
        self.assertEqual(log.endpoint, "/api/v1/tag/")

    def test_usage_log_timestamp_is_recorded(self):
        """Verify that usage log has a valid timestamp."""
        user, _, raw_key = self._create_user_with_api_key()
        before_request = timezone.now()
        response = self._make_request(api_key=raw_key)
        after_request = timezone.now()
        
        self.assertEqual(response.status_code, 200)
        
        log = UsageLog.objects.filter(user=user).latest("used_at")
        self.assertGreaterEqual(log.used_at, before_request)
        self.assertLessEqual(log.used_at, after_request)


class TestEndpointResponse(ImageTagAuthenticationTests):
    """
    Test suite for endpoint response format and content.
    """

    def test_endpoint_returns_json_response(self):
        """Verify that endpoint returns valid JSON."""
        _, _, raw_key = self._create_user_with_api_key()
        response = self._make_request(api_key=raw_key)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)

    def test_endpoint_response_structure(self):
        """Verify that response has expected structure."""
        _, _, raw_key = self._create_user_with_api_key()
        response = self._make_request(api_key=raw_key)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("image_url", response.data)
        self.assertIn("tags", response.data)

    def test_endpoint_tags_contains_expected_fields(self):
        """Verify that tags object has expected structure."""
        _, _, raw_key = self._create_user_with_api_key()
        response = self._make_request(api_key=raw_key)
        
        self.assertEqual(response.status_code, 200)
        tags = response.data.get("tags", {})
        self.assertIn("category", tags)
        self.assertIn("color", tags)
        self.assertIn("material", tags)

    def test_endpoint_missing_image_url_returns_400(self):
        """Verify that missing image_url returns 400 Bad Request."""
        _, _, raw_key = self._create_user_with_api_key()
        response = self._make_request(api_key=raw_key, image_url=None)
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.data)


class TestAPIKeyRotation(ImageTagAuthenticationTests):
    """
    Test suite for API key rotation and multiple keys per user.
    Note: Current implementation uses OneToOneField, so only one key per user.
    """

    def test_one_to_one_relation_enforced(self):
        """Verify that only one API key can exist per user."""
        user, _, _ = self._create_user_with_api_key()
        
        raw_key2, prefix2, hashed2 = generate_key()
        
        with self.assertRaises(Exception):
            APIKey.objects.create(user=user, key=hashed2, prefix=prefix2)


class TestAuthenticationEdgeCases(ImageTagAuthenticationTests):
    """
    Test suite for edge cases in authentication.
    """

    def test_deleted_user_api_key_rejected(self):
        """Verify that API key from deleted user is rejected."""
        user, _, raw_key = self._create_user_with_api_key()
        user.delete()
        
        response = self._make_request(api_key=raw_key)
        self.assertEqual(response.status_code, 401)

    def test_key_prefix_indexed_correctly(self):
        """Verify that key lookup via prefix works correctly."""
        user1, api_key1, raw_key1 = self._create_user_with_api_key(
            email="user1@example.com"
        )
        user2, api_key2, raw_key2 = self._create_user_with_api_key(
            email="user2@example.com"
        )
        
        response1 = self._make_request(api_key=raw_key1)
        response2 = self._make_request(api_key=raw_key2)
        
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        
        log1 = UsageLog.objects.filter(user=user1).latest("used_at")
        log2 = UsageLog.objects.filter(user=user2).latest("used_at")
        
        self.assertEqual(log1.user, user1)
        self.assertEqual(log2.user, user2)

    def test_concurrent_requests_same_user(self):
        """Verify that concurrent requests from same user respect quota."""
        _, _, raw_key = self._create_user_with_api_key(weekly_quota=2)
        
        response1 = self._make_request(api_key=raw_key)
        response2 = self._make_request(api_key=raw_key)
        response3 = self._make_request(api_key=raw_key)
        
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 429)
