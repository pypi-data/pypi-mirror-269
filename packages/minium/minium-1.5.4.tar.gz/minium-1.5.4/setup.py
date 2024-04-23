'''
Author: yopofeng
Date: 2023-10-06 17:50:32
LastEditors: yopofeng yopofeng@tencent.com
LastEditTime: 2024-04-11 11:32:49
FilePath: /py-minium/setup.py
Description: 

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
#!/usr/bin/env python3
import sys
import os

__version__ = "1.5.4"

from setuptools import setup, find_packages

# We do not support Python <3.8
if sys.version_info < (3, 8):
    print(
        "Unfortunately, your python version is not supported!\n"
        "Please upgrade at least to Python 3.8!",
        file=sys.stderr,
    )
    sys.exit(1)

requirements_path = "requirements.txt"
try:
    import pkg_resources
except ImportError:
    # websocket_client # 1.4.0后有个兼容报错
    with open(requirements_path, "r") as f:
        install_requires = f.read().split("\n")
else:
    with open(requirements_path, "r") as f:
        install_requires = [str(req) for req in pkg_resources.parse_requirements(f)]

entry_points = {
    "console_scripts": [
        "minitest=minium.framework.loader:main",
        "minidoctor=minium.framework.minidoctor:main",
        "miniruntest=minium.framework.loader:main",
        "minireport=minium.framework.report:main",
        "mininative=minium.native.nativeapp:start_server",
    ]
}

def find_data_files(pkg, directory):
    for root, dirs, files in os.walk(os.path.join(pkg, directory)):
        for filename in files:
            yield os.path.join(os.path.relpath(root, pkg), filename)

config_path = "miniprogram/base_driver/version.json"
package_data = {
    "minium": [
        config_path,
        requirements_path,
        *list(find_data_files("minium", "externlib")),
        *list(find_data_files("minium", "framework/dist")),
        *list(find_data_files("minium", "native")),
        *list(find_data_files("minium", "utils/js/min")),
        *list(find_data_files("minium", "utils/js/es5")),
    ]
}

exclude_package_data = {"": ["*pyc", "readme.md", "build.py", "__pycache__"]}
extras_require = {
    "ios": ["tidevice==0.12.0", "lxml", "nest_asyncio", "pymobiledevice3"],
}

long_description = """
install:
```
pip3 install minium
```
if you use ios devices, you can install with
```
pip3 install "minium[ios]"
```

See the [document](https://minitest.weixin.qq.com/#/minium/Python/readme) for details
"""

if __name__ == "__main__":
    setup(
        name="minium",
        version=__version__,
        license="MIT",
        url="https://minitest.weixin.qq.com/#/",
        packages=find_packages(),
        description="Minium is the best MiniProgram auto test framework.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        package_data=package_data,
        exclude_package_data=exclude_package_data,
        entry_points=entry_points,
        install_requires=install_requires,
        extras_require=extras_require,
        setup_requires=["setuptools"],
        python_requires=">=3.8",
        author="WeChat-Test",
        author_email="minitest@tencent.com",
        platforms=["MacOS", "Windows"],
        keywords=["minium", "WeApp", "MiniProgram", "Automation", "Test"],
    )
