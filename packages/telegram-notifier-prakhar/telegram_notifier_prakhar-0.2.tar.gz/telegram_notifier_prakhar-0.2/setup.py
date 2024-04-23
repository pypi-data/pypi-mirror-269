from setuptools import setup, find_packages


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='telegram_notifier_prakhar',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Prakhar Shrivas',
    author_email='prakharshrivas17@example.com',
    description='A simple library to send Telegram notifition when your code is completed .',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='telegram bot message notify',
)
