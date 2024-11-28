# 🚀 NGLSpammer v2.0

A high-performance asynchronous NGL message spammer with a beautiful minimal UI.

## 📊 Performance Analysis

```mermaid
graph TD
    subgraph Performance
    A[Start] --> B[Initialize]
    B --> C[Send Messages]
    C --> D[Rate Limiting]
    D --> E[Success/Fail]
    E --> C
    end
```

## 📈 Message Throughput

```mermaid
%%{init: {'theme': 'dark'}}%%
xychart-beta
    title "Messages per Second"
    x-axis [10, 50, 100, 500, 1000]
    y-axis "Messages/s" 0 --> 50
    line [45, 42, 40, 38, 35]
    style line stroke:cyan,stroke-width:2
```

## ✨ Features

- 🚄 **High Performance**: 35-45 messages per second
- 🔄 **Asynchronous**: Concurrent message sending
- 🎯 **Smart Rate Limiting**: Automatic retry with exponential backoff
- 🎨 **Minimal UI**: Clean design with real-time progress
- 🔒 **Advanced Bypass**: Dynamic device ID and header generation

## 📊 Performance Stats

```mermaid
%%{init: {'theme': 'dark'}}%%
pie
    title "Message Delivery Analysis"
    "Success" : 95
    "Failed" : 3
    "Rate Limited" : 2
```

## 🔥 Concurrency Impact

```mermaid
%%{init: {'theme': 'dark'}}%%
gantt
    title Concurrent Request Performance
    dateFormat X
    axisFormat %s
    
    section 50 Requests
    42 msg/s: 0, 42
    section 100 Requests
    40 msg/s: 0, 40
    section 500 Requests
    38 msg/s: 0, 38
    section 1000 Requests
    35 msg/s: 0, 35
```

## 🛠️ Installation

```bash
git clone https://github.com/MyTheeNa/nglspammer.git
cd nglspammer
pip install -r requirements.txt
```

## 📝 Requirements

- Python 3.7+
- aiohttp==3.8.5
- asyncio==3.4.3
- colorama==0.4.6
- tqdm==4.66.1

## 💻 Usage

```bash
python ngl_spammer.py
```

Follow the prompts to enter:
1. NGL username
2. Number of messages
3. Concurrency level (recommended: 50-100)

## 🎮 Demo Output

```
NGLSpammer v2.0

✓ 95/100 (95.0%)
✗ 5/100 (5.0%)
➤ ██████████████████████████████
⚡ Batch #4

Mission Complete

✓ Success: 95/100
✗ Failed : 5/100
⏱ Time   : 2.42s
⚡ Rate   : 41.24 msg/s
```

## ⚡ Performance Tips

- Optimal concurrency: 50-100 requests
- Recommended message count: <1000 per session
- Stable internet connection required
- Use proxies for better success rate

## ⚠️ Disclaimer

This tool is for educational purposes only. Use responsibly and in accordance with NGL's terms of service.

## 🔧 Technical Architecture

```mermaid
flowchart LR
    A[User Input] --> B[Async Engine]
    B --> C{Rate Limiter}
    C -->|Pass| D[Message Sender]
    C -->|Limit| E[Retry Handler]
    E --> B
    D --> F[Success]
    D --> G[Fail]
```

## 🤝 Contributing

Feel free to:
- Open issues
- Submit PRs
- Suggest improvements
- Report bugs

## 📜 License

MIT License - feel free to use and modify!
