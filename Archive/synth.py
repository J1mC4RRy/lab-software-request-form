import pandas as pd
import random
from datetime import datetime, timedelta



# Number of rows
N = 100



# Load software list from CSV
software_df = pd.read_csv('software_list.csv', encoding='ISO-8859-1')
software_list = software_df['application-name'].tolist()

# Generate synthetic data
data = {
    'user-email': [f"user{i}@unimelb.edu.com" for i in range(N)],
    'subject-code': [f"SUBJ{random.randint(1000, 9999)}" for _ in range(N)],
    'software-list': [', '.join(random.sample(software_list, random.randint(1, 5))) for _ in range(N)],
    'DateTime': [(datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d %H:%M:%S') for _ in range(N)]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('synthetic_data.csv', index=False)

print("Synthetic dataset created and saved as 'synthetic_data.csv'")
