from setuptools import setup, find_packages

setup(
    name='arshattendancelib',
    version='0.1.0',
    description='A library for tracking student attendance in Django applications',
    author='arsh',
    author_email='arshisinghsahota@gmail.com',
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
    keywords='django attendance library',
    packages=find_packages(),
    install_requires=[
        'Django>=2.1',
        # Add any other dependencies your library requires
    ],
    python_requires='>=3.7, <4',
)
