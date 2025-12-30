# Smart QA: Intelligent Document Analysis CLI

Smart QA is a production-grade Python CLI tool designed to streamline interactions with the Google Gen AI (Gemini) API. It provides a robust, fault-tolerant interface for text summarization, context-aware Q&A, and structured entity extraction.

This project demonstrates modern Python engineering practices, including dependency injection, decorator-based resiliency patterns, and comprehensive unit testing.

## 🚀 Engineering Highlights

This is not just a wrapper; it is an optimized client built for reliability.

- **⚡ Cost Optimization (Caching)**: Implements `functools.lru_cache` to eliminate redundant API calls for identical queries during runtime, reducing latency and cost.
- **🛡️ Network Resilience**: Features a custom Exponential Backoff & Retry decorator. The client automatically handles transient HTTP 503 errors (Service Unavailable) without crashing.
- **🏗️ Structured Data Guarantee**: Solves the "LLM Hallucination" problem for JSON output by implementing rigorous string cleaning and validation logic, ensuring downstream systems receive valid JSON.
- **🧪 100% Test Coverage**: A full suite of unit tests using pytest and unittest.mock. Tests cover happy paths, API failures, missing credentials, and malformed responses.

## 🛠️ Installation

This project uses Poetry for deterministic dependency management.

1. **Clone the repository:**

```bash
git clone https://github.com/dishydammy/smart_qa.git
cd smart_qa
```

2. **Install dependencies:**

```bash
poetry install
```

3. **Configuration:** Create a `.env` file in the root directory to store sensitive credentials safely (following 12-Factor App principles).

```ini
GOOGLE_API_KEY=your_google_api_key_here
```
## 📖 Usage Guide

The tool exposes a clean CLI interface using `argparse`.

### 1. Summarization

Generate concise summaries of large text blocks or files.

```bash
poetry run python main.py summarize --file data/whitepaper.txt --save summary.txt
```

### 2. Context-Aware Q&A (RAG-Style)

Ask specific questions based strictly on the provided context, reducing hallucinations.

```bash
poetry run python main.py ask --file legal_contract.txt --question "What is the termination clause?"
```

### 3. Entity Extraction

Extract structured JSON data (People, Dates, Locations). The tool automatically strips Markdown formatting from the LLM response.

```bash
poetry run python main.py extract --text "Elon Musk visited Berlin on December 1st."
```

**Output:**

```json
{
  "People": ["Elon Musk"],
  "Locations": ["Berlin"],
  "Dates": ["December 1st"]
}
```
## 🧪 Testing & Quality

Reliability is paramount. The test suite mocks external API calls to ensure tests are fast, free, and deterministic.

**Run Unit Tests:**

```bash
poetry run pytest
```

**Verify Coverage:**

```bash
poetry run pytest --cov=smart_qa
```

**Current Status**: 100% Pass Rate

## 📂 Project Architecture

```
smart_qa/
├── smart_qa/
│   ├── client.py           # Core Engine: API handling, Caching, Retry Decorators
│   ├── custom_exceptions.py # Custom Domain Exceptions (Decoupling logic)
│   └── __init__.py
├── tests/
│   ├── conftest.py         # Pytest Fixtures (Mock Injection)
│   ├── test_client.py      # Comprehensive Test Suite
│   └── data/               # Test Assets
├── main.py                 # CLI Controller / Entry Point
├── pyproject.toml          # Poetry Dependency Lock
└── README.md
```