#!/bin/bash
# package.sh - Automated project packaging script
# Usage: ./package.sh [output_filename.zip]
#
# Builds the submission ZIP from .gitignore rules, then adds .env at the
# project root with obfuscated secrets. The local .env is never modified.

OUTPUT_ARG="${1:-m3_proyecto_carmen_garcia-peral.zip}"
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

if [[ "$OUTPUT_ARG" = /* ]]; then
    OUTPUT_FILE="$OUTPUT_ARG"
else
    OUTPUT_FILE="$PROJECT_ROOT/$OUTPUT_ARG"
fi

obfuscate_env_file() {
    local input_file="$1"
    while IFS= read -r line || [[ -n "$line" ]]; do
        if [[ "$line" =~ ^[[:space:]]*# ]] || [[ -z "${line//[[:space:]]/}" ]]; then
            echo "$line"
            continue
        fi
        if [[ "$line" =~ ^[[:space:]]*([A-Za-z_][A-Za-z0-9_]*)=(.*)$ ]]; then
            local key="${BASH_REMATCH[1]}"
            local raw_value="${BASH_REMATCH[2]}"
            local value="$raw_value"
            local quote=""

            if [[ "$value" =~ ^\"(.*)\"$ ]]; then
                quote="\""
                value="${BASH_REMATCH[1]}"
            elif [[ "$value" =~ ^\'(.*)\'$ ]]; then
                quote="'"
                value="${BASH_REMATCH[1]}"
            fi

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
echo "[INFO] Output file: $OUTPUT_FILE"

if [[ ! -f ".gitignore" ]]; then
    echo "[ERROR] .gitignore file not found!"
    exit 1
fi

echo "[INFO] Parsing .gitignore patterns..."

find_cmd="find . -type f -not -path './.env'"

while IFS= read -r pattern; do
    [[ $pattern =~ ^# ]] && continue
    [[ -z $pattern ]] && continue

    if [[ $pattern == */ ]]; then
        dir_pattern="${pattern%/}"
        find_cmd="$find_cmd -not -path './$dir_pattern/*'"
        echo "[INFO]   Directory: $pattern"
    elif [[ $pattern == *\** ]]; then
        if [[ $pattern == *\[* ]]; then
            base="${pattern%\[*\]}"
            class="${pattern#*\[}"
            class="${class%\]*}"
            echo "[INFO]   Character class: $pattern"
            for char in $(echo "$class" | grep -o .); do
                find_cmd="$find_cmd -not -name '$base$char'"
            done
        else
            find_cmd="$find_cmd -not -name '$pattern'"
            echo "[INFO]   Wildcard: $pattern"
        fi
    else
        find_cmd="$find_cmd -not -name '$pattern'"
        echo "[INFO]   Exact filename: $pattern"
    fi
done < .gitignore

include_count=$(eval "$find_cmd" | wc -l | tr -d ' ')
echo "[INFO] Files to be included (excluding .env): $include_count"

if [[ -f "$OUTPUT_FILE" ]]; then
    echo "[WARNING] Removing existing ZIP file: $OUTPUT_FILE"
    rm -f "$OUTPUT_FILE"
fi

echo "[INFO] Creating ZIP file: $OUTPUT_FILE"
eval "$find_cmd" | zip -@ "$OUTPUT_FILE"

if [[ -f ".env" ]]; then
    echo "[INFO] Adding obfuscated .env to ZIP..."
    STAGING_DIR=$(mktemp -d)
    obfuscate_env_file ".env" > "$STAGING_DIR/.env"
    (cd "$STAGING_DIR" && zip "$OUTPUT_FILE" .env)
    rm -rf "$STAGING_DIR"
    echo "[SUCCESS] .env added with obfuscated credentials"
else
    echo "[WARNING] No .env file found — ZIP will not contain Azure configuration"
fi

echo "[SUCCESS] ZIP file created successfully: $OUTPUT_FILE"

echo "[INFO] Verifying ZIP contents..."

bad_files=$(unzip -l "$OUTPUT_FILE" 2>/dev/null | grep -E "__pycache__|\.pyc|\.pyo|\.pyd|\.venv|\.pytest_cache|\.vscode|\.DS_Store" | wc -l | tr -d ' ')

if [[ $bad_files -gt 0 ]]; then
    echo "[ERROR] Found excluded files in ZIP:"
    unzip -l "$OUTPUT_FILE" | grep -E "__pycache__|\.pyc|\.pyo|\.pyd|\.venv|\.pytest_cache|\.vscode|\.DS_Store"
    exit 1
else
    echo "[SUCCESS] No excluded files found in ZIP ✓"
fi

if unzip -l "$OUTPUT_FILE" 2>/dev/null | grep -qE '(^| )\.env$'; then
    echo "[SUCCESS] .env is present in ZIP ✓"
    if unzip -p "$OUTPUT_FILE" .env 2>/dev/null | grep -qE '(API_KEY|SECRET|TOKEN|PASSWORD).*\*\*\*\*'; then
        echo "[SUCCESS] .env credentials appear obfuscated ✓"
    else
        echo "[WARNING] .env is in ZIP — review obfuscation manually if keys were set"
    fi
else
    echo "[WARNING] .env not found inside ZIP"
fi

total_files=$(unzip -l "$OUTPUT_FILE" 2>/dev/null | tail -1 | awk '{print $2}')
echo "[INFO] Total files in ZIP: $total_files"

echo "[SUCCESS] Packaging completed successfully! 🎉"
echo "[INFO] Ready for submission: $OUTPUT_FILE"
