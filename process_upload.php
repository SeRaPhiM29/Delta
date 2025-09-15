import sys
import json
from ezstdf.stdf_reader import StdfReader

def parse_stdf(file_path):
    results = []

    for record in StdfReader(file_path):
        if record.id == 'PTR':  # Parametric Test Record
            results.append({
                'test_number': record.test_num,
                'site_num': record.site_num,
                'result': record.result,
                'test_text': record.test_txt,
                'head_num': record.head_num
            })

    return results

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 parse_stdf.py input.stdf output.json")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        parsed_data = parse_stdf(input_file)
        with open(output_file, 'w') as f:
            json.dump(parsed_data, f, indent=2)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
