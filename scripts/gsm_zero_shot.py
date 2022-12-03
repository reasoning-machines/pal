from importlib import reload
import pandas as pd
from tqdm import tqdm
from contextlib import contextmanager
import signal
from glob import glob
import os

# from https://stackoverflow.com/questions/492519/timeout-on-a-function-call
@contextmanager
def timeout(duration):
    def timeout_handler(signum, frame):
        raise TimeoutError(f"block timedout after {duration} seconds")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(duration)
    try:
        yield
    finally:
        signal.alarm(0)

def read_json(path):
    import json
    rows = []
    with open(path, "r") as f:
        for line in f:
            rows.append(json.loads(line))
    
    task_df = pd.DataFrame(rows)
    return task_df

def evaluate_code_prompt(path):
    data = read_json(path)
    num_corr = 0
    for i, row in tqdm(data.iterrows(), total=len(data)):
        soln = row["generated_answer"].split("\n\n\n")[0].strip() + "\n"
        print(soln)
        soln = fix_function(soln)
        # header = "import spacy\nnlp = spacy.load('en_core_web_sm')\nimport nltk\nimport numpy as np\nimport pandas as pd"
        # soln = header + "\n" + soln
        os.system("rm -rf __pycache__")
        os.system("rm -f temp_result.pyc")
        # soln is a python string, write it to a file, and then run it, get the output
        with open("temp_result.py", "w") as f:
            f.write(soln)

        try:
            import temp_result
            question = row['question'].split("Q: ")[-1].split("#")[0].strip()
            reload(temp_result)
            correct_solution = str(row["answer"])
            print()
            exec(soln)
            with timeout(1):
                result = str(temp_result.solution())
            is_corr = check_corr(result, correct_solution)
            if not is_corr:
                debug_string = f"# Generated answer: \n{soln}\n# Correct answer: {correct_solution}\n# Generated result: {result}\n"
                with open(f"debug/temp_result_error_{i}.py", "w") as fout:
                    fout.write(debug_string)
            num_corr += int(is_corr)
            data.loc[i, "is_correct"] = is_corr
            data.loc[i, "generated_result"] = result
            data.loc[i, "question"] = question
             
        except Exception as e:
            continue
        if not (isinstance(result, int) or isinstance(result, float)):
            continue
        # compare float values


    print(f"Accuracy = {num_corr / len(data):.2%} ({num_corr}/{len(data)})")
    data.to_json("gsm_quco_results.jsonl", orient="records", lines=True)
    return num_corr / len(data)


def fix_function(soln):
    soln_lines = soln.split("\n")
    soln_lines[0] = "    " + soln_lines[0]
    # soln_lines = ["    " + line.strip() for line in soln_lines if line.strip() != "" and "solution" not in line]
    soln_lines = ["def solution():"] + soln_lines
    soln_lines = [line for line in soln_lines if "input(" not in line]
    # if the last line is print, remove it and replace it with return
    if "print" in soln_lines[-1]:
        # remove parenthesis
        soln_lines[-1] = soln_lines[-1].strip().replace("print(", "").replace(")", "")
        # add return
        soln_lines[-1] = "    return " + soln_lines[-1]

    return "\n".join(soln_lines)
    
    

def check_corr(result: float, correct_solution: float, tol: float = 1e-3):
    if result.strip() == correct_solution.strip():
        return 1
    try:
        result = float(result.strip())
        correct_solution = float(correct_solution.strip())
        return abs(result - correct_solution) < tol
    except:
        return 0


def evaluate_text_prompt(path):
    data = read_json(path)
    num_corr = 0
    for i, row in tqdm(data.iterrows(), total=len(data)):
        try:
            question = row['question'].split("Q: ")[-1].split("A:")[0].strip()
            generated_soln = row["generated_answer"].strip().split("The answer is ")[-1].strip()
        except:
            generated_soln = -100000
        correct_solution =str(row["answer"])
        is_corr = check_corr(generated_soln, correct_solution)
        if not is_corr:
            print(f"result: {row['generated_answer']}, correct_solution: {correct_solution}, is_corr: {is_corr}")

        num_corr += int(is_corr)
        data.loc[i, "is_correct"] = is_corr
        data.loc[i, "generated_result"] = generated_soln
        data.loc[i, "question"] = question
        

    print(f"Accuracy = {num_corr / len(data):.2%} ({num_corr}/{len(data)})")
    data.to_json("gsm_cot_results.jsonl", orient="records", lines=True)
    return num_corr / len(data)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default="data/quco/quco_test.jsonl")
    parser.add_argument("--type", type=str, default="code")
    args = parser.parse_args()
    if args.type == "code":
        func = evaluate_code_prompt
    else:
        func = evaluate_text_prompt
    if "*" in args.path:
        avg_acc = 0
        for path in glob(args.path):
            print(f"Evaluating {path}")
            avg_acc += func(path)
        print(f"Average accuracy = {avg_acc / len(glob(args.path)):.2%}")
    else:
        func(args.path)
