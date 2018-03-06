# -*- coding: utf-8 -*-
"""Processing Block Controller (Celery worker)"""
import os

from celery import Celery
from .workflow import Workflow

APP = Celery('tasks',
             broker=os.getenv('CELERY_BROKER'),
             backend=os.getenv('CELERY_BACKEND'))


@APP.task(bind=True)
def execute_processing_block(self, config):
    """Execute a processing block.

    Args:
        config (dict): Processing Block Configuration.
    """
    print('Executing Processing Block, id = ', config['id'])

    workflow = Workflow()
    workflow.run(config['workflow'])
