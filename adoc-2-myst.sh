#!/usr/bin/env bash

set -euo pipefail

OUTPUT_OVERRIDE=""
INPUT=""

# --- Parse args (order-independent) ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    -o)
      OUTPUT_OVERRIDE="$2"
      shift 2
      ;;
    -*)
      echo "Unknown option: $1"
      echo "Usage: $0 [-o output.md] <input.adoc>"
      exit 1
      ;;
    *)
      INPUT="$1"
      shift
      ;;
  esac
done

# --- Input validation ---
if [[ -z "$INPUT" ]]; then
  echo "Usage: $0 [-o output.md] <input.adoc>"
  exit 1
fi

if [[ ! -f "$INPUT" ]]; then
  echo "Error: file not found: $INPUT"
  exit 1
fi

# --- Derive names ---
BASENAME="$(basename "$INPUT" .adoc)"
WORKDIR="$(dirname "$INPUT")"

DOC5="$WORKDIR/doc5.xml"
DOC5_NONS="$WORKDIR/doc5-nons.xml"
DOC4="$WORKDIR/doc4.xml"

# --- Output handling ---
if [[ -n "$OUTPUT_OVERRIDE" ]]; then
  OUTPUT_MD="$OUTPUT_OVERRIDE"
else
  OUTPUT_MD="$WORKDIR/${BASENAME}.md"
fi

# --- Configure dbcookbook location ---
DBCOOKBOOK_DIR="${DBCOOKBOOK_DIR:-$HOME/temp/dbcookbook}"
XSL_DIR="$DBCOOKBOOK_DIR/en/xml/structure/db5-to-db4"
XSL_FILE="$XSL_DIR/db5to4.xsl"

if [[ ! -f "$XSL_FILE" ]]; then
  echo "Error: db5to4.xsl not found at: $XSL_FILE"
  echo "Set DBCOOKBOOK_DIR to the correct location."
  exit 1
fi

# --- Step 1 ---
asciidoctor -b docbook "$INPUT" -o "$DOC5"

# --- Step 2 ---
sed 's/xmlns="http:\/\/docbook.org\/ns\/docbook"//' "$DOC5" > "$DOC5_NONS"

# --- Step 3 ---
xsltproc \
  --path "$XSL_DIR" \
  "$XSL_FILE" \
  "$DOC5_NONS" > "$DOC4"

# --- Step 4 ---
python3 ~/snla/convert.py "$DOC4" > "$OUTPUT_MD"

echo "Done: $OUTPUT_MD"
