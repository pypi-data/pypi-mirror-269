from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

import aws_cdk._jsii
import constructs._jsii

__jsii_assembly__ = jsii.JSIIAssembly.load(
    "bedrock-agents-cdk",
    "0.0.11",
    __name__[0:-6],
    "bedrock-agents-cdk@0.0.11.jsii.tgz",
)

__all__ = [
    "__jsii_assembly__",
]

publication.publish()
