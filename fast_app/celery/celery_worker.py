import os
import time
from celery import Celery
from fastapi import Body

from fast_app.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from fast_app.scraper.scraper import AutoRiaScraper

celery = Celery(__name__)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND


@celery.task(name="start_scraper")
def start_scraper():
    scraper = AutoRiaScraper()
    scraper.main()
