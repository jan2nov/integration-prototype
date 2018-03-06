# -*- coding: utf-8 -*-
"""Tests of the Processing Block Controller Service.

see: http://docs.celeryproject.org/en/latest/userguide/testing.html

run with pytest tests/test.py
"""

import pytest
from pytest import raises

from celery.exceptions import Retry

from unittest.mock import patch
from app.tasks import execute_processing_block
from app.workflow import Workflow


class TestExecuteProcessingBlock:

    @patch('app.tasks.Workflow.run')  # < patching Workflow in module
    def test_execute(self, run_workflow):
        config = {'id': 'sb-01', 'workflow': {'stages': [{}, {}]}}
        execute_processing_block(config)
        run_workflow.assert_called_with(config['workflow'])

