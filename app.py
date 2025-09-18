
import os
import pandas as pd
from flask import Flask, request, send_file, render_template_string
from Semi_ATE import STDF

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
WEB_FOLDER = 'web'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        t1_file = request.files['t1_file']
        t2_file = request.files['t2_file']
        test_nums = request.form.getlist('test_num[]')
        delta_limits = request.form.getlist('delta_limit[]')

        if t1_file and t2_file:
            t1_path = os.path.join(UPLOAD_FOLDER, t1_file.filename)
            t2_path = os.path.join(UPLOAD_FOLDER, t2_file.filename)
            t1_file.save(t1_path)
            t2_file.save(t2_path)

            output_path = process_stdf(t1_path, t2_path, test_nums, delta_limits)
            return send_file(output_path)

    with open(os.path.join(WEB_FOLDER, 'index.html'), 'r', encoding='utf-8') as f:
        html = f.read()
    with open(os.path.join(WEB_FOLDER, 'style.css'), 'r', encoding='utf-8') as f:
        css = f.read()
    
    return render_template_string(html.replace('<link rel="stylesheet" href="style.css">', f"<style>{css}</style>"))


def process_stdf(t1_path, t2_path, test_nums, delta_limits):
    def extract_results(filepath):
        results = {}
        test_info = {}
        for record in STDF.records_from_file(filepath):
            if record.id == 'MIR':
                part_id = None
                soft_bin = None
                buffer = []
            elif record.id == 'PTR':
                test_num = str(record.get_value('TEST_NUM'))
                result = record.get_value('RESULT')
                test_txt = record.get_value('TEST_TXT') or ''
                units = record.get_value('UNITS') or ''
                if test_num not in test_info:
                    test_info[test_num] = {'TEST_TXT': test_txt, 'UNITS': units}
                if result is not None:
                    buffer.append((test_num, result))
            elif record.id == 'PRR':
                part_id = record.get_value('PART_ID')
                soft_bin = record.get_value('SOFT_BIN')
                if soft_bin == 1:
                    results[part_id] = {test_num: result for test_num, result in buffer}
        return results, test_info

    t1_data, test_info = extract_results(t1_path)
    t2_data, _ = extract_results(t2_path)

    common_parts = set(t1_data.keys()) & set(t2_data.keys())
    skipped_parts = sorted(set(t1_data.keys()) ^ set(t2_data.keys()))

    final_rows = []
    header_clusters = []

    for test_num, delta_limit in zip(test_nums, delta_limits):
        delta_limit = float(delta_limit)
        test_txt = test_info.get(test_num, {}).get('TEST_TXT', '')
        units = test_info.get(test_num, {}).get('UNITS', '')
        header_clusters.append((test_num, test_txt, delta_limit, units))

    for part_id in sorted(common_parts):
        row = [part_id]
        for test_num, test_txt, delta_limit, units in header_clusters:
            t1_val = t1_data[part_id].get(test_num)
            t2_val = t2_data[part_id].get(test_num)
            if t1_val is not None and t2_val is not None:
                delta = t2_val - t1_val
                passed = abs(delta) <= delta_limit
                pf = 'PASSED' if passed else 'FAILED'
                row.extend([f"{t1_val:.5f}", f"{t2_val:.5f}", f"{delta:.5f}", pf])
            else:
                row.extend(['', '', '', ''])
        final_rows.append(row)

    # Build HTML table
    header_html = "<tr><th rowspan='2'>Device#</th>"
    for test_num, test_txt, delta_limit, units in header_clusters:
        header_html += f"<th colspan='4'>{test_num}<br>{test_txt}<br>Limit: {delta_limit}<br>{units}</th>"
    header_html += "</tr><tr>"
    for _ in header_clusters:
        header_html += "<th>T1</th><th>T2</th><th>Δ</th><th>P/F</th>"
    header_html += "</tr>"

    rows_html = ""
    for row in final_rows:
        rows_html += "<tr>"
        rows_html += f"<td>{row[0]}</td>"
        for i in range(1, len(row), 4):
            t1, t2, delta, pf = row[i:i+4]
            pf_class = 'passed' if pf == 'PASSED' else 'failed'
            rows_html += f"<td>{t1}</td><td>{t2}</td><td>{delta}</td><td class='{pf_class}'>{pf}</td>"
        rows_html += "</tr>"

    skipped_html = "<p><strong>Skipped PART_IDs:</strong><br>" + ", ".join(skipped_parts) + "</p>"

    html_output = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset='UTF-8'>
    <style>
    .scroll-container {{ width: 100%; height: 600px; overflow: auto; border: 1px solid #ccc; }}
    .scroll-table {{ border-collapse: collapse; white-space: nowrap; }}
    th, td {{ padding: 8px; text-align: center; border: 1px solid #ccc; }}
    .passed {{ background-color: #c6efce; }}
    .failed {{ background-color: #f4cccc; }}
    </style>
    </head>
    <body>
    <h2>Delta Comparison Results</h2>
    <div class='scroll-container'>
    <table class='scroll-table'>
    {header_html}
    {rows_html}
    </table>
    </div>
    {skipped_html}
    </body>
    </html>
    """

    output_path = os.path.join(UPLOAD_FOLDER, "output.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_output)
    return output_path

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
