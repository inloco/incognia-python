from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='incognia-python',
    version='1.1.0',
    packages=find_packages(exclude=['tests']),
    license='MIT',
    url='https://github.com/inloco/incognia-python',
    author='Incognia',
    author_email='incognia@incognia.com',
    description='Incognia API Python Client',
    python_requires='>=3.8',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
