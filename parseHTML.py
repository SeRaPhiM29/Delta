import os
import pandas as pd
from Semi_ATE import STDF

# Step 1: Detect .stdf files
stdf_files = [f for f in os.listdir('.') if f.lower().endswith('.stdf')]
if not stdf_files:
    print("No .stdf files found.")
    exit()

# Step 2: Choose the first file
selected_file = stdf_files[0]
print(f"Parsing: {selected_file}")

# Step 3: Parse and collect PTR records with PART_ID
ptr_records = []
current_part_id = None

for record in STDF.records_from_file(selected_file):
    if record.id == 'PRR':
        current_part_id = record.get_value('PART_ID')
    elif record.id == 'PTR' and current_part_id is not None:
        ptr_records.append({
            'TEST_NUM': record.get_value('TEST_NUM'),
            'TEST_TXT': record.get_value('TEST_TXT') or '',
            'UNITS': record.get_value('UNITS') or '',
            'PART_ID': current_part_id,
            'RESULT': record.get_value('RESULT')
        })

# Step 4: Convert to DataFrame and pivot
df = pd.DataFrame(ptr_records)
pivot_df = df.pivot_table(index=['TEST_NUM', 'TEST_TXT', 'UNITS'], columns='PART_ID', values='RESULT')

# Step 5: Export to scrollable HTML with both scrollbars
html_table = pivot_df.to_html(classes='scroll-table', border=1)

html_output = f"""
<!DOCTYPE html>
<html>
<head>
<style>
.scroll-container {{
    width: 100%;
    height: 600px;
    overflow: auto; /* Enables both horizontal and vertical scrollbars */
    border: 1px solid #ccc;
}}
.scroll-table {{
    border-collapse: collapse;
    white-space: nowrap; /* Prevents wrapping for wide tables */
}}
th, td {{
    padding: 8px;
    text-align: center;
    border: 1px solid #ccc;
}}
</style>
</head>
<body>
<div class="scroll-container">
{html_table}
</div>
</body>
</html>
"""

with open("output.html", "w") as f:
    f.write(html_output)

print("✅ HTML table with both scrollbars saved to output.html")
