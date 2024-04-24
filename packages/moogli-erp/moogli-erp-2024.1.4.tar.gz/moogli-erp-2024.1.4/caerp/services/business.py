from sqlalchemy import select

from caerp.models.third_party import Customer
from caerp.models.task import Task
from .base import BaseService


class BusinessService(BaseService):
    def get_customer(self, business):
        customer_id_query = select(Task.customer_id).where(
            Task.business_id == business.id
        ).limit(1)
        query = select(Customer).where(
            Customer.id.in_(customer_id_query)
        )
        return self.dbsession.execute(query).fetchone()
    
    
