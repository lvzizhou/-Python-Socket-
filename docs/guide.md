# 从零操作手册

## 一、启动

1. 在 GitHub 仓库点击绿色 Code → Download ZIP，解压全部文件。
2. 安装 Python 3.10+，勾选 Add Python to PATH。已安装则无需重复安装。
3. 打开解压后包含 README.md、socketlab 文件夹的位置。
4. 在资源管理器地址栏输入 cmd 后回车。
5. 输入 `python -m socketlab`，回车，保留命令窗口。
6. 浏览器应打开 http://127.0.0.1:8080 ，右上角显示“本地后端已连接”。
7. 如果 python 不可用，尝试 `py -m socketlab`；不要直接双击 core.py。

## 二、正常实验

选择“正常通信”，并发数填 3，点击“启动真实实验”。预期通信正常、文件 1048576 字节、完整性通过、UDP 8/8、并发成功 3/3。耗时和速率随机器变化。截图保留页面诊断、指标和详情。

## 三、六个故障

逐个选择 F1 到 F6，每次点击按钮，阅读诊断和“原始观测数据”，下载 JSON 并截图。

- F1：DNS 正常，但正确 IP 直连也失败。
- F2：文件依然通过校验，完整传输耗时通常大于 350 ms；这不是丢包证据。
- F3：UDP 8 发 4 收，50% 应答缺失；TCP 正常。
- F4：DNS 为 127.0.0.2，正确 IP 直连正常，域名地址连接失败。
- F5：TCP 传输成功且长度正常，SHA-256 失败。
- F6：同时出现 DNS_MISMATCH 和 TCP_UNAVAILABLE。查看 DNS 与 direct_tcp 两组证据。

每个故障之后再运行“正常通信”，保留恢复截图。程序自动配置故障，不需要修改 Windows 网卡或防火墙。实验结束后服务保持最后一轮状态，下一轮自动重建。

## 四、Wireshark 取证（可选但建议）

1. 打开 Wireshark，选择 Adapter for loopback traffic capture / Npcap Loopback Adapter。
2. 开始抓包，再到网页运行一轮实验。
3. 显示过滤器填 `tcp.port == 19090 || udp.port == 19091 || udp.port == 15353`。
4. 正常 TCP：查看 SYN、SYN/ACK、ACK，右键相关包 → Follow → TCP Stream；文件为二进制内容。
5. UDP 丢包：过滤 `udp.port == 19091`，8 个请求，4 个应答。程序未应答不等于操作系统捕获丢失。
6. DNS：过滤 `udp.port == 15353`。非标准端口未识别时右键数据包 → Decode As → DNS。正常回答 127.0.0.1，错误场景回答 127.0.0.2。
7. F1：可观察连接被拒绝时的 RST；具体表现以实际系统抓包为准。
8. 停止，File → Save As 保存 pcapng。使用自己的截图和抓包写报告。

## 五、上传实验材料

程序结果保存在 results 文件夹，默认不提交自动生成数据。选取需要提交的 JSON 复制到自建 evidence 文件夹，连同截图、pcapng 和最终报告上传。不要将未完成的实验写成已验证。

## 六、答辩演示

先运行正常场景，解释 Socket 和长度前缀；运行 F3，展示 UDP 无应答；运行 F4，比较域名与直接 IP；运行 F5，解释应用校验；运行 F6，展示多故障识别；最后恢复正常。可再使用 Wireshark 核对报文。

GitHub 静态网页不能执行真实实验。现场展示请运行本地 Python 后端。无需 Packet Tracer 或虚拟机。
