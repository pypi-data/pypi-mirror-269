from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Langgraph quickstart package.'
LONG_DESCRIPTION = 'this package is a quickstart for langgraph.'

# Setting up
setup(
    name="AvaxiaLLM",
    version=VERSION,
    author="Avaxia-Group",
    author_email="<yan.seiji.nishiyama@avaxia-group.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'fastapi==0.110.1',
         'langchain-openai==0.1.1',
          'langgraph==0.0.32',
           'langchain==0.1.14',
           'uvicorn==0.29.0',
           'unstructured',
           'grandalf',
           'matplotlib',
           'langchain-chroma',
           'msal'
    ],
    keywords=['python', 'ML', 'LLM', 'openai', 'langchain', 'langgraph'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)