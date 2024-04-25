import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "gammarer.aws-daily-cloud-watch-logs-archive-stack",
    "version": "2.6.7",
    "description": "AWS CloudWatch Logs daily archive to s3 bucket",
    "license": "Apache-2.0",
    "url": "https://github.com/gammarer/aws-daily-cloud-watch-logs-archive-stack.git",
    "long_description_content_type": "text/markdown",
    "author": "yicr<yicr@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/gammarer/aws-daily-cloud-watch-logs-archive-stack.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "gammarer.aws_daily_cloud_watch_logs_archive_stack",
        "gammarer.aws_daily_cloud_watch_logs_archive_stack._jsii"
    ],
    "package_data": {
        "gammarer.aws_daily_cloud_watch_logs_archive_stack._jsii": [
            "aws-daily-cloud-watch-logs-archive-stack@2.6.7.jsii.tgz"
        ],
        "gammarer.aws_daily_cloud_watch_logs_archive_stack": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.80.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "gammarer.aws-secure-bucket>=1.1.0, <1.2.0",
        "gammarer.aws-secure-log-bucket>=1.4.0, <1.5.0",
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
