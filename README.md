# 🔬 Multi-Agent Research AI

> An autonomous AI research assistant powered by **Mistral AI**, **LangChain**, **Tavily**, and **Streamlit** — built on a 4-agent pipeline that searches, scrapes, writes, and critiques research reports in minutes.



## 🧠 How It Works

The system runs a sequential 4-agent pipeline on any research topic:

```
User Input → Search Agent → Reader Agent → Writer Chain → Critic Chain → Final Report
```

| Step | Agent | Role |
|------|-------|------|
| 01 | **Search Agent** | Uses Tavily to find recent, reliable web sources |
| 02 | **Reader Agent** | Picks the best URL and scrapes deep content |
| 03 | **Writer Chain** | Synthesizes research into a structured report |
| 04 | **Critic Chain** | Reviews and scores the report (strengths, improvements, verdict) |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| [Mistral AI](https://mistral.ai) | LLM backbone (`mistral-small`) |
| [LangChain](https://langchain.com) | Agent orchestration & chains |
| [Tavily](https://tavily.com) | Real-time web search API |
| [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) | Web scraping & HTML parsing |
| [Streamlit](https://streamlit.io) | Interactive web UI |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Environment variable management |

---

## 📁 Project Structure

```
deepresearch-ai/
├── app.py            # Streamlit UI — all frontend logic
├── agents.py         # Agent definitions (search, reader, writer, critic)
├── pipeline.py       # Core pipeline runner (CLI entry point)
├── tools.py          # LangChain tools (web_search, scrape_url)
├── requirements.txt  # Python dependencies
├── .gitignore        # Git ignore rules
└── .env              # API keys (not committed)
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Suryawanshi123566/deepresearch-ai.git
cd deepresearch-ai
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:
```env
MISTRAL_API_KEY=your_mistral_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Get your API keys:
- Mistral AI → [https://console.mistral.ai](https://console.mistral.ai)
- Tavily → [https://app.tavily.com](https://app.tavily.com)

### 5. Run the app
```bash
streamlit run app.py
```

Or run the pipeline directly from CLI:
```bash
python pipeline.py
```

---

## 📋 Features

- ⚡ **4-agent autonomous pipeline** — no manual steps
- 🔍 **Real-time web search** via Tavily API
- 📄 **Deep content scraping** from top sources
- 📝 **Structured report generation** — Introduction, Key Findings, Conclusion, Sources
- 🧐 **AI critic review** — Score, Strengths, Areas to Improve, Verdict
- ⬇️ **Downloadable reports** as `.md` files
- 🎨 **Professional dark UI** built with Streamlit

---
## 📸 Screenshots

![Screenshot 1](assets/Screenshot%202026-05-28%20125358.png)
![Screenshot 2](assets/Screenshot%202026-05-28%20125440.png)
![Screenshot 3](assets/Screenshot%202026-05-28%20125502.png)
![Screenshot 4](assets/Screenshot%202026-05-28%20125528.png)
![Screenshot 5](assets/Screenshot%202026-05-28%20125603.png)

---
## 🖥️ Usage

1. Open the app in your browser (`http://localhost:8501`)
2. Enter any research topic (e.g. *"Latest breakthroughs in quantum computing 2025"*)
3. Click **Execute Research Pipeline**
4. Watch all 4 agents work in real-time
5. Read the final report and critic feedback
6. Download the report as a Markdown file

---

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MISTRAL_API_KEY` | Your Mistral AI API key | ✅ Yes |
| `TAVILY_API_KEY` | Your Tavily search API key | ✅ Yes |

---

## 📦 Requirements

- Python `3.9+`
- Internet connection (for web search & scraping)
- Mistral AI account
- Tavily account

---

Live Demo

🔗 Streamlit Deployment:
https://deepresearch-ai-apvfy8hdha9ndpqjcs9zim.streamlit.app/

GitHub Repository

💻 GitHub:
https://github.com/Suryawanshi123566/deepresearch-ai

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Open an [issue](https://github.com/Suryawanshi123566/deepresearch-ai/issues) for bugs or feature requests
- Submit a [pull request](https://github.com/Suryawanshi123566/deepresearch-ai/pulls) with improvements

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👩‍💻 Author

**Suryawanshi123566**
- GitHub: [@Suryawanshi123566](https://github.com/Suryawanshi123566)

---

<div align="center">
  <sub>Built with ❤️ using LangChain · Mistral AI · Tavily · Streamlit</sub>
</div>
