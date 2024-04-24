# hebill.pypi

## 应用
快速打包上传到pypi

## 示例
```python
import hebill


pypi = hebill.pypi.Pypi(hebill)
pypi.pack(True, True)
```

## setup.py
```python
from setuptools import setup, find_packages

setup(
    name='your_package_name',
    version='0.1',
    packages=find_packages(),
    # 包含 Markdown 文件
    package_data={
        '': ['*.md'],  # 包含所有 Markdown 文件
        # 或者指定特定的目录下的 Markdown 文件
        # 'docs': ['*.md'], 
    },
    # 其他设置...
)

```