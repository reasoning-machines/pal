"""Sample usage:
python -u scripts/aqua_eval.py --path "datasets/outputs/aqua_pal_outputs.jsonl" --type code|grep -e "Acc" -e "Eval"
"""

from importlib import reload
import os
import pandas as pd
from tqdm import tqdm
from contextlib import contextmanager
import signal
from glob import glob
import shutil

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

import numpy as np

def evaluate_code_prompt(path):
    def _parse_option(option: str, question: str):
        
        solution = question.split(option)[1].split(")")[0]
        if "none" in solution.lower():
            return None
        # remove all non-numerical characters
        solution = "".join([c for c in solution if c.isdigit() or c == "."])
        if solution[0] == "." and solution.count(".") > 1:
            solution = solution[1:]
        solution = float(solution)
        return solution
    
    def find_closest_option(result: float, question: str):
        options = ["(a)", "(b)", "(c)", "(d)", "(e)"]
        option_solutions = [_parse_option(option, question) for option in options if _parse_option(option, question) is not None]
        has_None = len(option_solutions) < len(options)
            
        closest_option = options[np.argmin(np.abs(np.array(option_solutions) - result))]
        closest_option_dist = np.abs(_parse_option(closest_option, question) - result)
        
        # if the closest option is too far away (relative difference > 0.1), then return None
        relative_dist = abs(closest_option_dist / (result + 1e-6))
        # print(relative_dist, _parse_option(closest_option, question), result)
        if relative_dist > 10 and has_None:
            return "(e)"
        return closest_option
            
    data = read_json(path)
    num_corr = 0
    for rec_idx, row in tqdm(data.iterrows(), total=len(data)):
        question = row['question'].split("Question: ")[-1].split("#")[0]
        # print(question)
        soln = row["generated_answer"]
        soln = soln.split("\n\n\n")[0].strip()
        # replace line "from sympy import *" from the solution
        soln_lines = soln.split("\n")
        soln_lines = [line for line in soln_lines if "from sympy import *" not in line]
        
        # next repair the `solve` call. If it does not have a `dict=True` argument, then add it
        # find the line with `solve` in it
        for i, soln_line in enumerate(soln_lines):
            if "solve(" in soln_line and "dict=True" not in soln_line:
                soln_lines[i] = soln_line.replace(")", ", dict=True)")
                # the next line should be sol[n] -> sol[0][n]
                j = i + 1
                while "sol[" in soln_lines[j]:
                    if "sol[0][" not in soln_lines[j]:
                        soln_lines[j] = soln_lines[j].replace("[", "[0][")
                    j += 1
    
            
        
        soln = "\n".join(soln_lines)
        soln = "from sympy import *\nimport numpy as np\nimport math\nfrom math import sqrt\n" + soln
        result = None
        # delete pycache
        os.system("rm -rf __pycache__")
        os.system("rm -f temp_result.pyc")

        # soln is a python string, write it to a file, and then run it, get the output
        with open("temp_result.py", "w") as f:
            f.write(soln)
            

        try:
            import temp_result

            reload(temp_result)
            correct_solution_option = row["answer"]
            
            
            with timeout(5):
                exec(soln)

                result = float(temp_result.solution())
                del temp_result
                closest_option = find_closest_option(result, question)
                
        except Exception as e:
            pass            

        if not (isinstance(result, int) or isinstance(result, float)):
            continue
        # compare float values
        is_corr = closest_option == correct_solution_option
        num_corr += int(is_corr)

    print(f"Accuracy = {num_corr / len(data):.2%} ({num_corr}/{len(data)})")
    return num_corr / len(data)


def evaluate_text_prompt(path):
    data = read_json(path)
    num_corr = 0
    for i, row in tqdm(data.iterrows(), total=len(data)):

        try:
            generated_soln =  row["generated_answer"].strip().split("So the answer is ")[1].split(".")[0]
            
        except:
            generated_soln = "(e)"
        correct_solution = row["answer"]
        is_corr = generated_soln == correct_solution
        num_corr += int(is_corr)

    print(f"Accuracy = {num_corr / len(data):.2%} ({num_corr}/{len(data)})")
    return num_corr / len(data)

def check_corr(result: float, correct_solution: float):
    return abs(result - correct_solution) < 1e-3

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
