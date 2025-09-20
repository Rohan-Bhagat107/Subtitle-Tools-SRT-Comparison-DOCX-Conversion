# # # Input-> .srt
# # # Output-> .txt(Report file)
import re
from datetime import datetime
from difflib import SequenceMatcher
import os
from logging import exception

# Function for validating user input
def validator(file_path):
    if os.path.exists(file_path): # Checking the received path exists or not
        if not os.path.isdir(file_path):
            basename=os.path.basename(file_path) # Getting the file name
            if basename.endswith(".srt"):
                return True
            else:
                print("Invalid file path received!")
                return False
        else:
            print("File path expected!")
            return False
    else:
        print("Invalid path received!")
        return  False

# Function ofr reading the srt
def parse_srt(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        content = f.read().strip()
    blocks = re.split(r'\n{2,}', content)
    subtitles = []

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            index = lines[0].strip()
            timecode = lines[1].strip()
            text = " ".join(lines[2:]).strip()
            start_time, end_time = [t.strip() for t in timecode.split('-->')]
            subtitles.append((index, start_time, end_time, text))

    return subtitles

# Function for sequence matching  for subtitles
def align_words(ref_words, hyp_words):
    matcher = SequenceMatcher(None, ref_words, hyp_words)
    original, updated = [], []
    insertions = deletions = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            for w1 in ref_words[i1:i2]:
                original.append(f"[{w1}]")
            for w2 in hyp_words[j1:j2]:
                updated.append(f"[{w2}]")

        elif tag == 'replace':
            ref_segment = ref_words[i1:i2]
            hyp_segment = hyp_words[j1:j2]
            max_len = max(len(ref_segment), len(hyp_segment))

            for idx in range(max_len):
                if idx < len(ref_segment) and idx < len(hyp_segment):
                    original.append(f"[{ref_segment[idx]}]")
                    updated.append(f"[{hyp_segment[idx]}]")
                elif idx < len(ref_segment):
                    original.append(f"[{ref_segment[idx]}]")
                    updated.append("[-]")
                    deletions += 1
                else:
                    original.append("[-]")
                    updated.append(f"[{hyp_segment[idx]}]")
                    insertions += 1

        elif tag == 'delete':
            for w in ref_words[i1:i2]:
                original.append(f"[{w}]")
                updated.append("[-]")
                deletions += 1

        elif tag == 'insert':
            for w in hyp_words[j1:j2]:
                original.append("[-]")
                updated.append(f"[{w}]")
                insertions += 1

    return original, updated, insertions, deletions


# Function for comparing two srt files(time and subtitle)
def compare_srt(original_file, updated_file):
    org_subs = parse_srt(original_file)
    new_subs = parse_srt(updated_file)

    max_len = max(len(org_subs), len(new_subs))
    output = []

    for i in range(max_len):
        if i >= len(org_subs):
            continue
        if i >= len(new_subs):
            continue

        _, org_start, org_end, ref_text = org_subs[i]
        _, new_start, new_end, hyp_text = new_subs[i]

        org_words = ref_text.split()
        new_words = hyp_text.split()

        org_ref, new_hyp, ins, dels = align_words(org_words, new_words)
        output.append(f"{'-' * 20} Segment {i + 1} {'-' * 20}")
        output.append(f"Reference Time:   {org_start} --> {org_end}")
        output.append(f"Hypothesis Time:  {new_start} --> {new_end}\n")
        output.append(f"Reference Text:\n{ref_text}\n")
        output.append(f"Hypothesis Text:\n{hyp_text}\n")
        output.append(f"Insertions (+): {ins}")
        output.append(f"Deletions  (-): {dels}\n")
        output.append(f"Aligned Reference:\n{' '.join(org_ref)}\n")
        output.append(f"Aligned Hypothesis:\n{' '.join(new_hyp)}\n")

    with open(os.path.join(os.path.dirname(original_file),f"Report_{os.path.basename(original_file).replace('.srt','.txt')}"), "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print("Report generated successfully!")

if __name__ == "__main__":
    try:
        file1 = input("Please enter your reference srt file path: ")
        if not validator(file1):
            raise Exception()
    except Exception as e:
        print("Please try again!")
    else:
        try:
            file2 = input("Please enter your hypothesis srt file path: ")
            if not validator(file2):
                raise  Exception()
        except Exception as e:
            print("Please try again!")
        else:
                compare_srt(file1, file2)






# --------------------------Working (With other report format) ---------------------------------------
#
# import re
# from datetime import datetime
# from difflib import SequenceMatcher
# import os
# from logging import exception
#
# # Function for validating user input
# def validator(file_path):
#     if os.path.exists(file_path):  # Checking the received path exists or not
#         if not os.path.isdir(file_path):
#             basename = os.path.basename(file_path)  # Getting the file name
#             if basename.endswith(".srt"):
#                 return True
#             else:
#                 print("Invalid file path received!")
#                 return False
#         else:
#             print("File path expected!")
#             return False
#     else:
#         print("Invalid path received!")
#         return False
#
# # Function for reading the srt
# def parse_srt(file_path):
#     with open(file_path, 'r', encoding='utf-8-sig') as f:
#         content = f.read().strip()
#     blocks = re.split(r'\n{2,}', content)
#     subtitles = []
#
#     for block in blocks:
#         lines = block.strip().split('\n')
#         if len(lines) >= 3:
#             index = lines[0].strip()
#             timecode = lines[1].strip()
#             text = " ".join(lines[2:]).strip()
#             start_time, end_time = [t.strip() for t in timecode.split('-->')]
#             subtitles.append((index, start_time, end_time, text))
#
#     return subtitles
#
# # Function for sequence matching for subtitles at character level
# def align_chars(ref_text, hyp_text):
#     matcher = SequenceMatcher(None, ref_text, hyp_text)
#     original, updated = [], []
#     insertions = deletions = 0
#
#     for tag, i1, i2, j1, j2 in matcher.get_opcodes():
#         if tag == 'equal':
#             # Equal characters, just append
#             original.extend(ref_text[i1:i2])
#             updated.extend(hyp_text[j1:j2])
#         elif tag == 'replace':
#             # Replace characters, mark with brackets
#             original.extend([f"[{c}]" for c in ref_text[i1:i2]])
#             updated.extend([f"[{c}]" for c in hyp_text[j1:j2]])
#             # Count insertions and deletions by difference in length
#             deletions += (i2 - i1)
#             insertions += (j2 - j1)
#         elif tag == 'delete':
#             original.extend([f"[{c}]" for c in ref_text[i1:i2]])
#             updated.extend(["[-]"] * (i2 - i1))
#             deletions += (i2 - i1)
#         elif tag == 'insert':
#             original.extend(["[-]"] * (j2 - j1))
#             updated.extend([f"[{c}]" for c in hyp_text[j1:j2]])
#             insertions += (j2 - j1)
#
#     return original, updated, insertions, deletions
#
# # Function for comparing two srt files (time and subtitle)
# def compare_srt(original_file, updated_file):
#     org_subs = parse_srt(original_file)
#     new_subs = parse_srt(updated_file)
#
#     max_len = max(len(org_subs), len(new_subs))
#     output = []
#
#     for i in range(max_len):
#         if i >= len(org_subs):
#             continue
#         if i >= len(new_subs):
#             continue
#
#         _, org_start, org_end, ref_text = org_subs[i]
#         _, new_start, new_end, hyp_text = new_subs[i]
#
#         org_ref, new_hyp, ins, dels = align_chars(ref_text, hyp_text)
#         output.append(f"{'-' * 20} Segment {i + 1} {'-' * 20}")
#         output.append(f"Reference Time:   {org_start} --> {org_end}")
#         output.append(f"Hypothesis Time:  {new_start} --> {new_end}\n")
#         output.append(f"Reference Text:\n{ref_text}\n")
#         output.append(f"Hypothesis Text:\n{hyp_text}\n")
#         output.append(f"Insertions (+): {ins}")
#         output.append(f"Deletions  (-): {dels}\n")
#         output.append(f"Aligned Reference:\n{''.join(org_ref)}\n")
#         output.append(f"Aligned Hypothesis:\n{''.join(new_hyp)}\n")
#
#     report_path = os.path.join(os.path.dirname(original_file),
#                                f"Report_{os.path.basename(original_file).replace('.srt', '.txt')}")
#     with open(report_path, "w", encoding="utf-8") as f:
#         f.write("\n".join(output))
#
#     print("Report generated successfully!")
#
# if __name__ == "__main__":
#     try:
#         file1 = input("Please enter your reference srt file path: ")
#         if not validator(file1):
#             raise Exception()
#     except Exception as e:
#         print("Please try again!")
#     else:
#         try:
#             file2 = input("Please enter your hypothesis srt file path: ")
#             if not validator(file2):
#                 raise Exception()
#         except Exception as e:
#             print("Please try again!")
#         else:
#             compare_srt(file1, file2)
