from setuptools import setup, find_packages

setup(
    name='meerkatio',
    version='1.12',
    packages=find_packages(),
    package_data={'meerkat': ['ping_sounds/*.mp3']},
    include_package_data=True,
    install_requires=[
        "requests",
        "click",
        "typing_extensions==4.11.0",
        "ipython"
    ],
    entry_points='''
        [console_scripts]
        meerkat=meerkat.cli:meerkat
    ''',
    author="MeerkatIO",
    description="Personal notification and debug tool for multi-tasking software developers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license=open("LICENSE").read(),
    keywords=["notification", "alerting", "personal", "productivity", "big data"],
    url="https://meerkatio.com"
)
