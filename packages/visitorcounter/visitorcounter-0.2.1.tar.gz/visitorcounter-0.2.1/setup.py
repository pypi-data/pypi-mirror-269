from setuptools import setup, find_packages

setup(
    name='visitorcounter',
    version='0.2.1',
    packages=find_packages(),
    description='Vistor counter calculation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sandeep Reddy P ',
    author_email='sandeepreddy.pathakottu@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
)
