# README 模板库

## 前端项目模板

### React 项目
```markdown
# [项目名称]

[项目简短描述]

## 🚀 功能特性
- 功能1：描述
- 功能2：描述
- 功能3：描述

## 📦 安装

```bash
# 克隆仓库
git clone [仓库地址]
cd [项目目录]

# 安装依赖
npm install
# 或
yarn install
# 或
pnpm install
```

## 🎯 使用

```bash
# 开发模式
npm run dev

# 构建生产版本
npm run build

# 运行测试
npm test
```

## 🏗️ 项目结构

```
project/
├── public/           # 静态资源
├── src/             # 源代码
│   ├── components/  # React组件
│   ├── pages/       # 页面组件
│   ├── hooks/       # 自定义Hooks
│   ├── utils/       # 工具函数
│   ├── styles/      # 样式文件
│   └── App.jsx      # 主应用组件
├── package.json     # 依赖配置
└── README.md        # 项目说明
```

## ⚙️ 配置

### 环境变量
创建 `.env` 文件：
```env
REACT_APP_API_URL=http://localhost:3000
REACT_APP_ENV=development
```

## 🧪 测试

```bash
# 运行所有测试
npm test

# 运行测试并生成覆盖率报告
npm test -- --coverage
```

## 🤝 贡献

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📄 许可证

本项目基于 [许可证名称] 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情
```

### Vue 项目
```markdown
# [项目名称]

[项目简短描述]

## 功能特性
- 基于 Vue 3 的现代化前端应用
- 使用 Composition API
- 支持 TypeScript
- 响应式设计

## 快速开始

### 环境要求
- Node.js 16+
- npm 7+ 或 yarn 1.22+

### 安装
```bash
npm install
```

### 开发
```bash
npm run dev
```

### 构建
```bash
npm run build
```

## 项目结构
```
src/
├── assets/          # 静态资源
├── components/      # 组件
├── composables/     # 组合式函数
├── router/         # 路由配置
├── stores/         # 状态管理
├── views/          # 页面视图
├── App.vue         # 根组件
└── main.ts         # 入口文件
```

## 技术栈
- Vue 3
- Vue Router
- Pinia (状态管理)
- Vite (构建工具)
- TypeScript
- ESLint + Prettier
```

## 后端项目模板

### Node.js/Express 项目
```markdown
# [项目名称] API

RESTful API 服务

## 功能特性
- RESTful API 设计
- JWT 身份验证
- 数据库集成
- 错误处理中间件
- 请求验证

## 安装

```bash
npm install
```

## 配置

创建 `.env` 文件：
```env
PORT=3000
NODE_ENV=development
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
JWT_SECRET=your-secret-key
```

## 运行

```bash
# 开发模式
npm run dev

# 生产模式
npm start
```

## API 文档

### 认证
```
POST /api/auth/login
POST /api/auth/register
GET /api/auth/profile
```

### 用户管理
```
GET /api/users
GET /api/users/:id
PUT /api/users/:id
DELETE /api/users/:id
```

## 数据库迁移

```bash
# 创建迁移
npx knex migrate:make migration_name

# 运行迁移
npx knex migrate:latest

# 回滚迁移
npx knex migrate:rollback
```

## 测试

```bash
# 运行测试
npm test

# 运行测试并监视变化
npm run test:watch
```

## 部署

### Docker 部署
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "src/index.js"]
```
```

### Python Flask 项目
```markdown
# [项目名称] Flask API

Python Flask REST API

## 功能特性
- Flask RESTful API
- SQLAlchemy ORM
- JWT 认证
- Swagger 文档
- 单元测试

## 环境设置

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

## 运行

```bash
# 开发模式
flask run

# 或直接运行
python app.py
```

## 配置

创建 `.env` 文件：
```env
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db
SECRET_KEY=your-secret-key
```

## 项目结构
```
app/
├── __init__.py
├── models.py      # 数据模型
├── routes.py      # 路由定义
├── schemas.py     # 序列化模式
├── utils.py       # 工具函数
└── config.py      # 配置管理
```

## API 文档

访问 `http://localhost:5000/swagger` 查看 API 文档

## 测试

```bash
# 运行测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=app tests/
```

## 部署

### 使用 Gunicorn
```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```
```

## 全栈项目模板

### MERN 栈项目
```markdown
# [项目名称] - MERN 全栈应用

完整的 MERN (MongoDB, Express, React, Node.js) 应用

## 功能特性
- React 前端
- Express 后端 API
- MongoDB 数据库
- JWT 身份验证
- 响应式设计

## 项目结构
```
project/
├── client/         # React 前端
│   ├── public/
│   └── src/
├── server/         # Express 后端
│   ├── models/
│   ├── routes/
│   ├── middleware/
│   └── index.js
├── package.json    # 根 package.json
└── README.md
```

## 安装和运行

### 后端
```bash
cd server
npm install
npm start
```

### 前端
```bash
cd client
npm install
npm start
```

## 环境变量

### 后端 (.env)
```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/appdb
JWT_SECRET=your-secret-key
NODE_ENV=development
```

### 前端 (.env)
```env
REACT_APP_API_URL=http://localhost:5000/api
```

## API 端点
```
GET    /api/products     获取所有产品
POST   /api/products     创建新产品
GET    /api/products/:id 获取单个产品
PUT    /api/products/:id 更新产品
DELETE /api/products/:id 删除产品
```

## 数据库设置

```bash
# 启动 MongoDB
mongod

# 或使用 Docker
docker run -d -p 27017:27017 mongo
```

## 部署

### 后端部署
```bash
# 构建
cd server
npm run build

# 使用 PM2 运行
pm2 start dist/index.js --name "api-server"
```

