```shell
├── app.py                   # 应用程序的入口
├── config.py                # 配置文件
├── data/
│   ├── __init__.py
│   ├── repositories/        # 数据访问层
│   │   ├── __init__.py
│   │   ├── team_repository.py
│   │   ├── player_repository.py
│   │   └── ...（其他仓库）
├── models/                  # 模型层
│   ├── __init__.py
│   ├── base.py
│   ├── team.py
│   ├── player.py
│   ├── match.py
│   ├── hero.py
│   └── ...（其他模型）
├── services/                # 业务逻辑层
│   ├── __init__.py
│   ├── team_service.py
│   ├── player_service.py
│   └── ...（其他服务）
├── ui/                      # 用户界面层
│   ├── __init__.py
│   ├── main_window.py
│   ├── widgets/             # 界面小部件
│   │   ├── __init__.py
│   │   ├── team_management.py
│   │   ├── player_management.py
│   │   ├── match_management.py
│   │   └── ...（其他小部件）
│   ├── QSS/                 # 样式表文件
│   │   ├── dark_theme.qss
│   │   └── ...（其他样式表）
├── utils/                   # 实用工具层
│   ├── __init__.py
│   ├── db_utils.py
│   ├── logger.py
│   └── ...（其他工具）
```



# 项目框架说明

本次开发主要编程语言：python。

编程规范要求：尽量符合PEP8要求。具体要求符合《》

## 各层次详细说明

### 模型层（Models）

- 定义数据库模型，使用sqlalchemy orm映射到数据库表中。
- 每个模型对应数据库中的一张表。

### 数据访问层(Repositories)

- 封装对数据库的CRUD操作，提供数据访问接口。
- 每个实体都要对应的仓库类
- 与业务逻辑层解耦，便于更换数据源或修改数据库的实现。

### 业务逻辑层(Services)

- 处理应用程序的业务逻辑
- 每个实体都有对应的服务类
- 调用数据访问层的方法，封装业务逻辑，供UI层使用

### 用户界面层(UI)

- 提供图形用户界面，与用户进行交互
- 使用PyQt6进行构建页面，包括主窗口和各个功能模块的界面小部件
- 只处理界面和用户交互逻辑，不包含业务逻辑和数据访问

### 实用工具层(Utils)

- 提供通用的工具函数和配置管理
- 数据库链接、日志配置、配置文件加载等内容

