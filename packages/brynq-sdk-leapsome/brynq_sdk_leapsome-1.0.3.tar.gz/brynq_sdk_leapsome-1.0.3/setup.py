from setuptools import setup

setup(
    name='brynq_sdk_leapsome',
    version='1.0.3',
    description='Leapsome wrapper from BrynQ',
    long_description='Leapsome wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.leapsome"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
        'pandas>=2,<3',
        'openpyxl>=3,<4',
        'paramiko>=3,<4',
        'pysftp==0.2.9'
    ],
    zip_safe=False,
)
