import os
import pandas as pd
from io import StringIO
from pystdf.IO import Parser
from pystdf.Writers import TextWriter

def parse_stdf_to_device_table(stdf_path):
    p = Parser(inp=open(stdf_path, 'rb'))
    captured_output = StringIO()
    p.addSink(TextWriter(captured_output))
    p.parse()

    atdf = captured_output.getvalue().split('\n')
    ptr_lines = [line for line in atdf if line.startswith('PTR')]

    print("Sample PTR lines:")
    for line in ptr_lines[:5]:
        print(line)

    device_data = {}
    device_index = -1

    for line in ptr_lines:
        parts = line.split('|')
        if len(parts) >= 7:
            try:
                test_num = parts[1].strip()
                result = float(parts[6])

                # Detect start of a new device
                if test_num == '1':
                    device_index += 1

                if device_index not in device_data:
                    device_data[device_index] = {}
                device_data[device_index][test_num] = result
            except (ValueError, IndexError):
                continue

    df = pd.DataFrame.from_dict(device_data, orient='index')
    df.index.name = 'Device'
    df = df.sort_index()
    return df

# Auto-detect .stdf files
stdf_files = [f for f in os.listdir('.') if f.endswith('.stdf')]

if not stdf_files:
    print("No .stdf files found.")
elif len(stdf_files) == 1:
    selected_file = stdf_files[0]
else:
    print("Multiple .stdf files found:")
    for i, file in enumerate(stdf_files):
        print(f"{i + 1}: {file}")
    choice = int(input("Enter the number of the file to process: ")) - 1
    selected_file = stdf_files[choice]

# Parse and display raw data table
df = parse_stdf_to_device_table(selected_file)
print("\nRaw data table (each row = device, each column = test number):")
print(df.head(10))
print(f"\nTotal devices parsed: {df.shape[0]}")
print(f"Total unique tests: {df.shape[1]}")
