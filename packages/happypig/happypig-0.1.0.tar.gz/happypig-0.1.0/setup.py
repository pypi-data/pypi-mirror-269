from setuptools import find_packages
from setuptools import setup

def get_version():
    with open("src/happypig/VERSION.txt") as fr:
        version = fr.read().strip()
    return version

def get_long_description():
    with open("README.md") as f:
        long_description = f.read()
    return long_description

setup(
    name="happypig",
    version=get_version(),
    packages=find_packages("src"),
    package_dir={"": "src"},  # src layout 得这么写
    description="happypig",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="BuxianChen",
    author_email="541205605@qq.com",
    install_requires=["pandas"],  # 如果当前环境没有, 则从 PyPI 自动安装
    setup_requires=[],     # setuptools 本身的依赖项, 必须提前装好
    # tests_require=["pytest"],  # 执行 python setup.py test 时自动安装的依赖, 但现在由于 setup.py 的命令行用法均已被弃用, 且 python setup.py test 没有对应的 pip 替代命令
    # pip install .[tab] 会额外安装的一些包
    extras_require={
        "tab": ["tabulate"]
    },
    python_requires='>=3.7,<=3.12',
    include_package_data=True,  # 使用 MANIFEST.in + include_package_data=True
    # package_data={"happypig": ["data/*", "VERSION.txt"]},  # 也可以使用 package_data
    entry_points={
        "console_scripts": [
            "happypig=happypig.commands.main:main",
            "happypig-random=happypig.commands.random_main:random_main"
        ],
    }
)
