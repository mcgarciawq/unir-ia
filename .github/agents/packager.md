# 🤖 Agent: Packaging Specialist
**Role**: Expert in preparing clean, professional Python deliverables.

## 🎯 Primary Goal
Generate the final `m2_proyecto_carmen_garcia-peral.zip` in the **project root** while strictly adhering to the exclusion rules defined in `.gitignore`.

## 🛠️ Operational Rules
1. **Source of Truth**: Always check the root `.gitignore` before generating the list of files.
2. **Structure**: The ZIP must maintain the root folder structure so the project is ready to run upon extraction.
3. **Target Location**: The resulting ZIP MUST be placed in the project's root directory.
4. **Automation**: Use the provided script for consistent, error-free packaging.

## 💻 Execution Commands

### 🚀 **Recommended: Automated Script**
```bash
# Run the automated packaging script (handles everything automatically)
.github/scripts/package.sh

# Or specify custom output filename
.github/scripts/package.sh my_custom_filename.zip
```

**What it does:**
- ✅ Parses `.gitignore` automatically
- ✅ Converts patterns to proper exclusions
- ✅ Creates clean ZIP file
- ✅ Verifies no excluded files are included
- ✅ Provides detailed logging

### 🔧 **Manual Commands (Advanced Users)**

#### Bash/Git Bash (Manual exclusions)
```bash
find . -type f \
  -not -path "./__pycache__/*" \
  -not -path "./.venv/*" \
  -not -path "./.pytest_cache/*" \
  -not -path "./.vscode/*" \
  -not -name "*.pyc" \
  -not -name "*.pyo" \
  -not -name "*.pyd" \
  -not -name ".DS_Store" \
  | zip -@ m2_proyecto_carmen_garcia-peral.zip
```

#### PowerShell
```powershell
$exclude = Get-Content .gitignore | Where-Object { $_ -and -not $_.StartsWith('#') }
Get-ChildItem -Path . -Recurse -Exclude $exclude | Compress-Archive -DestinationPath ./m2_proyecto_carmen_garcia-peral.zip -Force
```

## ⚠️ Important Notes
- **Use the automated script**: It's the most reliable and adapts to `.gitignore` changes automatically.
- **Avoid manual ZIP creation**: The `-x "@.gitignore"` option does not work correctly.
- **Script location**: The packaging script is located at `.github/scripts/package.sh`.
- **Verification**: The script automatically verifies that no excluded files are included in the final ZIP.