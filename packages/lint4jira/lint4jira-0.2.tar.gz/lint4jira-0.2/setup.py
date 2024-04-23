from setuptools import setup, find_packages

setup(
    name='lint4jira',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'jira',
        'requests',
        'argparse',
        'curses',
        'windows-curses; platform_system=="Windows"',
    ],
    entry_points={
        'console_scripts': [
            'lint4jira=lint4jira.lint4jira:main',
        ],
    },
    author='Alameddin Çelik',
    author_email='alameddinc@gmail.com',
    description='lint4jira is a calculator for Jira tasks or sprints health. ' \
                'It calculates the health of the tasks in a sprint or a single task in Jira.',
    license='MIT',
    keywords='jira health sprint task',
    url='https://github.com/alameddinc/lint4jira',

)