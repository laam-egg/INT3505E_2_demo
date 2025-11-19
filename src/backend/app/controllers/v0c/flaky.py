from flask_restx import Namespace, Resource
from ...utils.circuit_breaker import circuit_breaker
import random

flaky_api = Namespace('flaky', 'Flaky API routes.')

class FlakyService:
    @circuit_breaker
    def get_flaky_data(self):
        coin_flip = random.randint(0, 1)  # Simulate flakiness
        if coin_flip == 0:
            raise Exception("Simulated failure/flakiness.")
        return {"message": "This is a flaky endpoint! It sometimes works, sometimes doesn't."}

@flaky_api.route("/")
class Flaky(Resource):
    service = FlakyService()

    def get(self):
        return self.service.get_flaky_data()
