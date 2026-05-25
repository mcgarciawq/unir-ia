# Scripts Directory

This directory contains automated scripts for project maintenance.

## package.sh

**Automated project packaging script** that generates clean ZIP files by automatically parsing and excluding `.gitignore` patterns.

### Features

- ✅ **Automatic .gitignore parsing**: Reads your `.gitignore` file and converts patterns to proper exclusions
- ✅ **Smart pattern handling**: Supports directories, wildcards, and character classes (like `*.py[cod]`)
- ✅ **Verification**: Automatically checks that excluded files are not included in the final ZIP
- ✅ **Colored logging**: Provides clear feedback during execution
- ✅ **Error handling**: Fails safely if `.gitignore` is missing or other issues occur

### Usage

```bash
# Generate default ZIP file
.github/scripts/package.sh

# Generate custom ZIP filename
.github/scripts/package.sh my_project.zip
```

### What it does

1. **Parses .gitignore**: Reads all patterns and converts them to `find` exclusions
2. **Excludes local `.env` from the file list** (even if not gitignored)
3. **Counts files**: Shows how many files will be included
4. **Creates ZIP**: Uses `find` + `zip -@` for clean packaging
5. **Adds obfuscated `.env`**: Copies `.env` into the ZIP with masked `API_KEY` / `SECRET` / `TOKEN` values (local file unchanged)
6. **Verifies**: Ensures no excluded files made it into the ZIP and checks `.env` presence
7. **Reports**: Provides success/failure feedback

### Example Output

```
[INFO] Starting automated project packaging...
[INFO] Output file: m3_proyecto_carmen_garcia-peral.zip
[INFO] Parsing .gitignore patterns...
[INFO]   Processing: __pycache__/
[INFO]   Processing: *.py[cod]
[INFO]   Processing: .venv/
[INFO]   Processing: .pytest_cache/
[INFO]   Processing: .vscode/
[INFO]   Processing: .DS_Store
[INFO] Generated exclusion patterns: -not -path "./__pycache__/*" -not -name "*.pyc" ...
[INFO] Files to be included: 37
[INFO] Creating ZIP file: m3_proyecto_carmen_garcia-peral.zip
[SUCCESS] ZIP file created successfully: m3_proyecto_carmen_garcia-peral.zip
[INFO] Verifying ZIP contents...
[SUCCESS] No excluded files found in ZIP ✓
[INFO] Total files in ZIP: 37
[SUCCESS] Packaging completed successfully! 🎉
```

### Requirements

- Bash shell
- `find`, `zip`, and `unzip` commands
- `.gitignore` file in project root

### Error Handling

The script will exit with an error if:
- `.gitignore` file is not found
- ZIP creation fails
- Excluded files are found in the final ZIP

This ensures reliable, automated packaging that adapts to changes in your `.gitignore` file.