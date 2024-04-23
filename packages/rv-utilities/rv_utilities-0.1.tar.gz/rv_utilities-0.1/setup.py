from setuptools import setup, find_packages

setup(
    name="rv_utilities",
    version="0.1",
    packages=find_packages(),
    description="rv_utilities package",
    author="Robert",
    author_email="robert.valassi@accenture.com",
    license="MIT",
    include_package_data=True,
    package_data={},
    install_requires=[
        # Any dependencies
    ],
    python_requires='>=3.7',
)

