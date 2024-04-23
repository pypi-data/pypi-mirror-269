"""
Flask-PikaMQ
-------------

ADD RABBITMQ_URL TO FLASK CONFIG
"""

from setuptools import setup


setup(
    name="Flask-PikaRMQ",
    version="1.0.2",
    url="",
    license="BSD",
    author="Rasco Developers",
    author_email="rezahartono.rasco@gmail.com",
    description="This is Extension for RabbitMQ Microservice",
    long_description=__doc__,
    py_modules=["flask_pikarmq/__init__"],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=["Flask", "pika"],
    classifiers=[],
)
