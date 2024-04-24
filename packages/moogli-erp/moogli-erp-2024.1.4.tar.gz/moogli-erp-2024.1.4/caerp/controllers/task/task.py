import logging
import datetime
from typing import Type

from sqlalchemy import desc

from caerp.controllers.base import BaseController
from caerp.models.config import Config
from caerp.models.progress_invoicing import ProgressInvoicingPlan
from caerp.models.price_study import PriceStudy, PriceStudyChapter
from caerp.models.task import Task

logger = logging.getLogger(__name__)


class TaskController(BaseController):
    def create(self, customer, data: dict, no_price_study: bool = False) -> Task:
        instance = self._new_instance(customer, data)
        if not no_price_study and instance.project.project_type.price_study_default():
            logger.debug("   + Adding Price study to {}".format(instance))
            self.set_price_study(instance)

        self.set_display_ttc(instance)
        self.set_display_units(instance)
        return instance

    def _new_instance(self, customer, data):
        for key in ["company", "project", "business_type_id"]:
            assert key in data
        # On s'assure que l'info est bien dans les data
        data["customer"] = customer

        factory = self.get_customer_task_factory(customer)
        logger.debug("  + Creating task of type {} for {}".format(factory, customer))
        instance = factory(**data)
        # On gère les données relatives à l'affaire
        self._set_business_data(instance)
        # On gère les données relatives au type d'affaire
        # Initialise les indicateurs (fichiers requis, mentions)
        instance.initialize_business_type_data()

        self.dbsession.add(instance)
        self.dbsession.flush()

        if "decimal_to_display" not in data:
            instance.decimal_to_display = instance.company.decimal_to_display
        return instance

    def _set_business_data(self, instance):
        instance.update_indicators()

    def get_customer_task_factory(self, customer) -> Type[Task]:
        return Task

    def set_display_units(self, task: Task):
        """
        Set last display_units value used by the company
        :return: number
        """
        default = Config.get_value("task_display_units_default")
        query = self.dbsession.query(Task.display_units)
        query = query.filter(Task.company_id == task.company_id)
        query = query.filter(Task.id != task.id)
        query = query.order_by(desc(Task.id)).limit(1)
        last_display_units = query.scalar()
        if last_display_units in (0, 1):
            default = last_display_units
        task.display_units = default

    def set_display_ttc(self, task: Task):
        """
        Set last display_ttc value used by the company
        :return: number
        """
        default = Config.get_value("task_display_ttc_default")
        query = self.dbsession.query(Task.display_ttc)
        query = query.filter(Task.company_id == task.company_id)
        query = query.filter(Task.id != task.id)
        query = query.order_by(desc(Task.id)).limit(1)
        last_display_ttc = query.scalar()
        if last_display_ttc in (0, 1):
            default = last_display_ttc
        task.display_ttc = default

    def set_price_study(self, task):
        """
        Initialize a price study using the task's current datas
        """
        if task.price_study is None:
            self._clean_task(task)
            price_study = PriceStudy(
                general_overhead=task.company.general_overhead,
                task=task,
            )
            chapter = PriceStudyChapter()
            price_study.chapters.append(chapter)

            self.dbsession.add(price_study)
            self.dbsession.flush()
            price_study.sync_with_task(self.request)

        return task.price_study

    def _clean_task(self, task):
        """
        Remove the price study and ensure the task has the appropriate line groups
        """
        logger.debug("Cleaning the task")
        # On vide la task avant d'ajouter une étude de prix
        for group in task.line_groups:
            self.dbsession.delete(group)
        task.line_groups = []

        for discount in task.discounts:
            self.dbsession.delete(discount)
        task.discounts = []

        task.expenses_ht = 0
        self.dbsession.merge(task)
        self.dbsession.flush()

    def unset_price_study(self, task):
        """
        Remove the price study and ensure the task has the appropriate line groups
        """
        self.dbsession.delete(task.price_study)
        if len(task.line_groups) == 0:
            task.add_default_task_line_group()
        self.cache_totals(task)
        self.dbsession.merge(task)

    def cache_totals(self, task_obj):
        """Cache the totals of a task"""
        logger.debug("TaskService.cache_totals()")

        task_obj.ht = task_obj.total_ht()
        logger.debug(
            f" + Setting TTC {task_obj.tva} TVA : {task_obj.tva} HT : {task_obj.ht}"
        )
        task_obj.tva = task_obj.tva_amount()
        task_obj.ttc = task_obj.total()
        task_obj.updated_at = datetime.datetime.now()

        self.dbsession.merge(task_obj)

    def set_progress_invoicing_plan(self, task):
        """
        Initialize a price study using the task's current datas
        """
        task.invoicing_mode = task.PROGRESS_MODE
        self.dbsession.merge(task)
        if task.progress_invoicing_plan is None:
            self._clean_task(task)
            progress_invoicing_plan = ProgressInvoicingPlan(
                business=task.business,
                task=task,
            )
            self.dbsession.add(progress_invoicing_plan)
            self.dbsession.flush()
        return task.progress_invoicing_plan

    def unset_progress_invoicing_plan(self, task):
        """
        Remove the price study and ensure the task has the appropriate line groups
        """
        self.dbsession.delete(task.progress_invoicing_plan)
        if len(task.line_groups) == 0:
            task.add_default_task_line_group()
        self.cache_totals(task)
        self.dbsession.merge(task)
