#!/usr/bin/env bash
set -euo pipefail

# Deskew with per-page AUTO margin on the tighter side (prevents left/right clipping)
#
# Usage:
#   Single: ./deskew-best.sh input.[tif|png|jpg] [output_file]
#   Batch : ./deskew-best.sh input_dir [output_dir]
#
# Key env vars (tune as needed):
#   CROP_W=90          # center-band % for angle detection
#   THR=50             # -deskew threshold %
#   BG=white           # background/padding fill color
#   MAX=4              # clamp abs(angle)
#   PADX=12 PADY=6     # pre-rotation padding (%) to avoid corner cuts
#   FINAL=margin       # keep | grow | margin
#   BASE_LEFT_EXTRA=0
#   BASE_RIGHT_EXTRA=150
#   MIN_MARGIN=120     # desired minimum whitespace (px) on each side
#   AUTO_MARGIN=1      # 1=auto-add px to tighter side(s) to reach MIN_MARGIN
#   MARGIN_THRESH=85   # threshold % for margin detection (binarize then trim)
#   ANCHOR=east        # gravity for final extent
#   BILEVEL=0          # 1 => bilevel output
#   QUIET=0            # 1 => less console output

CROP_W="${CROP_W:-90}"
THR="${THR:-50}"
BG="${BG:-white}"
MAX="${MAX:-4}"
PADX="${PADX:-12}"
PADY="${PADY:-6}"
FINAL="${FINAL:-margin}"
BASE_LEFT_EXTRA="${BASE_LEFT_EXTRA:-0}"
BASE_RIGHT_EXTRA="${BASE_RIGHT_EXTRA:-150}"
MIN_MARGIN="${MIN_MARGIN:-120}"
AUTO_MARGIN="${AUTO_MARGIN:-1}"
MARGIN_THRESH="${MARGIN_THRESH:-85}"
ANCHOR="${ANCHOR:-east}"
BILEVEL="${BILEVEL:-0}"
QUIET="${QUIET:-0}"

is_dir()  { [[ -d "$1" ]]; }
is_file() { [[ -f "$1" ]]; }
log() { [[ "$QUIET" = "1" ]] || echo "$@"; }

gravity_for() {
  case "${1,,}" in
    east) echo "East" ;;
    west) echo "West" ;;
    north) echo "North" ;;
    south) echo "South" ;;
    *) echo "Center" ;;
  esac
}

detect_angle() {
  local f="$1" angle=""
  angle=$(magick "$f" \
    -gravity center -crop "${CROP_W}%x100%+0+0" +repage \
    -colorspace Gray -normalize \
    -deskew "${THR}%" \
    -format '%[deskew:angle]' info:) || angle=""
  if [[ -z "$angle" || "$angle" == "0" ]]; then
    local THR2=$(( THR>70 ? THR : THR+20 ))
    angle=$(magick "$f" \
      -gravity center -crop "${CROP_W}%x100%+0+0" +repage \
      -colorspace Gray -normalize -blur 0x0.5 \
      -deskew "${THR2}%" \
      -format '%[deskew:angle]' info:) || angle=""
  fi
  [[ -z "$angle" || "$angle" == "-0" ]] && angle="0"
  awk -v a="$angle" -v m="$MAX" 'BEGIN{ if(a>m)a=m; if(a<-m)a=-m; print a }'
}

# ---- FIXED: robust margin measurement (parse %[page] after trim) ----
measure_margins() {
  local f="$1"
  local origW origH page geom trimW trimH offX offY
  origW=$(magick "$f" -format '%[w]' info:)
  origH=$(magick "$f" -format '%[h]' info:)

  # After threshold+trim, %[page] looks like: WxH+X+Y
  page=$(magick "$f" \
    -colorspace Gray -threshold "${MARGIN_THRESH}%" -type bilevel \
    -trim -format '%[page]' info:) || page=""

  # Fallback if trim failed or page is empty
  if [[ -z "$page" || "$page" == "0x0+0+0" ]]; then
    echo "0,0,0,0"; return
  fi

  # Parse "WxH+X+Y"
  # shellcheck disable=SC2001
  geom=$(echo "$page" | sed 's/x/ /; s/+/ /g')
  read -r trimW trimH offX offY <<<"$geom"

  # Sanity defaults
  [[ -z "${trimW:-}" || -z "${offX:-}" ]] && { echo "0,0,0,0"; return; }

  local left right top bottom
  left="$offX"
  right=$(( origW - (offX + trimW) ))
  top="$offY"
  bottom=$(( origH - (offY + trimH) ))
  # Guard against negatives
  (( left   < 0 )) && left=0
  (( right  < 0 )) && right=0
  (( top    < 0 )) && top=0
  (( bottom < 0 )) && bottom=0
  echo "${left},${right},${top},${bottom}"
}

