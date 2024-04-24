from caerp.controllers.task.task import TaskController
from caerp.models.task import Estimation, InternalEstimation
from caerp.services.business import BusinessService


class EstimationController(TaskController):
    def create(self, customer, data: dict, no_price_study: bool = False):
        estimation: Estimation = super().create(customer, data, no_price_study)
        estimation.add_default_payment_line()
        estimation.set_default_validity_duration()
        return estimation

    def cache_totals(self, task_obj):
        result = super().cache_totals(task_obj)
        task_obj.update_payment_lines(self.request)
        return result

    def get_customer_task_factory(self, customer):
        if customer.is_internal():
            factory = InternalEstimation
        else:
            factory = Estimation
        return factory

