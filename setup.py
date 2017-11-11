from setuptools import setup

setup(
    name='interpreter',
    packages=['interpreter'],
    include_package_data=True,
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
