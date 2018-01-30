from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = ''.join(f.readlines())

setup(
    name='rpg_toolkit_server',
    version='0.1.dev0',
    description='A server for generic RPG support',
    long_description=long_description,
    author='Tomáš Drbota',
    author_email='argoneuscze@gmail.com',
    license='AGPL',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rpgtserver = server.__main__:main'
        ]
    },
    install_requires=[
        'websockets'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'pytest-asyncio'
    ],
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python :: 3'
        'Programming Language :: Python :: 3.5'
        'Programming Language :: Python :: 3.6'
        'Intended Audience :: End Users/Desktop'
    ]
)
