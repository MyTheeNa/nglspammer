# 🚀 NGLSpammer v2.0

A high-performance asynchronous NGL message spammer with a beautiful minimal UI.

## 📊 Performance Analysis

```mermaid
graph TD
    style A fill:#2ecc71,stroke:#27ae60,stroke-width:2px
    style B fill:#3498db,stroke:#2980b9,stroke-width:2px
    style C fill:#9b59b6,stroke:#8e44ad,stroke-width:2px
    style D fill:#e74c3c,stroke:#c0392b,stroke-width:2px
    style E fill:#f1c40f,stroke:#f39c12,stroke-width:2px
    
    A(["🚀 Start"]) --> B(["⚙️ Initialize"])
    B --> C(["📨 Send Messages"])
    C --> D(["🔄 Rate Limiting"])
    D --> E(["✅ Success/❌ Fail"])
    E -->|"Loop"| C
```

## 📈 Message Throughput

```mermaid
%%{init: {'theme': 'dark'}}%%
graph LR
    style A fill:#2ecc71,stroke:#27ae60,stroke-width:2px
    style B fill:#3498db,stroke:#2980b9,stroke-width:2px
    style C fill:#9b59b6,stroke:#8e44ad,stroke-width:2px
    style D fill:#e74c3c,stroke:#c0392b,stroke-width:2px
    style E fill:#f1c40f,stroke:#f39c12,stroke-width:2px

    A["10 msgs: 45/s"] --> B["50 msgs: 42/s"]
    B --> C["100 msgs: 40/s"]
    C --> D["500 msgs: 38/s"]
    D --> E["1000 msgs: 35/s"]
```

## ✨ Features

- 🚄 **High Performance**: 35-45 messages per second
- 🔄 **Asynchronous**: Concurrent message sending
- 🎯 **Smart Rate Limiting**: Automatic retry with exponential backoff
- 🎨 **Minimal UI**: Clean design with real-time progress
- 🔒 **Advanced Bypass**: Dynamic device ID and header generation

## 📊 Success Rate Analysis

```mermaid
%%{init: {'theme': 'dark'}}%%
pie
    title "Message Delivery Analysis"
    "✅ Success (95%)" : 95
    "❌ Failed (3%)" : 3
    "⏳ Rate Limited (2%)" : 2
```

## 🔥 System Architecture

```mermaid
%%{init: {'theme': 'dark'}}%%
flowchart LR
    style A fill:#2ecc71,stroke:#27ae60,stroke-width:2px
    style B fill:#3498db,stroke:#2980b9,stroke-width:2px
    style C fill:#9b59b6,stroke:#8e44ad,stroke-width:2px
    style D fill:#e74c3c,stroke:#c0392b,stroke-width:2px
    style E fill:#f1c40f,stroke:#f39c12,stroke-width:2px
    style F fill:#1abc9c,stroke:#16a085,stroke-width:2px
    style G fill:#e67e22,stroke:#d35400,stroke-width:2px

    A[("📱 User Input")] --> B["⚡ Async Engine"]
    B --> C{"🔄 Rate Limiter"}
    C -->|"✅ Pass"| D["📨 Message Sender"]
    C -->|"⏳ Limit"| E["🔄 Retry Handler"]
    E --> B
    D --> F["✅ Success"]
    D --> G["❌ Fail"]
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

- 🎯 Optimal concurrency: 50-100 requests
- 📊 Recommended message count: <1000 per session
- 🌐 Stable internet connection required
- 🔒 Use proxies for better success rate

## ⚠️ Disclaimer

This tool is for educational purposes only. Use responsibly and in accordance with NGL's terms of service.

## 🤝 Contributing

Feel free to:
- 🐛 Open issues
- 🔀 Submit PRs
- 💡 Suggest improvements
- 📝 Report bugs

## 📜 License

MIT License - feel free to use and modify!
