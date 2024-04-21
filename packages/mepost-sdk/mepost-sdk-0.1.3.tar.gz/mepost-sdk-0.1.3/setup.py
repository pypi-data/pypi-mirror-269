from setuptools import setup, find_packages

setup(
    name='mepost-sdk',
    version='0.1.3',
    packages=find_packages(),
    description='A Python SDK for interacting with the Mepost API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='mepost',
    author_email='info@mepost.io',
    license='MIT',
    install_requires=[
        'requests'
    ],
    url='https://github.com/mepost-io/python-sdk',
    keywords='mepost, email, sdk, api',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
