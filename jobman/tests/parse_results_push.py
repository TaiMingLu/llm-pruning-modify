import os
import re
import glob
import ast
import json
import tabulate
import argparse
from tqdm import tqdm

pattern = "jobs/yx1168/0000**/logs/command_worker_0*.log"

ppl_tasks = [
    "wikitext2",
    "wikitext",
    "c4",
    "dclm",
    "cnn_dailymail"
]

all_keys = [
    'model', 'training',
    'c4-ppl', 'wikitext-ppl', 'wikitext2-ppl', 'cnn_dailymail-ppl', 'dclm-ppl', 
    'winogrande-acc', 'arc_challenge-acc', 'arc_challenge-acc_norm', 'arc_easy-acc', 'arc_easy-acc_norm', 
    'hellaswag-acc', 'hellaswag-acc_norm', 'truthfulqa_mc1-acc', 'truthfulqa_mc2-acc', 'piqa-acc', 'piqa-acc_norm', 
    'sciq-acc', 'sciq-acc_norm', 'boolq-acc',  'anli_r1-acc', 'anli_r2-acc', 'anli_r3-acc', 
    'openbookqa-acc', 'openbookqa-acc_norm', 'rte-acc', 'mmlu-acc', 'record-em', 'record-f1', 
    'model_path', 'log_path'
]

model_types = [
    "llama3_8b",
    "llama3-8b",
    "llama3.1_8b",
    "llama3.1-8b",
    "llama3_4b_depth",
    "llama3-4b-depth",
    "llama3.1_4b_depth",
    "llama3.1-4b-depth",
    "llama3_4b_width",
    "llama3-4b-width",
    "llama3.1_4b_width",
    "llama3.1-4b-width",
    "llama3_1.5b_depth",
    "llama3-1.5b-depth",
    "llama3.1-1b",
    "llama3.1_1.5b_depth",
    "llama3.1-1.5b-depth",
    "llama3_2b_depth",
    "llama3-2b-depth",
    "llama3.1_2b_depth",
    "llama3.1-2b-depth",
    "llama3_3b_depth",
    "llama3-3b-depth",
    "llama3.1_3b_depth",
    "llama3.1-3b-depth",
    "llama3.1_minitron_depth",
    "llama3.1_minitron_width",
]

training_types = [
    "HF",
    "L200",
    "S50",
    "S250",
    "minitron",
    "orbax",
    "2000_steps",
    "4000_steps",
]

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def maybe_format_as_percentage(value):
    if isinstance(value, float) and 0 <= value <= 1:
        return f"{value * 100:.2f}%"
    elif isinstance(value, float) and value > 1:
        return f"{value:.2f}"
    return value

def push_to_google_sheet(rows):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]  # or .readonly

    creds = Credentials.from_service_account_file("service-account.json", scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)

    # SAMPLE_SPREADSHEET_ID = "1r0HmtlhWnZceOI_Do-FVuMQtJ8INr1LlkxU164FpB6A"
    SAMPLE_SPREADSHEET_ID = "1TnichIIOAisBc_SKYxiGrA6Vj9hF7vDcw7TD82F0jHk"
    # SAMPLE_RANGE_NAME = "automatic-push-test!A1:Z100"
    SAMPLE_RANGE_NAME = "automatic-push-test!A1:ZZ500"
    
    # all_keys = list({k for r in rows for k in r.keys()})

    # 2️⃣ Build a 2-D array: header + rows (fill missing values with "")
    values = [all_keys]
    for r in rows:
        row_data = [maybe_format_as_percentage(r.get(k, "")) for k in all_keys]
        values.append(row_data)

    try:
        service.spreadsheets().values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=SAMPLE_RANGE_NAME,
            valueInputOption="RAW",      # or "USER_ENTERED"
            body={"values": values},
        ).execute()
        print(f"✅ Uploaded {len(rows)} rows, {len(all_keys)} columns.")
        print(f"See results at https://docs.google.com/spreadsheets/d/{SAMPLE_SPREADSHEET_ID}/edit#gid=0")
    except HttpError as e:
        print("❌ Upload failed:", e)

rows = []
for log_path in tqdm(glob.glob(pattern)):
    row = {}
    with open(log_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("Config param load_parameters_path"):
                
                model_path = line.split(": ")[1].strip()
                if model_path.startswith("gs://") and 'direct' in model_path:
                    for model_type in model_types:
                        if model_type in model_path:
                            if row.get('model', None) and row['model'] != model_type:
                                rows.append(row)
                                row = {}
                            row["model"] = model_type
                    used_training = []
                    for training_type in training_types:
                        if training_type in model_path:
                            used_training.append(training_type)
                    row["training"] = "+".join(used_training)
                    # if not row.get("model", None):
                    #     print(model_path)
                    #     import pdb; pdb.set_trace()
                    # if row.get("model", None) and row.get("training", None) is None:
                    #     print(model_path)
                    #     import pdb; pdb.set_trace()
                        # row["training"] = "HF_S50" if "hf/" in model_path else "L200_S50"
                        
            if any(line.startswith(ppl_task) for ppl_task in ppl_tasks):
                # print(line)
                try:
                    ppl_task, ppl = line.strip().split(" ")
                    row[f"{ppl_task}-ppl"] = float(ppl)
                except:
                    pass
            if line.startswith("{"):
                # print(line)
                line = re.sub(r'np\.float64\(([^)]+)\)', r'\1', line)
                d = ast.literal_eval(line)
                if 'alias' not in d:
                    continue
                task = d['alias']
                row[f"{task}-acc"] = d.get("acc,none", None)
                row[f"{task}-acc_norm"] = d.get("acc_norm,none", None)
                row[f"{task}-em"] = d.get("em,none", None)
                row[f"{task}-f1"] = d.get("f1,none", None)
                
    # if row.get("training", None) == "orbax":
    #     import pdb; pdb.set_trace()
    if len(row.keys()) > 3:
        row["model_path"] = model_path
        row["log_path"] = log_path
        row = {k: v for k, v in row.items() if v is not None}
        rows.append(row)
        print(os.path.abspath(log_path))
        print(row.keys())
        # import pdb; pdb.set_trace()
        
# for row in rows:
#     print(json.dumps(row, indent=2))
    
rows = sorted(rows, key=lambda r: (r.get("model", ""), r.get("training", "")))

push_to_google_sheet(rows)