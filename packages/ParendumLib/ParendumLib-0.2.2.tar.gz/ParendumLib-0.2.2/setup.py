from setuptools import setup, find_packages

requirements = [
    "fastapi",
    "jinja2",
    "requests",
    "motor",
    "python-multipart",
    "fastapi-sessions"
]

setup(
    name='ParendumLib',
    version='0.2.2',
    packages=find_packages(),
    install_requires=requirements,
    author='Parendum',
    author_email='info@parendum.com',
    description='Parendum Official Library',
    keywords='logger',
)
