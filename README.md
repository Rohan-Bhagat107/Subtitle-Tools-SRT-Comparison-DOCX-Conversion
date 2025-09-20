# Subtitle-Tools-SRT-Comparison-DOCX-Conversion
Tools for comparing two SRT subtitle files with detailed diff reports and converting speaker-tagged SRTs into clean DOCX files with merged dialogues. Useful for subtitle review, editing, and documentation workflows.

# 🎬 Subtitle Utilities: SRT Comparison & DOCX Conversion

This repository contains two Python scripts designed to work with `.srt` subtitle files:

## 🔍 1. SRT Comparison Tool

**Purpose**: Compare two `.srt` files (e.g., Reference vs Hypothesis) and generate a detailed `.txt` report highlighting:

- Timecode differences
- Word-level insertions and deletions
- Aligned subtitle segments for easy review

**Output**:  
Generates a `Report_<original_filename>.txt` file in the same directory as the original `.srt`.

### 🧪 Features:
- Compares subtitles segment-by-segment
- Highlights word-level differences using `[word]` formatting
- Shows insertions and deletions
- Compatible with UTF-8 encoded `.srt` files

---

## 📝 2. SRT to DOCX Converter

**Purpose**: Convert speaker-tagged `.srt` files into a well-formatted `.docx` document.

### 🎯 Features:
- Detects speaker names formatted like `[Speaker] Dialogue`
- Merges continuous lines from the same speaker
- Creates a DOCX with a two-column layout:
  - **Left**: Speaker Name (Bold)
  - **Right**: Dialogue
- Auto-detects Tamil script and applies proper font (`Arial Unicode MS`)

**Output**:  
A `Srt to docx output/` folder inside the provided directory containing `.docx` versions of the `.srt` files.

---

## 📦 Requirements

Install the required dependencies using:

```bash
pip install -r requirements.txt
