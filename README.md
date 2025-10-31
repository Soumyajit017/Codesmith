# 🤖 CodeSmith - Autonomous Python Coding Agent

**An AI-powered system that generates Python code from natural language descriptions.**

[![Status](https://img.shields.io/badge/status-production-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.10+-blue)]()
[![Tests](https://img.shields.io/badge/tests-100%25%20passing-success)]()
[![LLM](https://img.shields.io/badge/LLM-Gemini%20%7C%20GPT--4%20%7C%20Claude-orange)]()

---

## 🎯 What is CodeSmith?

CodeSmith automatically writes Python programs from plain English descriptions. You describe what you want, provide test cases, and CodeSmith:

1. ✅ Generates working Python code
2. ✅ Tests it automatically
3. ✅ Self-repairs if tests fail
4. ✅ Saves the solution

**No more writing boilerplate. Just describe your problem!**

---

## 🚀 Quick Start (30 seconds)

### 1. Create a task file (`my_task.json`):
```json
{
  "task": "Write a Python program that reads a number from stdin (using sys.stdin.readline()) and prints if it's even or odd. No command-line arguments, no doctests.",
  "test_cases": [
    {"input": "4", "expected": "even"},
    {"input": "7", "expected": "odd"}
  ],
  "run_doctests": false
}
```

### 2. Run CodeSmith:
```bash
python run_codesmith.py my_task.json --llm gemini --api-key YOUR_API_KEY --output solution.py
```

### 3. Use your solution:
```bash
echo 10 | python solution.py
# Output: even
```

**That's it!** 🎉

---

## 📁 Project Structure

```
codesmith-project/
│
├── run_codesmith.py           ⭐ Main entry point (USE THIS!)
├── requirements-codesmith.txt  📦 Dependencies
├── PROJECT_STRUCTURE.md        📖 Detailed structure guide
│
├── codesmith/                  🔵 Core system (stable)
│   ├── agent.py               🤖 AI agent (Gemini, GPT-4, Claude)
│   ├── sandbox.py             🔒 Safe code execution
│   ├── orchestrator.py        🔄 Task loop & auto-repair
│   └── ...
│
├── examples/                   🟢 Your workspace
│   ├── tasks/                 📝 Task specifications
│   ├── solutions/             ✨ Generated code
│   └── demos/                 🎬 Demo scripts
│
└── docs/                       🟡 Documentation
    ├── QUICKSTART_YOUR_PROBLEMS.md  ⭐ START HERE
    ├── HOW_TO_USE.md                📚 Full guide
    └── ...
```

**See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for complete details.**

---

## 📚 Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| **[QUICKSTART_YOUR_PROBLEMS.md](docs/QUICKSTART_YOUR_PROBLEMS.md)** | **How to solve YOUR problems** | **👤 Users (START HERE!)** |
| [HOW_TO_USE.md](docs/HOW_TO_USE.md) | Detailed usage guide | Users |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design | Developers |
| [TEST_RESULTS.md](docs/TEST_RESULTS.md) | Test validation | Reference |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Directory structure | All |

---

## ✨ Features

- 🤖 **Multiple LLM Support**: Gemini, OpenAI GPT-4, Anthropic Claude, Mock
- 🔒 **Safe Execution**: Isolated sandbox environment
- 🔄 **Auto-Repair**: Fixes failing code automatically (up to 3 attempts)
- ✅ **Test Validation**: Runs test cases to verify correctness
- 📝 **Clear Output**: Structured JSON responses (plan, code, notes)
- 🎯 **High Success Rate**: 100% pass rate on all test tasks

---

## 🎓 Example Use Cases

Create programs that:
- 📊 **Calculate statistics** (mean, median, mode)
- 🔢 **Math operations** (Fibonacci, primes, factorials)
- 📝 **Text processing** (word count, palindrome check, case conversion)
- 🔄 **Data transformation** (sorting, filtering, mapping)
- ✅ **Validation** (even/odd, prime check, password strength)
- 🌡️ **Conversions** (temperature, units, currencies)

**See `examples/` for working demonstrations!**

---

## 🛠️ Installation

### Prerequisites
- Python 3.10 or higher
- Google Gemini API key (or OpenAI/Anthropic)

### Setup
```bash
# 1. Install dependencies
pip install -r requirements-codesmith.txt

# 2. Get API key from https://makersuite.google.com/app/apikey

# 3. Ready to use!
python run_codesmith.py examples/tasks/word_count_task.json --llm gemini --api-key YOUR_KEY --output solution.py
```

---

## 🎯 Usage Examples

### Example 1: Word Counter
```bash
python run_codesmith.py examples/tasks/word_count_task.json \
  --llm gemini \
  --api-key AIzaSy... \
  --output word_counter.py
```

### Example 2: Temperature Converter
Create `temp_task.json`:
```json
{
  "task": "Read Celsius from stdin, print Fahrenheit (F = C * 9/5 + 32), rounded to 1 decimal. No args, no doctests.",
  "test_cases": [
    {"input": "0", "expected": "32.0"},
    {"input": "100", "expected": "212.0"}
  ],
  "run_doctests": false
}
```

Run:
```bash
python run_codesmith.py temp_task.json --llm gemini --api-key YOUR_KEY --output temp.py
echo 25 | python temp.py  # Output: 77.0
```

---

## 🔧 Command Line Options

```bash
python run_codesmith.py TASK.json [OPTIONS]

Required:
  TASK.json              Task specification file

Options:
  --llm PROVIDER         LLM provider: gemini, openai, anthropic, mock (default: mock)
  --api-key KEY          API key for LLM provider
  --output FILE          Output file path (default: solution.py)
  --max-attempts N       Max repair attempts (default: 3)
  --verbose              Enable verbose output
```

---

## 📊 Test Results

**Latest validation: 5/5 tasks passed (100% success rate)**

| Task | Test Cases | Status |
|------|-----------|--------|
| Sum Two Numbers | 2/2 | ✅ |
| Fibonacci Sequence | 2/2 | ✅ |
| Palindrome Checker | 2/2 | ✅ |
| Prime Validator | 4/4 | ✅ |
| Reverse Words | 2/2 | ✅ |

**Total: 14/14 test cases passed**

See [TEST_RESULTS.md](docs/TEST_RESULTS.md) for details.

---

## 🤝 Contributing

This is a complete, working system. To extend:

1. **Add LLM provider**: Edit `codesmith/agent.py`
2. **Improve sandbox**: Edit `codesmith/sandbox.py`
3. **Add examples**: Create new task JSONs in `examples/tasks/`

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design.

---

## 📄 License

MIT License - Feel free to use and modify!

---

## 🆘 Support

- **Quick Help**: Read [QUICKSTART_YOUR_PROBLEMS.md](docs/QUICKSTART_YOUR_PROBLEMS.md)
- **Detailed Guide**: See [HOW_TO_USE.md](docs/HOW_TO_USE.md)
- **Issues**: Check task description clarity and test case format

---

## 🎉 Success Stories

CodeSmith has successfully generated:
- ✅ Mathematical algorithms (Fibonacci, primes)
- ✅ String processors (palindrome, word reversal)
- ✅ Statistical calculators (mean, median)
- ✅ Input validators (even/odd, prime check)
- ✅ Text analyzers (word count, vowel count)

**Your turn to build something amazing!** 🚀

---

## 🔗 Quick Links

- 📖 [Full Documentation](docs/)
- 🎬 [Examples](examples/)
- 🏗️ [Architecture](docs/ARCHITECTURE.md)
- ✅ [Test Results](docs/TEST_RESULTS.md)

---

**Made with ❤️ using AI-powered code generation**
