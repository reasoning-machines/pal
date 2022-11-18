# Copyright 2022 PAL Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import openai
import time


# GPT-3 API
def call_gpt(prompt, model='code-davinci-002', stop=None, max_tokens=128, temperature=0.):
    for i in range(20):
        try:
            ans = openai.Completion.create(
                            model=model,
                            max_tokens=max_tokens,
                            stop=stop,
                            prompt=prompt,
                            temperature=temperature)
            return ans['choices'][0]['text']
        except openai.error.RateLimitError:
            time.sleep(max(i+1, 3))
    raise RuntimeError('Failed to call GPT API')
