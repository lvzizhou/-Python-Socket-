# 基于 Python Socket 的网络服务与故障诊断平台设计与实现

一个使用 Python 标准库编写的网络编程课程设计。浏览器控制真实 Socket 实验，完成 TCP 文件传输、UDP 应答、DNS 查询、并发连接和六种故障诊断。无需虚拟机，无第三方 Python 依赖。

## 快速运行

安装 Python 3.10 或更新版本（安装时勾选 Add Python to PATH），下载仓库 ZIP 并解压。在包含 README.md 的文件夹地址栏输入 `cmd`，回车后执行：

```sh
python -m socketlab
```

浏览器会打开 http://127.0.0.1:8080 。选择场景，点击“启动真实实验”。也可双击 `启动平台.bat`。关闭时在命令窗口按 Ctrl+C。

```sh
python -m socketlab --batch
python -m unittest discover -s tests -v
```

第一条运行全部场景并输出 results/batch.json；第二条运行自动化测试。端口占用时关闭其他本项目进程。网页端口可用 `--port 8088` 修改。

## 编程实现

- `socketlab/core.py`：原始 TCP/UDP Socket、标准 DNS A 报文、并发服务端、故障注入、客户端和基于观测的诊断。
- `socketlab/__main__.py`：本地 HTTP 控制接口、参数检查、实验串行保护及 JSON 持久化。
- `docs/`：前端控制台，支持真实调用、导入导出及开发时实测记录。
- `tests/`：全部场景、恢复、10 客户端并发、分段接收、提前断开、超长报文测试。

TCP 应用协议使用 4 字节网络字节序长度头加消息体。客户端先发送 JSON 下载请求，服务端依次发送 JSON 元数据和 1 MiB 二进制数据；客户端循环 recv，处理 TCP 无消息边界问题，验证字节数及 SHA-256。UDP 请求携带序号和会话标识，客户端设置超时并统计应答。DNS 使用真实标准 A 查询，非 JSON 模拟解析。

## 六种故障

|场景|注入方式|观测诊断|
|---|---|---|
|F1 TCP 停服|关闭 TCP 监听|TCP_UNAVAILABLE|
|F2 响应延迟|应用等待 350 ms|RESPONSE_DELAY|
|F3 UDP 丢包|服务端丢弃奇数序号|UDP_LOSS|
|F4 错误 DNS|返回 127.0.0.2|DNS_MISMATCH|
|F5 内容损坏|修改首字节|FILE_CORRUPTED|
|F6 复合故障|DNS 错误 + TCP 停服|同时报告两种问题|

每轮实验独立重建服务；运行正常场景可验证恢复。诊断根据证据生成，不读取注入场景标签。TCP 失败只能证明端点不可达，不能仅靠它断言路由或防火墙故障。350 ms 是应用响应延迟；UDP 丢弃是应用模拟；SHA-256 演示应用完整性检查，不等同于 TCP 校验和。

## 展示与部署

GitHub Pages 发布 docs 静态页面，可查看实测样本、导入 JSON。浏览器网页不能直接使用 Python Socket；真实实验必须在本机启动后端。不要把静态站点展示误写为云端运行 Python。Packet Tracer 不再是本项目的必要组件。

[小白操作手册](docs/guide.md) · [设计及报告提纲](docs/design.md)

旧版项目内容已替换；旧提交仍在 Git 历史里，以便恢复。本版本实测记录由当前代码生成，未沿用旧版抓包。
