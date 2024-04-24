import os, re
from csv import DictReader

def write_to_brat(jsonl: dict, filename_prefix: str, directory: str):
    # write txt file
    txt = jsonl["text"]
    anns = jsonl["label"]
    with open(os.path.join(directory, "{}.txt".format(filename_prefix)), "w") as f:
        f.write(txt)

    # write ann file
    with open(os.path.join(directory, "{}.ann".format(filename_prefix)), "w") as f:
        f.write("\n".join([
            "T{}\t{} {} {}\t{}".format(
                ann_id+1,
                re.sub(r'\s', '_', ann[2]).replace("|","-"),
                str(ann[0]),
                str(ann[1]),
                re.sub(r'\s', ' ', txt[ann[0]:ann[1]])
            )
            for ann_id, ann in enumerate(sorted(anns, key=lambda x: x[0]))
        ]))

def parse_output(stdout_data):
    output = stdout_data.decode("utf-8")
    context, csvdata = output.split("\nSummary:\n")
    context = [ l for l in context.splitlines() if l ]

    # parse output table
    score_data = {}
    for entry in DictReader(csvdata.splitlines(), delimiter="|"):
        # empty-spaced data item has label class
        label_class = entry[""]
        values = {
            "tp": int(entry["tp"]),
            "fp": int(entry["fp"]),
            "fn": int(entry["fn"]),
            "PR": float(entry["precision"]),
            "RE": float(entry["recall"]),
            "F1": float(entry["f1"]),
        }
        score_data[label_class] = values

    return {
        "scores": score_data,
        "context": context
    }
