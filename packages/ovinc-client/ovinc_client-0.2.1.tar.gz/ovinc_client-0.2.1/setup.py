#!/usr/bin/env python

from setuptools import setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ovinc_client",
    version="0.2.1",
    author="OVINC",
    url="https://www.ovinc.cn/",
    author_email="contact@ovinc.cn",
    description="A Tool for OVINC Union API",
    packages=[
        "ovinc_client",
        "ovinc_client.account",
        "ovinc_client.account.migrations",
        "ovinc_client.components",
        "ovinc_client.core",
        "ovinc_client.trace",
    ],
    install_requires=[
        "Django>=4.2.11,<5",
        "django_environ==0.10.0",
        "djangorestframework==3.14.0",
        "mysqlclient==2.1.1",
        "django-cors-headers==3.10.1",
        "pytz==2021.3",
        "django-sslserver==0.22",
        "pyOpenSSL==22.1.0",
        "django-simpleui==2023.8.28",
        "redis==4.5.4",
        "django-redis==5.2.0",
        "python_json_logger==2.0.4",
        "requests==2.31.0",
        "protobuf==3.19.5",
        "opentelemetry-api==1.24.0",
        "opentelemetry-sdk==1.24.0",
        "opentelemetry-exporter-jaeger==1.21.0",
        "opentelemetry-exporter-otlp==1.24.0",
        "opentelemetry-instrumentation==0.45b0",
        "opentelemetry-instrumentation-django==0.45b0",
        "opentelemetry-instrumentation-dbapi==0.45b0",
        "opentelemetry-instrumentation-redis==0.45b0",
        "opentelemetry-instrumentation-requests==0.45b0",
        "opentelemetry-instrumentation-celery==0.45b0",
        "opentelemetry-instrumentation-logging==0.45b0",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
