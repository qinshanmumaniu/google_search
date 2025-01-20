# Google搜索采集器

一个现代化的Google搜索URL采集工具，使用CustomTkinter构建精美的深色主题图形界面，支持批量获取搜索结果并导出为CSV文件。

![image](C:\Users\32398\Desktop\github_tool\google_search\image.png)

## 功能特点

- 现代化深色主题界面，美观易用
- 支持自定义API密钥和搜索引擎ID
- 支持自定义搜索页数范围
- 实时显示搜索结果
- 进度条显示搜索进度
- 支持导出搜索结果为CSV/TXT文件
- 多线程搜索，界面响应流畅
- 智能延迟功能，防止请求过快
- 支持随时停止采集过程
- 一键清空搜索结果
- 自动保存配置信息

## 系统要求

- Python 3.6+
- customtkinter
- requests

## 安装依赖

```bash
pip install customtkinter requests
```

## 使用说明

1. 配置Google Custom Search API
   - 在程序界面填入你的 Google API Key
   - 填入你的搜索引擎ID (CX)

2. 运行程序
   ```bash
   python google_search.py
   ```

3. 使用方法
   - 填写API配置信息
   - 输入搜索关键词
   - 设置起始和结束页码
   - 点击"开始搜索"按钮开始采集
   - 可随时点击"停止采集"中断搜索
   - 使用"清空结果"重置搜索结果
   - 点击"导出结果"保存为CSV或TXT文件

## 界面功能

- 现代化深色主题设计
- 简洁清晰的布局
- 实时进度显示
- 直观的操作按钮：
  - 开始搜索：启动搜索过程
  - 停止采集：随时中断当前搜索
  - 清空结果：一键清除当前结果
  - 导出结果：保存搜索结果到文件
- 可滚动的结果显示区域

## 注意事项

- 需要有效的Google Custom Search API密钥
- 请遵守Google API的使用限制
- 建议适当设置搜索页数，避免超出配额
- 导出支持CSV和TXT格式
- 配置信息会自动保存，下次启动自动加载

## 更新日志

### v1.0
- 新增停止采集功能
- 新增清空结果功能
- 优化按钮状态管理
- 改进搜索进度显示
- 完善错误处理机制

