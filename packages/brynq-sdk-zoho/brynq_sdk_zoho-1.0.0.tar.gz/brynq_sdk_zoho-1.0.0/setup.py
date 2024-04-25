from setuptools import setup

setup(
    name='brynq_sdk_zoho',
    version='1.0.0',
    description='ZOHO wrapper from BrynQ',
    long_description='ZOHO wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.zoho"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1'
    ],
    zip_safe=False,
)
