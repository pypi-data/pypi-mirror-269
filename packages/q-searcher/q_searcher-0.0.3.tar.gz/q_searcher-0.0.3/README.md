# 量化的时序函数包

投研团队自用包，出问题了请提 Issue、修复后请关闭 Issue。

## 功能列表

### 初始化

- `td_init_run(configs=None)`：初始化包
- `td_db_connect()`：获取一个数据库连接

### A 股

#### 股票

1. ~~获取所有指数（股票市场、当前有效的）: get_all_index~~
2. 获取所有股票（默认：当前有效的）: td_all_security
3. ~~获取标的的最新信息（股票市场、不包含未来）: get_data~~
4. ~~获取龙虎榜股票列表: get_dragon_tiger_list~~

## Code/Style Linter

我们使用 [Ruff](https://github.com/astral-sh/ruff) 作为代码检查器，请在提交前使用以下命令，确保 PR 的顺利进行：

- `ruff check .`
- `ruff format .`

## 打包

1. 更新 [pyproject.toml](pyproject.toml) 文件
2. 执行 `./build.sh`
3. 输入 API token

旧的打包方式：

1. 更新 [pyproject.toml](pyproject.toml) 文件
2. 执行 `python -m build`
3. 执行 `python -m twine upload dist/*`
4. 对输入框，输入账号: `__token__` 并回车
5. 最后输入 API token 即可

## 测试

需要运行自动化测试？

- `poetry run pytest`

如果你希望使用 Poetry 提供的虚拟机制，也需要本地提示。试试这个：

1. 执行 `python -m build`
2. 本地安装包 `pip install dist [package-...-any.whl]`
