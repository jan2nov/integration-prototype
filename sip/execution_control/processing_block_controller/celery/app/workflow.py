# -*- coding: utf-8 -*-
"""Module for handling execution of a Processing Block Workflow"""
import time


class Workflow:

    def __init__(self):
        """ """
        pass

    def run(self, config):
        """ """
        print('Executing workflow ...')
        for stage_config in config['stages']:
            self.run_stage(stage_config)

    @staticmethod
    def run_stage(config):
        """ """
        print('Executing workflow stage ...')
        time.sleep(0.5)
