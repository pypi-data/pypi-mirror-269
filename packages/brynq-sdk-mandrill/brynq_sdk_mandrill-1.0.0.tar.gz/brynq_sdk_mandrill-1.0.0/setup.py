from setuptools import setup


setup(
    name='brynq_sdk_mandrill',
    version='1.0.0',
    description='Mandrill wrapper from BrynQ',
    long_description='Mandrill wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.mandrill"],
    package_data={'brynq_sdk.mandrill': ['templates/*']},
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
        'mandrill-really-maintained>=1,<=2'
    ],
    zip_safe=False,
)