# ChatDocument

ChatDocument是一个易于使用的API包装器，用于将文件聊天功能连接到任何支持GPT的应用。

## 开始之前

请先到[AI Proxy](https://aiproxy.io/)注册账号，获取API key。请确保勾选管理权限，否则无法正常运行此项目。

![image](https://github.com/realnoob007/ChatDocument/assets/87698941/a52d29aa-ad6f-48fc-9603-831011918cd5)

## 安装

使用Docker运行：

```bash
git clone https://github.com/realnoob007/ChatDocument.git
docker build -t my-api .
docker run -p 3000:3000 my-api
```

你可以将第一个端口号修改为你可用的端口。运行后，访问`http://ip:端口`，打开文件上传网页。

## 使用

API端口为`http://ip:端口/v1/chat/completions`，你可以自行设置反代。

设置model为'chatdocument'。在文件上传网页上传后得到的文件URL写进system prompt里，请求格式与OpenAI一致。

## 贡献

欢迎提交pull request。

## 许可证

MIT
