import base64

from locust import HttpLocust, TaskSet, task
from random import randint, choice

USER_CREDENTIALS = [
    ("user", "password"),
    ("user1", "password"),
    ("user2", "password"),
    ("user3", "password"),
    ("user4", "password"),
    ("user5", "password"),
    ("user6", "password"),
    ("user7", "password"),
    ("user8", "password"),
    ("user9", "password"),
    ("user10", "password"),
    ("user11", "password"),
    ("user12", "password"),
    ("user13", "password"),
    ("user14", "password"),
    ("user15", "password"),
    ("user16", "password"),
    ("user17", "password"),
    ("user18", "password"),
    ("user19", "password"),
    ("user20", "password"),
    ("user21", "password"),
    ("user22", "password"),
    ("user23", "password"),
    ("user24", "password"),
]


class UserTasks(TaskSet):

    def on_start(self):
        if len(USER_CREDENTIALS) > 0:
            user, passw = USER_CREDENTIALS.pop()
            base64string = base64.encodestring('%s:%s' % (user, passw)).replace('\n', '')
            self.client.get("/")
            response = self.client.get("/login", headers={"Authorization":"Basic %s" % base64string})
            print "Response status code:", response.status_code , user
            if response.status_code != 200:
                response = self.client.post("/register", json={"username": user, "password": passw, "email": "", "firstName": "", "lastName": ""})
                response = self.client.post("/cards", json={"longNum": "1111222233334444", "expires": "09/2020", "ccv": "123"})
                response = self.client.post("/addresses", json={"number": "246", "street": "Whitelees Road", "city": "Glasgow","postcode": "G67 3DL", "country": "United Kingdom"})
                
    @task
    def home(self):
        self.client.get("/")
        
    @task
    def category(self):
        catalogue = self.client.get("/catalogue").json()
        category_item = choice(catalogue)
        item_id = category_item["id"]
        self.client.get("/detail.html?id={}".format(item_id))

    @task
    def addToCarts(self):
        catalogue = self.client.get("/catalogue").json()
        category_item = choice(catalogue)
        item_id = category_item["id"]
        self.client.get("/category.html")
        self.client.get("/detail.html?id={}".format(item_id))
        self.client.delete("/cart")
        self.client.post("/cart", json={"id": item_id, "quantity": 1})
        self.client.get("/basket.html")
        self.client.post("/orders")

    @task
    def carts(self):
        self.client.get("/basket.html")
            
    @task
    def orders(self):
        self.client.post("/orders")

    @task
    def customerOrders(self):
        self.client.get("/customer-orders.html")

    def my_success_handler(request_type, name, response_time, response_length, **kw):
        print "Successfully fetched: %s" % (name)

class Web(HttpLocust):
    task_set = UserTasks
    min_wait = 100
    max_wait = 200
