#!/usr/bin/env python

from distutils.core import setup

setup(
    name="pid_optimization",
    version="0.0.0",
    description="Auto-Tuning PID Library",
    author="Formlabs",
    author_email="mikhail.hyde@formlabs.com",
    url="https://github.com/Formlabs/mordor/tree/master/python/lib",
    packages= [
        "dsp",
        "optimizers",
        "project_manager"
    ]
)
