"""
Flask-PikaMQ
-------------

ADD RABBITMQ_URL TO FLASK CONFIG
"""

from setuptools import setup


setup(
    name="Flask-PikaRMQ",
    version="1.0",
    url="",
    license="BSD",
    author="Rasco Developers",
    author_email="rezahartono.rasco@gmail.com",
    description="This is Extension for RabbitMQ Microservice",
    long_description=__doc__,
    py_modules=["flask_pikarmq/flask_pikarmq"],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=["Flask", "pika"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
