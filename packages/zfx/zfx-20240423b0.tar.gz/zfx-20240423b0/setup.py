from setuptools import setup, find_packages

setup(
    name='zfx',
    version='20240423B',
    packages=find_packages(),
    # 不包含其他文件
    include_package_data=False,
    # 作者信息等
    author='zengfengxiang',
    author_email='424491679@qq.com',
    description='自用',
    # 项目主页
    url='',
    # 依赖列表
    install_requires=[
        'requests',
        # 添加其他依赖库
    ],
)
