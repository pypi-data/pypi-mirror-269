import datetime

from caerp.controllers.task.task import TaskController
from caerp.models.task import (
    Invoice,
    InternalInvoice,
    CancelInvoice,
    InternalCancelInvoice,
)


class InvoiceController(TaskController):
    def create(self, customer, data: dict, no_price_study: bool = False):
        invoice: Invoice = super().create(customer, data, no_price_study)
        invoice.financial_year = datetime.date.today().year
        return invoice

    def _set_business_data(self, invoice):
        # Une facture a forcément une affaire associée
        if not invoice.business and not invoice.business_id:
            invoice.gen_business()

        return super()._set_business_data(invoice)

    def get_customer_task_factory(self, customer):
        if customer.is_internal():
            factory = InternalInvoice
        else:
            factory = Invoice
        return factory


class CancelInvoiceController(TaskController):
    def get_customer_task_factory(self, customer):
        if customer.is_internal():
            factory = InternalCancelInvoice
        else:
            factory = CancelInvoice
        return factory
