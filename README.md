# PAL:  Program-Aided Language Model
Repo for paper, PAL: Program-Aided Language Model.

In PAL, Large Language Model solves reasoning problems that involve complex arithmetic and procedural tasks by generating reasoning chains of **text and code**.  It offloads the execution of the code to a program runtime, in our case, a Python interpreter. In our paper, we implement PAL using a few-shot prompting approach. 

This repo provides an interactive implementation of PAL.

## Installation
Clone this repo and install with `pip`.
```
git clone https://github.com/luyug/pal
pip install -e ./pal
```

Before running the scripts, set the OpenAI key,
```export OPENAI_API_KEY='sk-...'```
## Interactive Usage
The core components of the `pal` package are the Interface classes. Specifically, `ProgramInterface` connects the LLM backend, a Python backend and user prompts.
```
import pal
from pal.prompt import math_prompts

interface = interface.ProgramInterface(
  model='code-davinci-002',
	stop='\n\n\n', # stop generation str for Codex API
	get_answer_expr='solution()' # python expression evaluated after generated code to obtain answer 
)

question = 'xxxxx'
prompt = math_prompts.MATH_PROMPT.format(question=question)
answer = interface.run(prompt)
```
Here, the `interface` 's `run`  method will run generation with the OpenAI API, run the generated snippet and then evaluate `get_answer_expr` (here `solution()`) to obtain the final answer.  

User should set `get_answer_expr` based on the prompt.

## Inference Loop
We provide simple inference loops in the `scripts/` folder.
```
python scripts/{colored_objects|gsm|date_understanding|penguin}_eval.py
``` 
