```shell
├── app.py                   # 应用程序入口
├── config.py                # 配置文件
├── models/                  # 数据模型定义
│   ├── __init__.py
│   ├── base.py
│   ├── hero.py
│   ├── player.py
│   ├── team.py
│   ├── match.py
│   ├── match_pick_ban.py
│   ├── player_match_stats.py
│   ├── team_player.py
├── repositories/	# 数据访问层
│   ├── __init__.py
│   ├── hero_repository.py
│   ├── player_repository.py
│   ├── team_repository.py
│   ├── match_repository.py
│   ├── match_pick_ban_repository.py
│   ├── player_match_stats_repository.py
│   ├── team_player_repository.py
├── services/                # 业务逻辑层
│   ├── __init__.py
│   ├── hero_service.py
│   ├── player_service.py
│   ├── team_service.py
│   ├── match_service.py
│   ├── match_pick_ban_service.py
│   ├── player_match_stats_service.py
│   └── team_player_service.py
├── ui/                      # 用户界面层
│   ├── __init__.py
│   ├── main_window.py
│   ├── widgets/             # 界面小部件
│       ├── __init__.py
│       ├── team_management.py
│       ├── player_management.py
│       ├── match_management.py
│       └── ...（其他小部件）
│   ├── QSS/                 # 样式表文件
│       ├── dark_theme.qss
│       └── ...（其他样式表）
├── utils/                   # 实用工具层
│   ├── __init__.py
│   ├── db_utils.py
│   └── ...（其他工具）
└── tests/                   # 测试层
    ├── __init__.py
    ├── test_team.py
    └── ...（其他测试模块）
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

