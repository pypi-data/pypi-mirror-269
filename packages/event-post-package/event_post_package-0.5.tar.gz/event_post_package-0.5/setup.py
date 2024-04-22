from setuptools import setup, find_packages

setup(
    name='event_post_package',
    version='0.5',
    packages=find_packages(),
    package_data={'event_post_package': ['templates/user/*.html','static/js/*.js','static/*.css']},
    install_requires=[
        'Django',
    ],
)