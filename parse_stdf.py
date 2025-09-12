import sys
import json
from ezstdf import STDF

def parse_stdf(file_path):
    stdf = STDF(file_path)
    results = []
    for rec in stdf.records:
        if rec.rec_typ == 10 and rec.rec_sub == 20:  # Assuming this is the test summary record
            results.append({
                'device': rec.hard_bin,
                'test_time': rec.test_time,
                'test_result': rec.test_num_passed
            })
    return results

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 parse_stdf.py input.stdf output.json")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    parsed_data = parse_stdf(input_file)

    with open(output_file, 'w') as f:
        json.dump(parsed_data, f, indent=2)


# Note: Adjust the record type check (rec_typ and rec_sub) and the fields to match what you want to extract.