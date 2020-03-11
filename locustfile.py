from locust import HttpLocust, TaskSet, task
from datetime import date, timedelta

class WebsiteTasks(TaskSet):
    
    @task
    def searchTicket(self):
        tomorrow = date.today() + timedelta(days=1)
        data = { "startingPlace": "Shang Hai",
                 "endPlace": "Su Zhou",
                 "departureTime": str(tomorrow)}
        url = "/api/v1/travelservice/trips/left"
        self.client.post(url, json=data)
        
class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 50
    max_wait = 50
