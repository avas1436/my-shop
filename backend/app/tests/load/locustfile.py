from locust import HttpUser, between, events, task


class ApiUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # دریافت اکسس توکن
        response = self.client.post(
            "/api/v1/users/login/password",
            json={"phone_number": "09359733907", "password": "4430"},
        )

        # print("Login status code:", response.status_code)
        # print("Login response:", response.text)

        data = response.json()

        # جدا کردن توکن از پاسخ
        access_token = data["data"]["access_token"]

        # قرار دادن توکن در هدر
        self.client.headers = {"Authorization": f"Bearer {access_token}"}

    @task
    def get_me(self):
        self.client.get("/api/v1/users/me", name="GET /me")

    @task
    def health(self):
        self.client.get("/health", name="GET /health")


# پیام خروجی در زمان شروع و تمامی شدن تست
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("=== Test started ===")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("=== Test finished ===")
