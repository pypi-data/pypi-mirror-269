# py-pkg-template

## desc

description

## 发布

1. 生成项目包 `python setup.py sdist bdist_wheel`
2. 上传包 `python -m twine upload dist/*`
<!-- 3. `python -m twine upload --repository-url https://pypi.org/legacy/ dist/*` -->

> 上传时使用 `API tokens` 可以保存在 `$HOME/.pypirc` 就不用每次都输入了

## 文档

- 打包和分发项目: <https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/>
- 官方:<https://packaging.python.org/en/latest/guides/section-build-and-publish/>
