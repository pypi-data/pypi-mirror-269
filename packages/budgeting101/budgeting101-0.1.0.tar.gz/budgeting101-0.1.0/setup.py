from setuptools import setup, find_packages

setup(
    name='budgeting101',  # Replace 'suggestions' with the name of your library
    version='0.1.0',  # Update the version number accordingly
    author='AliceRodgers',
    author_email='alicerodgers35@gmail.com',
    description='A library for providing budgeting suggestions',
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
    keywords='budgeting suggestions',
    python_requires='>=3.6',
    install_requires=[
        # Add any dependencies required by your library here
        'django',
        'weasyprint',
        # Add more dependencies as needed
    ],
)
