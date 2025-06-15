from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Suspicious Activity Triage - Certificate of Completion", ln=True, align="C")
        self.ln(10)

    def add_stats(self, name, stats, time_taken):
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"Officer Name: {name}", ln=True)
        self.cell(0, 10, f"Date Completed: {datetime.today().strftime('%Y-%m-%d')}", ln=True)
        self.cell(0, 10, f"Cases Handled: {stats['cases']}", ln=True)
        self.cell(0, 10, f"Correct Decisions: {stats['correct']}", ln=True)
        self.cell(0, 10, f"Missed Red Flags: {stats['missed']}", ln=True)
        self.cell(0, 10, f"Time Spent: {round(time_taken, 2)} minutes", ln=True)
        self.ln(5)

    def add_summary_chart(self, impact):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Case Handling Summary:", ln=True)
        self.set_font("Arial", "", 11)
        for k, v in impact.items():
            self.cell(0, 10, f"- {k}: {v}", ln=True)
        self.ln(5)

    def add_case_feedback(self, errors):
        if not errors:
            return
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Case Review (Incorrect Handling):", ln=True)
        self.set_font("Arial", "", 11)
        for err in errors:
            self.multi_cell(0, 8, f"Report ID: {err['report_id']}")
            self.multi_cell(0, 8, f"Background: {err['background']}")
            self.multi_cell(0, 8, f"Player Action: {err['player_action']}")
            self.multi_cell(0, 8, f"Correct Action: {err['correct_action']}")
            self.multi_cell(0, 8, f"Red Flags Missed: {', '.join(err['missed_flags'])}")
            self.multi_cell(0, 8, f"Required Flags: {', '.join(err['correct_flags'])}")
            self.ln(4)

    def disclaimer(self):
        self.set_font("Arial", "I", 9)
        self.ln(10)
        self.multi_cell(0, 6, "This certificate is generated for training purposes only. All names and data are fictitious.")

def generate_certificate(name, stats, errors=None, impact_summary=None, time_taken=0, output_path="certificate.pdf"):
    pdf = PDF()
    pdf.add_page()
    pdf.add_stats(name, stats, time_taken)
    if impact_summary:
        pdf.add_summary_chart(impact_summary)
    if errors:
        pdf.add_case_feedback(errors)
    pdf.disclaimer()
    pdf.output(output_path)
    return output_path
