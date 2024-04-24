# 安装包

```bash
pip install wheel twine
```

# 生成分发档案

在包的根目录下（即 `setup.py` 所在的目录），运行以下命令来生成分发档案。

```bash
python setup.py sdist bdist_wheel
```

# 上传你的包

```bash
twine upload dist/*
```
