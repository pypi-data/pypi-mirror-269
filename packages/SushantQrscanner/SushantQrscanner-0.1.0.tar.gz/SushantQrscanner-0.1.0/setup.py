from setuptools import setup, find_packages

setup(
    name='SushantQrscanner',
    version='0.1.0',
    author='Sushant',
    author_email='example@example.com',  # Placeholder email as actual email is not found
    packages=find_packages(),
    scripts=['readbc.py'],
    url='https://github.com/its-sushant/Qrscanner',
    description='An awesome QR code scanner.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "opencv-python >= 4.5.1.48",
        "pyzbar >= 0.1.8"
    ],
    classifiers=[  # Additional metadata
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify the Python version requirements
)
