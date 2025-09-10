import pandas as pd
from faker import Faker
import random

fake = Faker()
data = []
hardware_requests = ['Camera', 'Battery', 'RAM', 'Display', 'Processor']
software_requests = ['OS', 'Application Suite', 'Security Software', 'UI/UX']

for i in range(200000):
    user_id = fake.uuid4()
    feature_type = random.choice(['Hardware', 'Software'])
    hardware_request = random.choice(hardware_requests) if feature_type == 'Hardware' else None
    software_request = random.choice(software_requests) if feature_type == 'Software' else None
    description = fake.sentence(nb_words=10)
    
    data.append([user_id, feature_type, hardware_request, software_request, description])

df = pd.DataFrame(data, columns=['User Id', 'Type of feature', 'Hardware Request', 'Software Request', 'Brief Description'])

# Drop rows with any missing values (for this project, it might be fine to keep them)
# The next line is not necessary with the corrected code below
# df_cleaned = df.dropna(how='all') 

# Drop duplicate entries
df_cleaned = df.drop_duplicates()

# Separate the datasets - THIS IS THE FIX
hardware_df = df_cleaned[df_cleaned['Type of feature'] == 'Hardware']
software_df = df_cleaned[df_cleaned['Type of feature'] == 'Software']

# ... (rest of your code to create df_cleaned, hardware_df, and software_df)

# Rank Hardware Requests - THIS SECTION IS NEEDED
hardware_ranking = hardware_df['Hardware Request'].value_counts().reset_index()
hardware_ranking.columns = ['Hardware Feature', 'Request Count']
hardware_ranking['Rank'] = hardware_ranking['Request Count'].rank(ascending=False, method='min')

# Rank Software Requests - THIS SECTION IS ALSO NEEDED
software_ranking = software_df['Software Request'].value_counts().reset_index()
software_ranking.columns = ['Software Feature', 'Request Count']
software_ranking['Rank'] = software_ranking['Request Count'].rank(ascending=False, method='min')

# Save the final results to CSV files
hardware_ranking.to_csv('hardware_ranking.csv', index=False)
software_ranking.to_csv('software_ranking.csv', index=False)