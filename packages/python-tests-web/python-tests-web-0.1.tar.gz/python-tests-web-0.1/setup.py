from setuptools import setup, find_packages 

setup(
    name='python-tests-web',
    version='0.1',
    description='A simple functional test library using Selenium and Chrome driver',
    author='Linda Lopez',
    packages=find_packages(),
    install_requires=[
        "allure-behave==2.13.4",
        "allure-python-commons==2.13.4",
        "behave==1.2.6",
        "behave-html-formatter==0.9.10",
        "behave2cucumber==1.0.3",
        "docxcompose==1.4.0",
        "docxtpl==0.16.8",
        "playwright==1.42.0",
        "psutil==5.9.2",
        "PyPDF2==3.0.1",
        "python-docx==1.1.0",
        "pycparser==2.21",
        "screeninfo==0.8",
        "selenium==4.1.3",
        "webdriver-manager==4.0.1",
        "webdrivermanager==0.10.0",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
    ],
)