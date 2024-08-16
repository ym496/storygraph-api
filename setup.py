from setuptools import setup, find_packages

setup(
    name="storygraph-api",
    version="0.1.0",
    description="This package allows you to interact and fetch data from the StoryGraph website.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="ym496",
    author_email="yogendramishra2004@gmail.com",
    url="https://github.com/ym496/storygraph-api",
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'selenium',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["storygraph", "storygraph api", "api storygraph", "storygraph scraper"],
    python_requires='>=3.10',
)
