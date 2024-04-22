# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['q_searcher']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'q-searcher',
    'version': '0.0.3',
    'description': '',
    'long_description': '# 量化的时序函数包\n\n投研团队自用包，出问题了请提 Issue、修复后请关闭 Issue。\n\n## 功能列表\n\n### 初始化\n\n- `td_init_run(configs=None)`：初始化包\n- `td_db_connect()`：获取一个数据库连接\n\n### A 股\n\n#### 股票\n\n1. ~~获取所有指数（股票市场、当前有效的）: get_all_index~~\n2. 获取所有股票（默认：当前有效的）: td_all_security\n3. ~~获取标的的最新信息（股票市场、不包含未来）: get_data~~\n4. ~~获取龙虎榜股票列表: get_dragon_tiger_list~~\n\n## Code/Style Linter\n\n我们使用 [Ruff](https://github.com/astral-sh/ruff) 作为代码检查器，请在提交前使用以下命令，确保 PR 的顺利进行：\n\n- `ruff check .`\n- `ruff format .`\n\n## 打包\n\n1. 更新 [pyproject.toml](pyproject.toml) 文件\n2. 执行 `./build.sh`\n3. 输入 API token\n\n旧的打包方式：\n\n1. 更新 [pyproject.toml](pyproject.toml) 文件\n2. 执行 `python -m build`\n3. 执行 `python -m twine upload dist/*`\n4. 对输入框，输入账号: `__token__` 并回车\n5. 最后输入 API token 即可\n\n## 测试\n\n需要运行自动化测试？\n\n- `poetry run pytest`\n\n如果你希望使用 Poetry 提供的虚拟机制，也需要本地提示。试试这个：\n\n1. 执行 `python -m build`\n2. 本地安装包 `pip install dist [package-...-any.whl]`\n',
    'author': 'UioSun',
    'author_email': 'uiosun@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
