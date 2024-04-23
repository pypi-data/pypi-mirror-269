from setuptools import setup, find_packages

setup(
    name='telegram_notifier_prakhar',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Prakhar Shrivas',
    author_email='prakharshrivas17@example.com',
    description='A simple library to send Telegram messages.',
    keywords='telegram bot message notify',
)
