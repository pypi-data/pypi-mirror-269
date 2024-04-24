import logging
from typing import Optional, Union

from caerp.controllers.base import BaseController
from caerp.controllers.task.invoice import InvoiceController
from caerp.controllers.task.estimation import EstimationController
from caerp.services.business import BusinessService
from caerp.models.user import User
from caerp.models.project import Business, BusinessPaymentDeadline
from caerp.models.task import Task, Estimation, Invoice, CancelInvoice


logger = logging.getLogger(__name__)


class BusinessController(BaseController):
    def _create_deposit_deadline(self, business, estimation):
        """
        Create a deadline for the deposit in the business

        :param obj business: The Business instance
        :param obj estimation: The Estimation instance
        :returns: The Business instance
        :rtype: obj
        """
        deposit = estimation.deposit
        if not deposit:
            return None

        query = self.dbsession.query(BusinessPaymentDeadline)
        query = query.filter_by(business_id=business.id)
        query = query.filter_by(estimation_id=estimation.id)
        query = query.filter_by(deposit=True)
        if query.count() == 0:
            deadline = BusinessPaymentDeadline(
                business_id=business.id,
                estimation_id=estimation.id,
                deposit=True,
                date=estimation.date,
                amount=estimation.deposit_amount_ttc(),
                order=0,
                description="Acompte à la commande",
            )

            self.dbsession.add(deadline)
            self.dbsession.flush()
            return deadline
        return None

    def _create_business_deadline(self, business, payment_line, estimation, order):
        """
        Create a deadline for the payment in the business

        :param obj business: The Business instance
        :param obj payment_line: The PaymentLine instance
        :param obj estimation: The Estimation instance
        :returns: The Business instance
        :rtype: obj
        """
        from caerp.models.project.business import BusinessPaymentDeadline

        query = (
            self.dbsession.query(BusinessPaymentDeadline)
            .filter(BusinessPaymentDeadline.business_id == business.id)
            .filter(BusinessPaymentDeadline.estimation_id == estimation.id)
            .filter(BusinessPaymentDeadline.estimation_payment_id == payment_line.id)
        )
        deadline = None
        if query.count() == 0:
            deadline = BusinessPaymentDeadline(
                payment_line=payment_line,
                description=payment_line.description,
                date=payment_line.date,
                amount=payment_line.amount,
                estimation=estimation,
                order=order,
            )
            self.dbsession.add(deadline)
            self.dbsession.flush()
        return deadline

    def populate_deadlines(self, business, estimation=None):
        """
        Populate the business deadlines with those described in the associated
        estimation(s)

        :param obj business: The Business instance
        :param obj estimation: Optionnal Estimation instance
        :returns: The Business instance
        :rtype: obj
        """
        logger.debug("Populating deadlines for the business {}".format(business.id))
        if estimation is not None:
            estimations = [estimation]
        else:
            estimations = business.estimations

        order = 0
        deadlines = []
        for estimation in estimations:
            deadline = self._create_deposit_deadline(business, estimation)
            if deadline is not None:
                order += 1
                deadlines.append(deadline)
            for payment_line in estimation.payment_lines:
                deadlines.append(
                    self._create_business_deadline(
                        business, payment_line, estimation, order
                    )
                )
                order += 1

        self.dbsession.merge(business)
        return deadlines

    def gen_business_from_task(self, task: Task) -> Business:
        """
        Generate a business from the given task
        """
        business = Business(
            name=task.name,
            business_type_id=task.business_type_id,
            project=task.project,
        )

        if task.project.project_type.with_business:
            business.visible = True

        self.dbsession.add(business)
        self.dbsession.flush()
        task.business_id = business.id
        self.dbsession.merge(task)
        self.dbsession.flush()
        return business

    def gen_business_from_estimation(self, estimation: Estimation) -> Business:
        """
        Generate a business from the given estimation
        """
        business = self.gen_business_from_task(estimation)
        if estimation.deposit or len(estimation.payment_lines) > 1:
            business.visible = True
            self.dbsession.merge(business)
            self.dbsession.flush()
        self.populate_deadlines(business, estimation)
        business.populate_indicators()
        return business

    def gen_business_from_invoice(
        request, invoice: Union[Invoice, CancelInvoice]
    ) -> Business:
        """
        Generate a business from the given invoice
        """
        business = self.gen_business_from_task(invoice)
        business.populate_indicators()
        return business

    def gen_invoice(
        self,
        user: User,
        business: Business,
        payment_deadline: Optional[BusinessPaymentDeadline] = None,
    ) -> Invoice:
        if payment_deadline is None:
            payment_deadline = business.payment_deadlines[0]

        estimation = payment_deadline.estimation
        if payment_deadline.deposit:
            invoice = estimation.gen_deposit_invoice(self.request, user)
        else:
            invoice = estimation.gen_invoice(
                self.request, payment_deadline.payment_line, user
            )
        payment_deadline.invoice_id = invoice.id
        self.dbsession.merge(payment_deadline)
        self.dbsession.flush()
        return invoice

    def add_estimation_to_business(self, business, user):
        service = BusinessService(self.request)
        customer = service.get_customer(business)
        data = dict(
            user=user,
            company=business.project.company,
            project=business.project,
            business_id=business.id,
            business_type_id=business.business_type_id,
        )
        controller = EstimationController(self.request)
        estimation = controller.create(customer, data)
        if business.invoicing_mode == business.PROGRESS_MODE:
            pass

        self.dbsession.merge(estimation)
        self.dbsession.flush()
        return estimation
