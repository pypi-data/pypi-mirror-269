from setuptools import setup, find_packages

setup(
    name='PetsisDevUtils',
    version='0.1',
    description='A short description of your package',
    long_description='A longer description of your package',
    author='PetsisDev', 
    author_email='petsis_dev@proton.me',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
    install_requires=[],
)
