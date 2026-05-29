#!/bin/bash
# package.sh - Automated project packaging script
# Usage: ./package.sh [output_filename.zip]

OUTPUT_ARG="${1:-m4_proyecto_carmen_garcia-peral.zip}"
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# Normalize output path
if [[ "$OUTPUT_ARG" = /* ]]; then
    OUTPUT_FILE="$OUTPUT_ARG"
else
    OUTPUT_FILE="$PROJECT_ROOT/$OUTPUT_ARG"
fi

# Function to obfuscate the .env file
obfuscate_env_file() {
    local input_file="$1"
    while IFS= read -r line || [[ -n "$line" ]]; do
        # Ignore comments and empty lines
        if [[ "$line" =~ ^[[:space:]]*# ]] || [[ -z "${line//[[:space:]]/}" ]]; then
            echo "$line"
            continue
        fi
        # Check for key=value pattern
        if [[ "$line" =~ ^[[:space:]]*([A-Za-z_][A-Za-z0-9_]*)=(.*)$ ]]; then
            local key="${BASH_REMATCH[1]}"
            local raw_value="${BASH_REMATCH[2]}"
            local value="$raw_value"
            local quote=""

            # Handle quoted values
            if [[ "$value" =~ ^\"(.*)\"$ ]]; then
                quote="\""
                value="${BASH_REMATCH[1]}"
            elif [[ "$value" =~ ^\'(.*)\'$ ]]; then
                quote="'"
                value="${BASH_REMATCH[1]}"
            fi

            # Obfuscate sensitive keys
            if [[ "$key" =~ (API_KEY|SECRET|TOKEN|PASSWORD|CREDENTIAL) ]]; then
                if [[ -z "$value" ]]; then
                    echo "${key}="
                elif [[ ${#value} -le 8 ]]; then
                    echo "${key}=${quote}********${quote}"
                else
                    local prefix="${value:0:4}"
                    local suffix="${value: -4}"
                    echo "${key}=${quote}${prefix}****${suffix}${quote}"
                fi
            else
                echo "$line"
            fi
        else
            echo "$line"
        fi
    done < "$input_file"
}

cd "$PROJECT_ROOT" || exit 1

echo "[INFO] Starting automated project packaging..."

# 1. Create ZIP using git archive (automatically respects .gitignore)
echo "[INFO] Archiving project files (respecting .gitignore)..."
git archive --format=zip HEAD -o "$OUTPUT_FILE"

# 2. Handle .env file
if [[ -f ".env" ]]; then
    echo "[INFO] Adding obfuscated .env to ZIP..."
    STAGING_DIR=$(mktemp -d)
    obfuscate_env_file ".env" > "$STAGING_DIR/.env"
    
    # -u: update/add to existing zip, -j: junk paths (store only the file)
    zip -u "$OUTPUT_FILE" -j "$STAGING_DIR/.env"
    
    rm -rf "$STAGING_DIR"
    echo "[SUCCESS] .env added with obfuscated credentials"
else
    echo "[WARNING] No .env file found."
fi

echo "[SUCCESS] ZIP file created successfully: $OUTPUT_FILE"

# 3. Verification
echo "[INFO] Verifying ZIP contents..."
# Check for files that should have been ignored
bad_files=$(unzip -l "$OUTPUT_FILE" 2>/dev/null | grep -E "__pycache__|\.pyc|\.pyo|\.pyd|\.venv|\.pytest_cache|\.vscode|\.DS_Store" | wc -l | tr -d ' ')

if [[ $bad_files -gt 0 ]]; then
    echo "[ERROR] Found excluded files in ZIP:"
    unzip -l "$OUTPUT_FILE" | grep -E "__pycache__|\.pyc|\.pyo|\.pyd|\.venv|\.pytest_cache|\.vscode|\.DS_Store"
    exit 1
else
    echo "[SUCCESS] No excluded files found in ZIP ✓"
fi

total_files=$(unzip -l "$OUTPUT_FILE" 2>/dev/null | tail -1 | awk '{print $2}')
echo "[INFO] Total files in ZIP: $total_files"
echo "[SUCCESS] Packaging completed successfully! 🎉"