### 前端部署
```bash
cd client
npm run build
# 将 build/ 目录部署到静态主机
```
```

## 工具库/包模板

### npm 包
```markdown
# [包名称]

[包描述]

## 安装

```bash
npm install [包名称]
# 或
yarn add [包名称]
```

## 使用

```javascript
import { functionName } from '[包名称]';

// 使用示例
const result = functionName(params);
```

## API 参考

### functionName(params)
描述函数功能

**参数：**
- `param1` (类型): 描述
- `param2` (类型): 描述

**返回值：**
类型 - 描述

**示例：**
```javascript
import { functionName } from '[包名称]';

const result = functionName({ key: 'value' });
console.log(result);
```

## 开发

### 本地开发
```bash
# 克隆仓库
git clone [仓库地址]
cd [包目录]

# 安装依赖
npm install

# 运行测试
npm test

# 构建
npm run build
```

### 发布新版本
```bash
# 更新版本号
npm version patch  # 或 minor, major

# 发布到 npm
npm publish
```

## 测试

```bash
# 运行测试
npm test

# 运行测试并监视变化
npm run test:watch

# 生成覆盖率报告
npm run test:coverage
```

## 贡献

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。

## 许可证

MIT © [作者名称]
```

### Python 包
```markdown
# [包名称]

[包描述]

## 安装

```bash
pip install [包名称]
```

## 使用

```python
from package_name import module_name

# 使用示例
result = module_name.function_name(params)
```

## 功能特性
- 功能1
- 功能2
- 功能3

## 快速开始

```python
import package_name

# 基本使用
package_name.do_something()

# 高级使用
config = package_name.Config(param=value)
result = config.process()
```

## API 文档

### 类 `ClassName`
类描述

**方法：**
- `method_name(params)`: 方法描述

**属性：**
- `property_name`: 属性描述

### 函数 `function_name(params)`
函数描述

**参数：**
- `param` (类型): 参数描述

**返回值：**
类型 - 返回值描述

## 开发

### 设置开发环境
```bash
# 克隆仓库
git clone [仓库地址]
cd [包目录]

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装开发依赖
pip install -e ".[dev]"
```

### 运行测试
```bash
pytest

# 运行测试并生成覆盖率报告
pytest --cov=package_name tests/
```

### 构建
```bash
# 构建分发包
python -m build

# 检查构建
twine check dist/*
```

## 发布

```bash
# 上传到 PyPI
twine upload dist/*
```

## 许可证

[许可证信息]
```

## 配置/脚本项目模板

### Docker 配置项目
```markdown
# [项目名称] Docker 配置

Docker 容器化配置

## 功能特性
- 多阶段构建
- 生产优化
- 健康检查
- 日志配置

## 使用

### 构建镜像
```bash
docker build -t image-name:tag .
```

### 运行容器
```bash
docker run -d -p 8080:80 --name container-name image-name:tag
```

### 查看日志
```bash
docker logs container-name
```

## Dockerfile 说明

```dockerfile
# 构建阶段
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 生产阶段
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 环境变量
```env
NODE_ENV=production
API_URL=https://api.example.com
```

## Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 部署

### 推送到 Docker Hub
```bash
docker tag image-name:tag username/image-name:tag
docker push username/image-name:tag
```

### 使用 Docker Compose 部署
```bash
docker-compose up -d
```

## 监控和日志

```bash
# 查看容器状态
docker ps

# 查看容器资源使用
docker stats

# 查看容器日志
docker logs -f container-name
```

## 故障排除

### 常见问题
1. **端口冲突**：检查端口是否被占用
2. **构建失败**：检查 Dockerfile 语法和依赖
3. **容器启动失败**：检查环境变量和卷挂载

### 调试命令
```bash
# 进入容器
docker exec -it container-name sh

# 检查容器配置
docker inspect container-name
```
```

## 通用模板元素

### 徽章部分
```markdown
![版本](https://img.shields.io/badge/version-1.0.0-blue)
![构建状态](https://img.shields.io/badge/build-passing-green)
![许可证](https://img.shields.io/badge/license-MIT-blue)
![下载量](https://img.shields.io/npm/dt/package-name)
```

### 贡献指南
```markdown
## 🤝 贡献指南

我们欢迎所有形式的贡献！请阅读以下指南：

### 开发流程
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 代码规范
- 遵循项目现有的代码风格
- 添加适当的注释
- 编写单元测试
- 更新相关文档

### 提交信息规范
使用约定式提交：
- `feat:` 新功能
- `fix:` 修复bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具变动
```

### 许可证部分
```markdown
## 📄 许可证

本项目基于 [许可证名称] 许可证发布 - 查看 [LICENSE](LICENSE) 文件了解详情。

### 第三方依赖
本项目使用了以下第三方库：
- [库名称](链接) - 许可证
- [库名称](链接) - 许可证

### 版权声明
版权所有 © [年份] [作者/组织名称]。保留所有权利。
```

## 模板选择指南

### 根据项目类型选择模板
1. **前端项目**：React/Vue/Angular/Svelte 模板
2. **后端项目**：Node.js/Python/Go 模板
3. **全栈项目**：MERN/MEAN 模板
4. **工具库**：npm包/Python包模板
5. **配置项目**：Docker/部署脚本模板

### 根据受众调整
1. **开发者**：详细的技术文档和API参考
2. **用户**：简单的安装和使用说明
3. **贡献者**：详细的开发指南和贡献流程
4. **部署人员**：部署配置和运维说明

### 根据项目阶段调整
1. **初期**：简单的快速开始指南
2. **成熟期**：完整的文档和API参考
3. **维护期**：更新日志和迁移指南