process_one() {
  local in="$1" out="${2:-}"
  [[ -f "$in" ]] || { log "Skip (not a file): $in"; return; }
  [[ -z "$out" ]] && out="${in%.*}_fixed.${in##*.}"
  mkdir -p "$(dirname "$out")"

  local angle grav
  angle=$(detect_angle "$in")
  grav=$(gravity_for "$ANCHOR")

  # Original geometry and pre-rotation padding
  local origW origH padW padH
  origW=$(magick "$in" -format '%[w]' info:)
  origH=$(magick "$in" -format '%[h]' info:)
  padW=$(magick "$in" -format '%[fx:round(w*(1+'"$PADX"'/100.0))]' info:)
  padH=$(magick "$in" -format '%[fx:round(h*(1+'"$PADY"'/100.0))]' info:)

  # Baseline extras keep your right-edge fix
  local addL="$BASE_LEFT_EXTRA"
  local addR="$BASE_RIGHT_EXTRA"
  local addT=0
  local addB=0

  # Auto-add margins to tighter side(s)
  if [[ "$FINAL" == "margin" && "$AUTO_MARGIN" == "1" ]]; then
    local mL mR mT mB needed
    IFS=',' read -r mL mR mT mB < <(measure_margins "$in")
    if [[ "$mL" -lt "$MIN_MARGIN" ]]; then
      needed=$(( MIN_MARGIN - mL ))
      (( needed > addL )) && addL="$needed"
    fi
    if [[ "$mR" -lt "$MIN_MARGIN" ]]; then
      needed=$(( MIN_MARGIN - mR ))
      (( needed > addR )) && addR="$needed"
    fi
    if [[ "$mT" -lt "$MIN_MARGIN" ]]; then
      needed=$(( MIN_MARGIN - mT ))
      (( needed > addT )) && addT="$needed"
    fi
    if [[ "$mB" -lt "$MIN_MARGIN" ]]; then
      needed=$(( MIN_MARGIN - mB ))
      (( needed > addB )) && addB="$needed"
    fi
  fi

  local finalW finalH
  finalW=$(( origW + addL + addR ))
  finalH=$(( origH + addT + addB ))

  log "[$(basename "$in")] angle=${angle}° (crop=${CROP_W}%, thr=${THR}%, padx=${PADX}%, pady=${PADY}%)"
  log "   margins target≥${MIN_MARGIN}px | addL=${addL}px addR=${addR}px addT=${addT}px addB=${addB}px | final=${finalW}x${finalH}"

  # Pipeline: pad -> rotate -> final extent (margin mode)
  if [[ "$BILEVEL" = "1" ]]; then
    magick "$in" \
      -background "$BG" -alpha remove -alpha off \
      -gravity center -extent "${padW}x${padH}" \
      -rotate "$angle" \
      -gravity "$grav" -extent "${finalW}x${finalH}" \
      -threshold 50% -type bilevel \
      "$out"
  else
    magick "$in" \
      -background "$BG" -alpha remove -alpha off \
      -gravity center -extent "${padW}x${padH}" \
      -rotate "$angle" \
      -gravity "$grav" -extent "${finalW}x${finalH}" \
      "$out"
  fi

  log "✓ Saved: $out"
}

# --- CLI handling: single file vs directory ---
if [[ $# -eq 0 ]]; then
  echo "Usage:"
  echo "  Single: $0 input.[tif|png|jpg] [output_file]"
  echo "  Batch : $0 input_dir [output_dir]"
  exit 1
fi

if is_file "$1"; then
  process_one "$1" "${2:-}"
  exit 0
fi

if is_dir "$1"; then
  in_dir="$1"; out_dir="${2:-fixed}"
  mkdir -p "$out_dir"; shopt -s nullglob
  for f in "$in_dir"/*.{tif,tiff,png,jpg,jpeg,JPG,PNG,TIF,TIFF}; do
    bn="$(basename "$f")"
    process_one "$f" "$out_dir/$bn"
  done
  log "Done -> $out_dir/"
  exit 0
fi

echo "Error: '$1' is neither a file nor a directory."
exit 1

