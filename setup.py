from setuptools import setup

setup(
    name='interpreter',
    packages=['interpreter'],
    license='MIT',
    entry_points={
        'console_scripts': [
            'mmci=interpreter.interpret:main'
        ]
    },
    include_package_data=True,
    install_requires=['graphviz'],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
