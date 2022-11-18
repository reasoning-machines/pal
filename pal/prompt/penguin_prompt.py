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


PENGUIN_PROMPT = '''
"""
Q: Here is a table where the first line is a header and each subsequent line is a penguin:
name, age, height (cm), weight (kg) 
Louis, 7, 50, 11
Bernard, 5, 80, 13
Vincent, 9, 60, 11
Gwen, 8, 70, 15
For example: the age of Louis is 7, the weight of Gwen is 15 kg, the height of Bernard is 80 cm. 
We now add a penguin to the table:
James, 12, 90, 12
How many penguins are less than 8 years old?
"""

# Put the penguins into a list.
penguins = []
penguins.append(('Louis', 7, 50, 11))
penguins.append(('Bernard', 5, 80, 13))
penguins.append(('Vincent', 9, 60, 11))
penguins.append(('Gwen', 8, 70, 15))

# Add penguin James.
penguins.append(('James', 12, 90, 12))

# Find penguins under 8 years old.
penguins_under_8_years_old = [penguin for penguin in penguins if penguin[1] < 8]

# Count number of perguins under 8.
num_penguin_under_8 = len(penguins_under_8_years_old)
answer = num_penguin_under_8


"""
Q: Here is a table where the first line is a header and each subsequent line is a penguin:
name, age, height (cm), weight (kg) 
Louis, 7, 50, 11
Bernard, 5, 80, 13
Vincent, 9, 60, 11
Gwen, 8, 70, 15
For example: the age of Louis is 7, the weight of Gwen is 15 kg, the height of Bernard is 80 cm.
Which is the youngest penguin?
"""

# Put the penguins into a list.
penguins = []
penguins.append(('Louis', 7, 50, 11))
penguins.append(('Bernard', 5, 80, 13))
penguins.append(('Vincent', 9, 60, 11))
penguins.append(('Gwen', 8, 70, 15))

# Sort the penguins by age.
penguins = sorted(penguins, key=lambda x: x[1])

# Get the youngest penguin's name.
youngest_penguin_name = penguins[0][0]
answer = youngest_penguin_name


"""
Q: Here is a table where the first line is a header and each subsequent line is a penguin:
name, age, height (cm), weight (kg) 
Louis, 7, 50, 11
Bernard, 5, 80, 13
Vincent, 9, 60, 11
Gwen, 8, 70, 15
For example: the age of Louis is 7, the weight of Gwen is 15 kg, the height of Bernard is 80 cm.
What is the name of the second penguin sorted by alphabetic order?
"""

# Put the penguins into a list.
penguins = []
penguins.append(('Louis', 7, 50, 11))
penguins.append(('Bernard', 5, 80, 13))
penguins.append(('Vincent', 9, 60, 11))
penguins.append(('Gwen', 8, 70, 15))

# Sort penguins by alphabetic order.
penguins_alphabetic = sorted(penguins, key=lambda x: x[0])

# Get the second penguin sorted by alphabetic order.
second_penguin_name = penguins_alphabetic[1][0]
answer = second_penguin_name


"""
{question}
"""
'''.strip() + '\n'
