from setuptools import setup, find_packages

setup(
    name='python_mpesa_koros',
    version='0.1.9',
    author='Kevin Ongulu',
    author_email='kevinongulu@gmail.com',
    description='A python package for connecting to MPESA APIs',
    #packages=find_packages(),
    packages = ['python_mpesa_koros'], 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'requests', #requests>=2.26.0
        'python-dotenv',
        'pycryptodome'
    ],
    python_requires='>=3.6',
)