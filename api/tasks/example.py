# -*- coding:utf-8 -*-

from api.extensions import celery
from flask import current_app


@celery.task(queue="app_example_async")
def test_task():
    current_app.logger.info("test task.............................")
