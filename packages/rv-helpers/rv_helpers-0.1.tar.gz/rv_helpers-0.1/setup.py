from setuptools import setup, find_packages

setup(
    name="rv_helpers",
    version="0.1",
    packages=find_packages(),
    description="rv_helpers package",
    author="Robert",
    author_email="robert.valassi@accenture.com",
    license="MIT",
    include_package_data=True,
    package_data={'helpers':['./rv_helpers/data/zb_vstore *.json']},
    install_requires=[
        # Any dependencies
    ],
    python_requires='>=3.7',
)

