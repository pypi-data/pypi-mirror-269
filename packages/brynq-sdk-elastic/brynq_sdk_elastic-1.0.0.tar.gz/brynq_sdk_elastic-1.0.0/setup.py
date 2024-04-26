from setuptools import setup


setup(
    name='brynq_sdk_elastic',
    version='1.0.0',
    description='elastic wrapper from BrynQ',
    long_description='elastic wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.elastic"],
    license='BrynQ License',
    install_requires=[
        'requests>=2,<=3',
        'paramiko>=2,<=3'
    ],
    zip_safe=False,
)
