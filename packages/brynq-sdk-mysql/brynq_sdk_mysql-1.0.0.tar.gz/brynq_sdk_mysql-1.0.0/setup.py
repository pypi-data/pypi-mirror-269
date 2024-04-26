from setuptools import setup


setup(
    name='brynq_sdk_mysql',
    version='1.0.0',
    description='MySQL wrapper from Bryn',
    long_description='MySQL wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.mysql"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
        'pandas>=1,<3',
        'pymysql>=1,<=2',
        'requests>=2,<=3',
        'cryptography>=38,<=38',
    ],
    zip_safe=False,
)