# CodeSmith Multi-Language - Quick Test Guide

## ✅ System Status

All components are installed and working!

## 🚀 Quick Test (No API Key Required)

```powershell
# Run the showcase demo with mock LLM
python examples\demos\showcase_multilang.py
```

**Expected Output:**
- ✅ Parses LeetCode problem
- ✅ Generates 4 task JSON files
- ✅ Creates solutions in Python, C++, Java, JavaScript
- ✅ Displays results table
- ✅ Saves all files to `showcase_output/`

## 🔥 Test With Real LLM (Gemini)

### Step 1: Get API Key
Visit: https://makersuite.google.com/app/apikey

### Step 2: Parse Sample Problem
```powershell
python run_multilang.py parse sample_leetcode.txt
```

**Expected:** Creates `tasks/two_sum_*.json` files

### Step 3: Generate Solutions
```powershell
python run_multilang.py generate tasks/two_sum_python.json --llm gemini --api-key YOUR_KEY
```

**Expected:**
- Generates Python, C++, Java, JavaScript solutions
- Tests Python code
- Shows algorithm type (Hash Table)
- Shows complexity (O(n) time, O(n) space)
- Saves to `solutions/`

### Step 4: Full Workflow
```powershell
python run_multilang.py full sample_leetcode.txt --llm gemini --api-key YOUR_KEY
```

**Expected:** Complete workflow in one command!

## 📋 Test Checklist

- [ ] Showcase demo runs successfully
- [ ] Parser creates 4 task JSON files
- [ ] Generator works with Gemini API
- [ ] Results table displays correctly
- [ ] All 4 language solutions saved
- [ ] Algorithm detection works
- [ ] Complexity extraction works

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'codesmith'"
```powershell
# Make sure you're in the project root
cd "c:\Users\soumyajit\Downloads\python\teaching python\shitty works"
```

### "No API key provided"
```powershell
# Pass API key as argument
python run_multilang.py generate task.json --llm gemini --api-key YOUR_KEY

# Or set environment variable
$env:GEMINI_API_KEY = "your-key-here"
python run_multilang.py generate task.json --llm gemini
```

### "Failed to parse problem"
Make sure your problem text includes:
- Title at the top
- Examples with "Input:" and "Output:"
- Constraints section

## 📁 Generated Files

After running tests, you should have:

```
tasks/
├── two_sum_python.json
├── two_sum_cpp.json
├── two_sum_java.json
└── two_sum_javascript.json

solutions/
└── two_sum/
    ├── solution.py
    ├── solution.cpp
    ├── solution.java
    └── solution.js

showcase_output/
├── solution.py
├── solution.cpp
├── solution.java
└── solution.js
```

## 🎯 What to Demo for Resume/Interview

1. **Show the full workflow:**
   ```powershell
   python run_multilang.py full sample_leetcode.txt --llm gemini --api-key KEY
   ```

2. **Highlight the features:**
   - Multi-language support (4 languages!)
   - LeetCode integration (copy-paste convenience)
   - Algorithm detection (shows CS knowledge)
   - Complexity analysis (Big-O understanding)
   - Clean architecture (professional code)

3. **Explain the tech stack:**
   - Google Gemini AI API
   - Python 3.11+
   - JSON protocol
   - Sandbox execution
   - Automated testing

## 📚 Documentation

- **Quick Start:** README.md
- **Multi-Language Guide:** docs/MULTILANG_GUIDE.md
- **Feature Summary:** FEATURE_COMPLETE.md
- **Command Reference:** docs/QUICK_REFERENCE.md

## 🔗 GitHub Repository

https://github.com/Soumyajit017/Codesmith

**Ready to showcase on your resume!** ✨
