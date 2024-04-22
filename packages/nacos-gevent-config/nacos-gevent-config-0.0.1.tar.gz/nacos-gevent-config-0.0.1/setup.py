from setuptools import setup, find_packages

setup(
    name='nacos-gevent-config',
    version='0.0.1',
    author='Kane Kai Song',
    author_email='e1143097@u.nus.edu',
    description='This is a package for fetching config scheduled by gevent',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/test3625045/tunnel_insideimage',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    python_requires='>=3.7',
)
