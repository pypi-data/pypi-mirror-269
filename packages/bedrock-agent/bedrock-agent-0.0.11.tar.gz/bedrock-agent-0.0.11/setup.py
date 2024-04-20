import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "bedrock-agent",
    "version": "0.0.11",
    "description": "bedrock-agents-cdk",
    "license": "Apache-2.0",
    "url": "https://github.com/maxtybar/bedrock-agents-cdk.git",
    "long_description_content_type": "text/markdown",
    "author": "Max Tybar<maxtybar@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/maxtybar/bedrock-agents-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "bedrock_agent",
        "bedrock_agent._jsii"
    ],
    "package_data": {
        "bedrock_agent._jsii": [
            "bedrock-agents-cdk@0.0.11.jsii.tgz"
        ],
        "bedrock_agent": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.109.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.97.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
