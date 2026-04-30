from weasyprint import HTML
from jinja2 import Template

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Helvetica', sans-serif; margin: 40px; color: #333; }
        .header { text-align: center; border-bottom: 3px solid #004a99; padding-bottom: 10px; margin-bottom: 20px; }
        .section-title { background-color: #004a99; color: white; padding: 5px 10px; font-size: 1.2em; margin-top: 25px; border-radius: 3px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px; }
        .label { font-weight: bold; color: #555; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
        th { background-color: #f9f9f9; width: 60%; }
        .status-pass { color: green; font-weight: bold; }
        .status-fail { color: red; font-weight: bold; }
        .status-not-tested { color: #888; font-style: italic; }
        .footer { margin-top: 50px; font-size: 0.85em; color: #888; border-top: 1px solid #eee; padding-top: 10px; text-align: center; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Biomedical Equipment Inspection Report</h1>
        <p>Organization: MEDINNOVA</p>
    </div>
    
    <div class="section-title">Device Identification</div>
    <div class="grid">
        <div>
            <p><span class="label">Device Name:</span> {{ record.device_name }}</p>
            <p><span class="label">Manufacturer:</span> {{ record.manufacturer }}</p>
            <p><span class="label">Model:</span> {{ record.model_number }}</p>
            <p><span class="label">Purchase Date:</span> {{ record.purchase_date }}</p>
        </div>
        <div>
            <p><span class="label">Serial No:</span> {{ record.serial_number }}</p>
            <p><span class="label">Job Card No:</span> {{ record.job_card_no }}</p>
            <p><span class="label">Department:</span> {{ record.department }}</p>
        </div>
    </div>

    <div class="section-title">Technical Specifications</div>
    <div class="grid">
        <div><span class="label">Operating Voltage:</span> {{ record.operating_voltage }}</div>
        <div><span class="label">Battery Spec:</span> {{ record.battery_spec }}</div>
    </div>

    <div class="section-title">Inspection Summary</div>
    <div class="grid">
        <div><span class="label">Date:</span> {{ record.date }}</div>
        <div><span class="label">Inspected By:</span> {{ record.inspected_by }}</div>
        <div><span class="label">Technician:</span> {{ record.technician }}</div>
    </div>

    <div class="section-title">Checklist Results</div>
    <table>
        <thead>
            <tr>
                <th>Item / Test</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {% for item, status in checklist.items() %}
            <tr>
                <td>{{ item }}</td>
                <td class="status-{{ status|lower|replace(' ', '-') }}">{{ status }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <div class="section-title">Health Assessment</div>
    <div class="grid">
        <div><span class="label">Tests Passed:</span> {{ pass_count }} / {{ total_tests }}</div>
        <div><span class="label">Device Health Score:</span> {{ health_score }}%</div>
    </div>

    <div class="section-title">Remarks & Observations</div>
    <p style="padding: 10px; background-color: #fbfbfb; border: 1px solid #f0f0f0;">{{ record.remarks }}</p>

    <div class="footer">
        This is an electronically generated report. Professional medical equipment inspection system.
    </div>
</body>
</html>
"""

def generate_pdf(record, checklist):
    total_tests = len(checklist)
    pass_count = sum(1 for v in checklist.values() if v == "Pass")
    health_score = f"{(pass_count / total_tests * 100):.1f}" if total_tests > 0 else "N/A"

    template = Template(HTML_TEMPLATE)
    html_out = template.render(
        record=record,
        checklist=checklist,
        pass_count=pass_count,
        total_tests=total_tests,
        health_score=health_score,
    )
    pdf = HTML(string=html_out).write_pdf()
    return pdf
