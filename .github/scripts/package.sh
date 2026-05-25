#!/bin/bash
# package.sh - Automated project packaging script
# Usage: ./package.sh [output_filename.zip]

OUTPUT_FILE="${1:-m2_proyecto_carmen_garcia-peral.zip}"

echo "[INFO] Starting automated project packaging..."
echo "[INFO] Output file: $OUTPUT_FILE"

# Check if .gitignore exists
if [[ ! -f ".gitignore" ]]; then
    echo "[ERROR] .gitignore file not found!"
    exit 1
fi

echo "[INFO] Parsing .gitignore patterns..."

# Build find command with exclusions from .gitignore
# We use a string instead of an array to avoid word splitting issues
find_cmd="find . -type f"

while IFS= read -r pattern; do
    # Skip comments and empty lines
    [[ $pattern =~ ^# ]] && continue
    [[ -z $pattern ]] && continue

    # Convert .gitignore patterns to find exclusions
    if [[ $pattern == */ ]]; then
        # Directory patterns (ending with /)
        dir_pattern="${pattern%/}"
        find_cmd="$find_cmd -not -path './$dir_pattern/*'"
        echo "[INFO]   Directory: $pattern"
    elif [[ $pattern == *\** ]]; then
        # File patterns with wildcards
        if [[ $pattern == *\[* ]]; then
            # Handle character classes like *.py[cod]
            base="${pattern%\[*\]}"
            class="${pattern#*\[}"
            class="${class%\]*}"
            echo "[INFO]   Character class: $pattern"
            for char in $(echo "$class" | grep -o .); do
                find_cmd="$find_cmd -not -name '$base$char'"
            done
        else
            # Simple wildcards
            find_cmd="$find_cmd -not -name '$pattern'"
            echo "[INFO]   Wildcard: $pattern"
        fi
    else
        # Exact filenames
        find_cmd="$find_cmd -not -name '$pattern'"
        echo "[INFO]   Exact filename: $pattern"
    fi
done < .gitignore

# Count files that will be included
include_count=$(eval "$find_cmd" | wc -l)
echo "[INFO] Files to be included: $include_count"

# Remove existing ZIP if it exists
if [[ -f "$OUTPUT_FILE" ]]; then
    echo "[WARNING] Removing existing ZIP file: $OUTPUT_FILE"
    rm "$OUTPUT_FILE"
fi

echo "[INFO] Creating ZIP file: $OUTPUT_FILE"

# Create ZIP file
eval "$find_cmd" | zip -@ "$OUTPUT_FILE"

echo "[SUCCESS] ZIP file created successfully: $OUTPUT_FILE"

# Verify ZIP contents
echo "[INFO] Verifying ZIP contents..."

# Check for excluded files
bad_count=$(unzip -l "$OUTPUT_FILE" 2>/dev/null | grep -c "^\s*0\s" || echo "0")

if [[ "$bad_count" -gt 5 ]]; then
    echo "[WARNING] ZIP contains zero-size entries (might be spurious files)"
fi

# Specifically check for problematic patterns
bad_files=$(unzip -l "$OUTPUT_FILE" 2>/dev/null | grep -E "__pycache__|\.pyc|\.pyo|\.pyd|\.venv|\.pytest_cache|\.vscode|\.DS_Store" | wc -l)

if [[ $bad_files -gt 0 ]]; then
    echo "[ERROR] Found excluded files in ZIP:"
    unzip -l "$OUTPUT_FILE" | grep -E "__pycache__|\.pyc|\.pyo|\.pyd|\.venv|\.pytest_cache|\.vscode|\.DS_Store"
    exit 1
else
    echo "[SUCCESS] No excluded files found in ZIP ✓"
fi

# Count total files in ZIP
total_files=$(unzip -l "$OUTPUT_FILE" 2>/dev/null | tail -1 | awk '{print $2}')
echo "[INFO] Total files in ZIP: $total_files"

echo "[SUCCESS] Packaging completed successfully! 🎉"
echo "[INFO] Ready for submission: $OUTPUT_FILE"
