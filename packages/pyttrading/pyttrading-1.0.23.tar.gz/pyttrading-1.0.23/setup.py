from setuptools import find_packages, setup

setup(
    name='pyttrading',
    packages=find_packages(),
    version='1.0.23',
    description='Trading Library',
    author='CannavIT',
    install_requires=[
        'pytest-runner',
        'stock-dataframe==0.1.0',
        'mlflow==2.9.2',
        'backtesting==0.3.3',
        'scipy==1.12.0',
        'Backtesting',
        'matplotlib==3.8.3',
        'plotly==5.19.0',
        'mlflow',
        'numba==0.59.0',
        'ta==0.11.0',
        'python-dotenv==1.0.1',
        'pydantic==2.6.2'
    ],
    tests_require=['pytest==4.4.2'],
    test_suite='tests',
    python_requires='>=3.6'
)

# pip uninstall -y pyttrading && python setup.py sdist && twine upload dist/* 

#! Caps Simulation
# {
#   "platformName": "iOS",
#   "appium:automationName": "XCUITest",
#   "appium:udid": "EA9AAE0F-118C-4F6E-9625-2A4B37B6CEE9"
# }