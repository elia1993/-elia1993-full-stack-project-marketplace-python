from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):

    @task(1)
    def login(self):
        self.client.get("/login")

    @task(2)
    def register(self):
        self.client.get("/register")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)

if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py --host=http://192.168.1.179:5001")
