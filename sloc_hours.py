import random

import pandas as pd
import numpy as np


num_rows = 4000  

# Generate activity_id. Activity refers to the project or charge number associated with each Source Lines of Code (SLOC) change
activity_id = np.arange(1, num_rows + 1)

programming_languages = np.random.choice(['Simulink', 'C#', 'Ada'], size=num_rows)

# Generate random SLOC
sloc = np.random.randint(300, 1101, size=num_rows)

# Define base hours per SLOC for each programming language
base_hours_per_sloc = {
    'Simulink': 3.0,  
    'C#': 2.7,      
    'Ada': 3.3      
}

# Generate hours based on SLOC and programming language with some randomness
hours = []
for lang, lines in zip(programming_languages, sloc):
    base_hours = lines * base_hours_per_sloc[lang]
    random_factor1 = random.randrange(-200, 400)
    random_factor2 = np.random.uniform(0.9, 1.1)
    hours.append(int(base_hours * random_factor2 + random_factor1))

# Create the Dataframe
df = pd.DataFrame({
    'activity_id': activity_id,
    'programming_language': programming_languages,
    'sloc': sloc,
    'hours': hours
})

df.set_index('activity_id', inplace=True)
df.to_csv('activities.csv')