from setuptools import setup, find_packages
import swarmauri_developer

setup(
    name='swarmauri_developer',
    version=swarmauri_developer.__version__,
    author='Jacob Stewart',
    author_email='corporate@swarmauri.com',
    description=swarmauri_developer.__short_desc__,
    long_description=swarmauri_developer.__long_desc__,
    long_description_content_type='text/markdown',
    url='http://github.com/swarmauri/developer_assistant',
    license='MIT', 
    packages=find_packages(include=['swarmauri_developer']),
    entry_points={
        'console_scripts': [
            'developer_assistant = swarmauri_developer.DeveloperAssistant:main',
        ]
    },
    include_package_data=True,
    install_requires=['swarmauri[full]==0.1.80'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10'
    ],
    python_requires='>=3.10',
    setup_requires=["wheel"]
)