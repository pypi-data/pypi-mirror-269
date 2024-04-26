from setuptools import setup, find_packages

setup(
    name="opencti_excel_uploader",
    version="0.1",
    packages=find_packages(),
    description="Uploader for cases and reports from Excel files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="asz,jjk,eby",
    author_email="rnd@stratc.org",
    license="MIT",
    install_requires=[
        "pycti>=6.0.9,<7.0.0",
        "pandas>=2.2.2,<3.0.0",
        "openpyxl>=3.1.2,<4.0.0",
        "python-dotenv>=1.0.1,<2.0.0",
        "urllib3>=2.2.1,<3.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
