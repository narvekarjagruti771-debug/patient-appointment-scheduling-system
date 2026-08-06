# /// script
# dependencies = [
#   "fpdf2",
#   "matplotlib",
#   "pillow",
#   "pypdf"
# ]
# ///

import os
import sys

def generate_diagrams():
    print("Setting up matplotlib...")
    import matplotlib
    matplotlib.use('Agg') # Headless mode
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    
    print("Generating Level 0 DFD...")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    
    patient_box = patches.FancyBboxPatch((0.5, 2.0), 1.8, 1.0, boxstyle="round,pad=0.1", fc="#e0f2fe", ec="#0284c7", lw=2)
    sys_box = patches.Circle((5.0, 2.5), 1.0, fc="#fef3c7", ec="#d97706", lw=2)
    doc_box = patches.FancyBboxPatch((7.7, 2.0), 1.8, 1.0, boxstyle="round,pad=0.1", fc="#f3e8ff", ec="#7e22ce", lw=2)
    
    ax.add_patch(patient_box)
    ax.add_patch(sys_box)
    ax.add_patch(doc_box)
    
    ax.text(1.4, 2.5, "PATIENT\n(User Entity)", ha="center", va="center", fontsize=9, weight="bold", color="#0369a1")
    ax.text(5.0, 2.5, "MediFlow System\n(DBMS & API\nServer)", ha="center", va="center", fontsize=9, weight="bold", color="#b45309")
    ax.text(8.6, 2.5, "DOCTOR / ADMIN\n(User Entity)", ha="center", va="center", fontsize=9, weight="bold", color="#6b21a8")
    
    ax.annotate("Register Account\nBook Slot", xy=(3.9, 2.7), xytext=(1.4, 3.8),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.5, connectionstyle="arc3,rad=0.25"),
                fontsize=8, color="#0369a1")
    
    ax.annotate("Booking Confirmation\nQueue Status Updates", xy=(2.4, 2.2), xytext=(3.8, 1.1),
                arrowprops=dict(arrowstyle="<-", color="#0284c7", lw=1.5, connectionstyle="arc3,rad=0.25"),
                fontsize=8, color="#0369a1")
    
    ax.annotate("Set specialties\nUpdate Appt Status", xy=(6.1, 2.7), xytext=(6.8, 3.8),
                arrowprops=dict(arrowstyle="<-", color="#7e22ce", lw=1.5, connectionstyle="arc3,rad=-0.25"),
                fontsize=8, color="#6b21a8")
    
    ax.annotate("View Patient Queue\nDatabase logs & SP Reports", xy=(7.6, 2.2), xytext=(4.3, 1.3),
                arrowprops=dict(arrowstyle="->", color="#7e22ce", lw=1.5, connectionstyle="arc3,rad=-0.25"),
                fontsize=8, color="#6b21a8")
                
    plt.title("Level 0 Data Flow Diagram (Context Diagram)", fontsize=12, weight="bold", pad=15, color="#1e293b")
    plt.tight_layout()
    plt.savefig("dfd_level_0.png", dpi=300)
    plt.close()

    print("Generating Level 1 DFD...")
    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.axis('off')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.5)
    
    patient_ent = patches.FancyBboxPatch((0.2, 5.2), 1.5, 1.0, boxstyle="round,pad=0.1", fc="#e0f2fe", ec="#0284c7", lw=2)
    doc_ent = patches.FancyBboxPatch((10.3, 5.2), 1.5, 1.0, boxstyle="round,pad=0.1", fc="#f3e8ff", ec="#7e22ce", lw=2)
    ax.add_patch(patient_ent)
    ax.add_patch(doc_ent)
    ax.text(0.95, 5.7, "PATIENT", ha="center", va="center", fontsize=9, weight="bold", color="#0369a1")
    ax.text(11.05, 5.7, "DOCTOR\nADMIN", ha="center", va="center", fontsize=9, weight="bold", color="#6b21a8")
    
    p1 = patches.Circle((3.0, 5.7), 0.6, fc="#f0fdf4", ec="#16a34a", lw=1.5)
    p2 = patches.Circle((6.0, 5.7), 0.6, fc="#f0fdf4", ec="#16a34a", lw=1.5)
    p3 = patches.Circle((9.0, 5.7), 0.6, fc="#f0fdf4", ec="#16a34a", lw=1.5)
    p4 = patches.Circle((4.5, 3.2), 0.6, fc="#f0fdf4", ec="#16a34a", lw=1.5)
    p5 = patches.Circle((7.5, 3.2), 0.6, fc="#f0fdf4", ec="#16a34a", lw=1.5)
    
    for p_shape in [p1, p2, p3, p4, p5]:
        ax.add_patch(p_shape)
        
    ax.text(3.0, 5.7, "1.0\nRegister\nPatient", ha="center", va="center", fontsize=8, weight="bold", color="#15803d")
    ax.text(6.0, 5.7, "2.0\nLoad\nDoctors", ha="center", va="center", fontsize=8, weight="bold", color="#15803d")
    ax.text(9.0, 5.7, "3.0\nBook\nAppt", ha="center", va="center", fontsize=8, weight="bold", color="#15803d")
    ax.text(4.5, 3.2, "4.0\nUpdate\nStatus", ha="center", va="center", fontsize=8, weight="bold", color="#15803d")
    ax.text(7.5, 3.2, "5.0\nGenerate\nReport", ha="center", va="center", fontsize=8, weight="bold", color="#15803d")
    
    def draw_datastore(x, y, label):
        ax.plot([x, x+1.8], [y, y], color="#475569", lw=2)
        ax.plot([x, x+1.8], [y+0.6, y+0.6], color="#475569", lw=2)
        ax.fill_between([x, x+1.8], y, y+0.6, color="#f8fafc")
        ax.text(x+0.9, y+0.3, label, ha="center", va="center", fontsize=8, weight="bold", color="#334155")
        
    draw_datastore(1.5, 1.2, "D1: patients")
    draw_datastore(4.0, 1.2, "D2: doctors")
    draw_datastore(6.5, 1.2, "D3: appointments")
    draw_datastore(9.0, 1.2, "D4: logs")
    draw_datastore(7.5, 4.4, "D5: daily_reports")
    
    ax.annotate("Details", xy=(2.3, 5.7), xytext=(1.8, 5.7), arrowprops=dict(arrowstyle="->", color="#0284c7"))
    ax.annotate("Write Patient", xy=(2.3, 1.8), xytext=(2.9, 5.1), arrowprops=dict(arrowstyle="->", color="#16a34a"))
    ax.annotate("View Spec", xy=(5.4, 5.7), xytext=(1.8, 6.4), arrowprops=dict(arrowstyle="->", color="#0284c7", connectionstyle="arc3,rad=0.15"))
    ax.annotate("Read Docs", xy=(6.0, 1.8), xytext=(6.0, 5.1), arrowprops=dict(arrowstyle="<-", color="#16a34a"))
    ax.annotate("Request Book", xy=(8.4, 5.7), xytext=(1.8, 6.9), arrowprops=dict(arrowstyle="->", color="#0284c7", connectionstyle="arc3,rad=0.25"))
    ax.annotate("Insert Appt", xy=(7.4, 1.8), xytext=(8.8, 5.1), arrowprops=dict(arrowstyle="->", color="#16a34a"))
    ax.annotate("Status", xy=(4.6, 3.8), xytext=(10.3, 6.4), arrowprops=dict(arrowstyle="->", color="#7e22ce", connectionstyle="arc3,rad=0.15"))
    ax.annotate("Update Status", xy=(7.0, 1.8), xytext=(5.0, 2.7), arrowprops=dict(arrowstyle="->", color="#16a34a"))
    ax.annotate("Audit Log", xy=(9.2, 1.8), xytext=(5.1, 3.1), arrowprops=dict(arrowstyle="->", color="#dc2626", connectionstyle="arc3,rad=-0.1"))
    ax.annotate("Cursor Fetch", xy=(7.4, 1.8), xytext=(7.5, 2.6), arrowprops=dict(arrowstyle="<-", color="#d97706"))
    ax.annotate("Write Report", xy=(8.2, 4.4), xytext=(7.7, 3.8), arrowprops=dict(arrowstyle="->", color="#d97706"))
    ax.annotate("Trigger Run", xy=(8.1, 3.4), xytext=(10.3, 6.0), arrowprops=dict(arrowstyle="->", color="#7e22ce"))
    
    plt.title("Level 1 Data Flow Diagram (Functional Processes & Data Stores)", fontsize=12, weight="bold", pad=15, color="#1e293b")
    plt.tight_layout()
    plt.savefig("dfd_level_1.png", dpi=300)
    plt.close()

    print("Generating Level 2 DFD...")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    
    req_box = patches.FancyBboxPatch((0.5, 2.0), 1.8, 1.0, boxstyle="round,pad=0.1", fc="#fee2e2", ec="#ef4444", lw=1.5)
    db_engine = patches.FancyBboxPatch((4.0, 1.5), 2.2, 2.0, boxstyle="round,pad=0.1", fc="#ecfdf5", ec="#10b981", lw=2)
    logs_store = patches.FancyBboxPatch((8.0, 3.2), 1.6, 0.8, boxstyle="round,pad=0.1", fc="#f8fafc", ec="#475569", lw=1.5)
    rep_store = patches.FancyBboxPatch((8.0, 1.0), 1.6, 0.8, boxstyle="round,pad=0.1", fc="#f8fafc", ec="#475569", lw=1.5)
    
    ax.add_patch(req_box)
    ax.add_patch(db_engine)
    ax.add_patch(logs_store)
    ax.add_patch(rep_store)
    
    ax.text(1.4, 2.5, "HTTP POST/PUT\nAPI Requests\n(server.js Router)", ha="center", va="center", fontsize=8.5, weight="bold", color="#b91c1c")
    ax.text(5.1, 2.5, "MySQL DBMS ENGINE\n\n- SQL view queries\n- Triggers insert/update\n- Cursor SP execution", ha="center", va="center", fontsize=8.5, weight="bold", color="#047857")
    ax.text(8.8, 3.6, "Table:\nappointment_logs", ha="center", va="center", fontsize=8, weight="bold", color="#334155")
    ax.text(8.8, 1.4, "Table:\ndaily_reports", ha="center", va="center", fontsize=8, weight="bold", color="#334155")
    
    ax.annotate("INSERT / UPDATE\nappointments", xy=(4.0, 2.6), xytext=(2.4, 2.6),
                arrowprops=dict(arrowstyle="->", color="#ef4444", lw=1.5), fontsize=7.5)
    ax.annotate("CALL Stored Proc\ngenerate_daily_report", xy=(4.0, 2.1), xytext=(2.4, 1.6),
                arrowprops=dict(arrowstyle="->", color="#3b82f6", lw=1.5), fontsize=7.5)
    
    ax.annotate("Automatic Triggers\n(after_appt_insert/\nafter_appt_update)", xy=(8.0, 3.6), xytext=(6.3, 3.2),
                arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.5), fontsize=7.5)
    ax.annotate("Loop-fetch with Cursor\n& INSERT into report", xy=(8.0, 1.4), xytext=(6.3, 1.8),
                arrowprops=dict(arrowstyle="->", color="#d97706", lw=1.5), fontsize=7.5)
                
    plt.title("Level 2 Data Flow Diagram (DBMS Internal Event Processing)", fontsize=12, weight="bold", pad=15, color="#1e293b")
    plt.tight_layout()
    plt.savefig("dfd_level_2.png", dpi=300)
    plt.close()

    print("Generating ER Diagram...")
    fig, ax = plt.subplots(figsize=(12, 7.5))
    ax.axis('off')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8.5)
    
    def draw_entity(x, y, title, attributes, color_header, color_body):
        ax.plot([x, x+2.2], [y, y], color="#334155", lw=1.5)
        ax.plot([x, x+2.2], [y-0.5, y-0.5], color="#334155", lw=1.5)
        ax.fill_between([x, x+2.2], y-0.5, y, color=color_header)
        ax.text(x+1.1, y-0.25, title, ha="center", va="center", fontsize=8.5, weight="bold", color="#ffffff")
        
        h_body = len(attributes) * 0.35 + 0.15
        ax.plot([x, x+2.2], [y-0.5-h_body, y-0.5-h_body], color="#334155", lw=1.5)
        ax.plot([x, x], [y, y-0.5-h_body], color="#334155", lw=1.5)
        ax.plot([x+2.2, x+2.2], [y, y-0.5-h_body], color="#334155", lw=1.5)
        ax.fill_between([x, x+2.2], y-0.5-h_body, y-0.5, color=color_body)
        
        for idx, attr in enumerate(attributes):
            is_pk = "PK" in attr
            is_fk = "FK" in attr
            font_weight = "bold" if (is_pk or is_fk) else "normal"
            ax.text(x+0.1, y-0.8-idx*0.35, attr, ha="left", va="center", fontsize=7.5, weight=font_weight, family="monospace")
            
    draw_entity(0.5, 7.5, "patients", 
                ["patient_id (PK)", "name", "email (U)", "phone", "dob", "gender", "created_at"],
                "#0284c7", "#f0f9ff")
                
    draw_entity(9.3, 7.5, "doctors", 
                ["doctor_id (PK)", "name", "specialization", "email (U)", "phone", "created_at"],
                "#7e22ce", "#faf5ff")
                
    draw_entity(4.9, 5.0, "appointments", 
                ["appointment_id (PK)", "patient_id (FK)", "doctor_id (FK)", "appointment_date", "appointment_time", "status", "reason", "created_at"],
                "#16a34a", "#f0fdf4")
                
    draw_entity(0.5, 2.5, "appointment_logs", 
                ["log_id (PK)", "appointment_id", "action_type", "old_status", "new_status", "log_timestamp", "description"],
                "#dc2626", "#fef2f2")
                
    draw_entity(9.3, 2.5, "daily_reports", 
                ["report_id (PK)", "report_date (U)", "report_summary", "generated_at"],
                "#d97706", "#fffbeb")
                
    # Patients (1) to Appointments (N)
    ax.plot([2.7, 3.8, 3.8, 4.9], [5.5, 5.5, 4.3, 4.3], color="#0284c7", lw=1.5)
    ax.text(2.8, 5.65, "1", fontsize=8, weight="bold", color="#0284c7")
    ax.text(4.7, 4.45, "N", fontsize=8, weight="bold", color="#0284c7")
    
    # Doctors (1) to Appointments (N)
    ax.plot([9.3, 8.2, 8.2, 7.1], [5.5, 5.5, 4.3, 4.3], color="#7e22ce", lw=1.5)
    ax.text(9.1, 5.65, "1", fontsize=8, weight="bold", color="#7e22ce")
    ax.text(7.3, 4.45, "N", fontsize=8, weight="bold", color="#7e22ce")
    
    # Appointments (1) to logs (N) (via trigger)
    ax.plot([6.0, 6.0, 2.7], [2.6, 2.1, 2.1], color="#dc2626", lw=1.5)
    ax.text(5.8, 2.7, "1", fontsize=8, weight="bold", color="#dc2626")
    ax.text(2.8, 2.2, "N", fontsize=8, weight="bold", color="#dc2626")
    
    # Diamonds (using round boxes for compatibility)
    ax.text(3.8, 4.9, "has", bbox=dict(boxstyle="round,pad=0.3", fc="#ffffff", ec="#0284c7"), ha="center", va="center", fontsize=8)
    ax.text(8.2, 4.9, "attends", bbox=dict(boxstyle="round,pad=0.3", fc="#ffffff", ec="#7e22ce"), ha="center", va="center", fontsize=8)
    ax.text(4.5, 2.1, "logs activity", bbox=dict(boxstyle="round,pad=0.3", fc="#ffffff", ec="#dc2626"), ha="center", va="center", fontsize=7)
    
    plt.title("Entity-Relationship (ER) Diagram", fontsize=14, weight="bold", pad=20, color="#1e293b")
    plt.tight_layout()
    plt.savefig("erd.png", dpi=300)
    plt.close()
    print("All diagrams generated successfully!")

# Define FPDF Custom Class
from fpdf import FPDF

class DBMSReportPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.current_chapter_num = "0"
        self.set_margins(left=20, top=20, right=20)
        self.set_auto_page_break(auto=True, margin=20)
        self.alias_nb_pages()
        
    def header(self):
        # Suppress on cover page (page 1) or TOC (page 2)
        if self.page_no() <= 2:
            return
        
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 116, 139) # slate-500
        
        # Header text
        self.cell(0, 8, "DBMS Project Report: Patient Appointment Scheduling System", align="L", new_x="RIGHT", new_y="TOP")
        self.cell(0, 8, f"Chapter {self.current_chapter_num}", align="R", new_x="LMARGIN", new_y="NEXT")
        
        # Draw a thin rule line
        self.set_draw_color(226, 232, 240) # slate-200
        self.set_line_width(0.2)
        self.line(20, 16, 190, 16)
        self.ln(4)
        
    def footer(self):
        # Suppress on cover page
        if self.page_no() == 1:
            return
        
        self.set_y(-15)
        # Draw bottom rule line
        self.set_draw_color(226, 232, 240) # slate-200
        self.set_line_width(0.2)
        self.line(20, self.get_y() - 1, 190, self.get_y() - 1)
        
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 116, 139) # slate-500
        self.cell(0, 10, "Department of Computer Science & Engineering", align="L", new_x="RIGHT", new_y="TOP")
        self.cell(0, 10, f"Page {self.page_no()} of {{nb}}", align="R", new_x="LMARGIN", new_y="NEXT")

# Helper functions to build layout
def add_cover_page(pdf):
    pdf.add_page()
    pdf.set_y(40)
    
    # Document Header
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(30, 41, 59) # slate-800
    pdf.cell(0, 12, "PATIENT APPOINTMENT", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 12, "SCHEDULING SYSTEM", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(14, 165, 233) # sky-500
    pdf.cell(0, 8, "A DATABASE MANAGEMENT SYSTEM PROJECT REPORT", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(25)
    
    # Under DBMS Course
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(71, 85, 105) # slate-600
    pdf.cell(0, 6, "Submitted in partial fulfillment of the requirements", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "for the award of the degree of", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(15, 23, 42) # slate-900
    pdf.cell(0, 8, "BACHELOR OF TECHNOLOGY", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 6, "IN COMPUTER SCIENCE & ENGINEERING", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    
    # Author details
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 116, 139) # slate-500
    pdf.cell(0, 5, "DEVELOPED BY:", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 6, "[Student Name / Roll Number]", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, "UNDER THE GUIDANCE OF:", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 6, "[Instructor / Guide Name]", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(35)
    
    # Institution Logo Placeholder or Text
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 6, "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 6, "UNIVERSITY NAME / INSTITUTE DETAILS", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Session: 2025 - 2026", align="C", new_x="LMARGIN", new_y="NEXT")

def add_table_of_contents(pdf):
    pdf.add_page()
    pdf.set_y(25)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 15, "TABLE OF CONTENTS", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    def toc_line(chap_text, p_num, is_bold=False):
        pdf.set_font("Helvetica", "B" if is_bold else "", 10)
        pdf.set_text_color(15, 23, 42) if is_bold else pdf.set_text_color(71, 85, 105)
        
        # We need dot leaders. FPDF2 supports dot leaders using simple string width math
        w_ch = pdf.get_string_width(chap_text)
        w_p = pdf.get_string_width(p_num)
        avail = 170 - w_ch - w_p # Total width inside margins is 170mm
        num_dots = int(avail / pdf.get_string_width(".")) - 4
        dots = "." * num_dots if num_dots > 0 else " "
        
        pdf.cell(0, 7, f"{chap_text}{dots}{p_num}", new_x="LMARGIN", new_y="NEXT")
        
    toc_line("Chapter 1: Introduction", "1", is_bold=True)
    toc_line("  1.1 Introduction", "1")
    toc_line("  1.2 Objective", "1")
    toc_line("  1.3 Module Breakdown", "1")
    pdf.ln(2)
    
    toc_line("Chapter 2: Survey of Technologies", "2", is_bold=True)
    toc_line("  2.1 Software Description", "2")
    toc_line("  2.2 Languages & Architectures", "2")
    toc_line("    2.2.1 HTML", "2")
    toc_line("    2.2.2 CSS", "2")
    toc_line("    2.2.3 PHP (Technology Survey)", "3")
    toc_line("    2.2.4 MySQL", "3")
    pdf.ln(2)
    
    toc_line("Chapter 3: Requirements and Analysis", "4", is_bold=True)
    toc_line("  3.1 Requirement Specification", "4")
    toc_line("  3.2 Hardware and Software Requirements", "4")
    toc_line("  3.3 Data Flow Diagrams", "4")
    toc_line("    3.3.1 Level 0 (Context Diagram)", "5")
    toc_line("    3.3.2 Level 1 (Functional Details)", "5")
    toc_line("    3.3.3 Level 2 (DBMS Engine Flow)", "6")
    toc_line("  3.4 Data Dictionary", "7")
    toc_line("  3.5 Entity-Relationship (ER) Diagram", "11")
    toc_line("  3.6 Normalization (1NF to 3NF)", "12")
    pdf.ln(2)
    
    toc_line("Chapter 4: Program Code", "17", is_bold=True)
    toc_line("  4.1 Code Details and Code Efficiency", "17")
    pdf.ln(2)
    
    toc_line("Chapter 5: Result and Discussion", "42", is_bold=True)
    toc_line("  5.1 User Documentation", "42")
    pdf.ln(2)
    
    toc_line("Chapter 6: Testing", "46", is_bold=True)
    toc_line("  6.1 Unit Testing", "46")
    toc_line("  6.2 Integration Testing", "46")
    toc_line("  6.3 System Testing", "46")
    toc_line("  6.4 Acceptance Testing", "46")
    pdf.ln(2)
    
    toc_line("Chapter 7: Conclusion", "47", is_bold=True)
    toc_line("  7.1 Conclusion & Future Enhancements", "47")

def add_chapter_header(pdf, chap_num, chap_title):
    pdf.current_chapter_num = chap_num
    pdf.add_page()
    pdf.set_y(25)
    
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(14, 165, 233) # sky-500
    pdf.cell(0, 6, f"Chapter {chap_num}", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(15, 23, 42) # slate-900
    pdf.cell(0, 10, chap_title.upper(), new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(14, 165, 233)
    pdf.set_line_width(1.5)
    # Draw a line under title
    pdf.line(20, pdf.get_y() + 2, 80, pdf.get_y() + 2)
    pdf.ln(8)

def add_section_header(pdf, sec_num, sec_title):
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(3, 105, 161) # sky-700
    pdf.cell(0, 8, f"{sec_num} {sec_title}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

def add_subsection_header(pdf, sub_num, sub_title):
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(51, 65, 85) # slate-700
    pdf.cell(0, 6, f"{sub_num} {sub_title}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

def add_body_p(pdf, text):
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(71, 85, 105) # slate-600
    # Auto newline using multi_cell
    pdf.multi_cell(0, 6, text, align="J")
    pdf.ln(4)

def add_bullet_point(pdf, bold_part, text_part):
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.write(6, f"  *  {bold_part}: ")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(71, 85, 105)
    pdf.write(6, f"{text_part}\n")
    pdf.ln(2)

def add_code_block(pdf, title, code):
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 5, f"[File: {title}]", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Courier", "", 8)
    pdf.set_text_color(15, 23, 42)
    pdf.set_fill_color(248, 250, 252) # slate-50 background
    pdf.set_draw_color(226, 232, 240) # slate-200 border
    pdf.multi_cell(0, 4, code, border=1, fill=True)
    pdf.ln(4)

def add_diagram_with_caption(pdf, image_path, width, height, caption_text):
    # Ensure image fits on current page
    # Page height is 297, bottom margin is 20, top margin is 20.
    # Max printable y is 277.
    required_height = height + 15
    if pdf.get_y() + required_height > 277:
        pdf.add_page()
    
    # Center the image relative to the physical page width (210mm)
    x_pos = (210 - width) / 2
    pdf.image(image_path, x=x_pos, y=pdf.get_y(), w=width)
    
    # Move cursor below image
    pdf.set_y(pdf.get_y() + height + 2)
    
    # Add caption centered
    pdf.set_font("Helvetica", "I", 9.5)
    pdf.set_text_color(71, 85, 105) # slate-600
    pdf.cell(0, 6, caption_text, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

def clean_for_pdf(text):
    replacements = {
        "❌": "[X]",
        "✅": "[OK]",
        "🌐": "[URL]",
        "🎉": "[Success]",
        "🛠️": "[Setup]",
        "🛠": "[Setup]",
        "🔍": "[Search]",
        "ℹ️": "[Info]",
        "ℹ": "[Info]",
        "💡": "[Tip]",
        "✔️": "[Y]",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "—": "-",
        "–": "-"
    }
    for emoji, replacement in replacements.items():
        text = text.replace(emoji, replacement)
    
    cleaned = []
    for char in text:
        if ord(char) < 256:
            cleaned.append(char)
        else:
            cleaned.append(" ")
    return "".join(cleaned)

def build_pdf_report():
    print("Creating PDF document object...")
    pdf = DBMSReportPDF()
    
    # 1. Cover Page
    print("Writing Cover Page...")
    add_cover_page(pdf)
    
    # 2. Table of Contents
    print("Writing TOC...")
    add_table_of_contents(pdf)
    
    # ====================================================================
    # CHAPTER 1
    # ====================================================================
    print("Writing Chapter 1...")
    add_chapter_header(pdf, "1", "Introduction")
    
    add_section_header(pdf, "1.1", "Introduction")
    add_body_p(pdf, 
        "Modern medical facilities and clinics face significant operational hurdles when managing patient appointments, consultation slots, and physician availability using manual, paper-based records. Manual processes frequently lead to scheduling overlapping appointments (double-bookings), patient queue blockages, high administrator stress, and structural record-keeping errors. This lack of coordination deteriorates the patient experience and reduces healthcare delivery efficiency."
    )
    add_body_p(pdf,
        "To address these operational deficits, this Database Management System (DBMS) project introduces 'MediFlow', a dedicated Patient Appointment Scheduling System. MediFlow utilizes a three-tier software model that encapsulates clinic logical schemas directly inside a secure Relational Database Management System. By mapping real-world medical entities (patients, doctors, logs, and summaries) into a normalized MySQL schema, clinic admins can automate appointment queues, track historical records, and ensure absolute consistency."
    )
    
    add_section_header(pdf, "1.2", "Objective")
    add_body_p(pdf,
        "The fundamental objective of this database application is to deliver a reliable, automated, and conflict-free tool for medical schedule management. Key database-specific design targets include:"
    )
    add_bullet_point(pdf, "Integrity and Non-Overlapping Scheduling", "Enforce relational foreign keys and transaction boundaries so that patients and doctors cannot double-book the same slot.")
    add_bullet_point(pdf, "Encapsulation of Query Joins", "Create an SQL Virtual View (`upcoming_appointments_view`) to handle multi-table joins inside the database engine, returning a clean upcoming schedule to APIs.")
    add_bullet_point(pdf, "Automated Security Audit Trails", "Use database triggers to intercept appointment changes (inserts and status updates) and write immutable log audits directly to an independent logs table.")
    add_bullet_point(pdf, "Row-by-Row Cursor Processing", "Utilize a procedural SQL database cursor to loop through daily appointments on demand, compile a textual summary, and save it in a reporting structure.")
    add_bullet_point(pdf, "Modern Architecture", "Build an easy-to-use modern web interface communicating with a fast asynchronous Node.js Express API server and a MySQL database backend.")
    
    add_section_header(pdf, "1.3", "Module Breakdown")
    add_body_p(pdf, "The architecture of MediFlow is split into five distinct functional modules:")
    add_bullet_point(pdf, "Patient Registration Module", "Enables the registration of new patients. Validates emails to prevent duplicates and writes patient profiles (name, DOB, gender, phone, email) to the database.")
    add_bullet_point(pdf, "Doctor Specialty Lookup Module", "Maintains records of available specialist doctors. Allows frontend lookups to filter slots and query matching specialist consultants.")
    add_bullet_point(pdf, "Appointment Booking Engine", "Manages scheduling slots. Feeds new appointment rows into MySQL while checking database constraint requirements.")
    add_bullet_point(pdf, "Automated Audit Module", "Contains database-level triggers (`after_appointment_insert`, `after_appointment_update`) running completely independent of application code to log scheduling actions.")
    add_bullet_point(pdf, "Daily Report Compilation Module", "Implements the stored procedure `generate_daily_report(date)`. Activates a cursor query that crawls specific dates, merges patient/doctor descriptions, and outputs administrative reports.")

    # ====================================================================
    # CHAPTER 2
    # ====================================================================
    print("Writing Chapter 2...")
    add_chapter_header(pdf, "2", "Survey of Technologies")
    
    add_section_header(pdf, "2.1", "Software Description")
    add_body_p(pdf,
        "The software architecture follows a modular Three-Tier client-server pattern. The client layer runs directly inside any standard web browser, sending AJAX fetch commands. The middle tier runs a lightweight Node.js Express server to handle routing, input validation, and connection pool query dispatching. The storage tier uses MySQL to execute transactional data procedures. By cleanly decoupling client rendering, API controllers, and database storage, the application remains scalable and highly maintainable."
    )
    
    add_section_header(pdf, "2.2", "Languages & Architectures")
    
    add_subsection_header(pdf, "2.2.1", "HTML (HyperText Markup Language)")
    add_body_p(pdf,
        "HTML5 is utilized to layout the application layout. The layout features a Sidebar Navigation panel, an active Status indicator checking database connectivity, a Patient Portal (registration modal, selector list, booking form), a Doctor Queue panel (for status management), and a Developer Lab interface exposing raw table counts, live database trigger log captures, and stored procedure execution outputs. All forms include HTML5 constraints (required fields, date range limits) to prevent malformed data payloads."
    )
    
    add_subsection_header(pdf, "2.2.2", "CSS (Cascading Style Sheets)")
    add_body_p(pdf,
        "The visual aesthetics use premium CSS3 techniques, rendering a state-of-the-art administrative dashboard. The visual theme uses a sleek Dark Mode scheme with deep purple, indigo, and teal neon gradients. Glassmorphism is implemented via CSS backdrop-filters, rendering translucent cards. Interaction feedback is provided through CSS micro-animations on hover states, pulsing indicators, and sliding tabs. Layouts are completely responsive, adjusting cleanly using CSS Flexbox and CSS Grid frameworks."
    )
    
    add_subsection_header(pdf, "2.2.3", "PHP (Traditional Stack Survey)")
    add_body_p(pdf,
        "Traditionally, academic DBMS projects are structured around PHP, a server-side scripting language running on Apache in XAMPP. In a standard PHP model, the server processes SQL queries sequentially via standard drivers (`PDO` or `mysqli`) and injects variables directly into HTML templates before responding. While PHP remains a robust and reliable stack, its synchronous model blocks threads for long-running database requests. In our modern implementation, Node.js replaces PHP as the application layer, running an asynchronous, event-driven event loop that uses non-blocking database pools to handle thousands of concurrent queries without blocking."
    )
    
    add_subsection_header(pdf, "2.2.4", "MySQL Database")
    add_body_p(pdf,
        "MySQL is an open-source Relational Database Management System (RDBMS) configured using the transactional InnoDB storage engine. MySQL executes physical database operations. It maintains strict constraints: it prevents orphan records using foreign keys with cascading deletions, exposes a queryable relational view to combine tables efficiently, runs row-level triggers to enforce data audits, and executes stored procedures that loop through active sets using database cursors. The database connects to Node.js through a persistent pool of reusable connections, eliminating connection-startup latency."
    )

    # ====================================================================
    # CHAPTER 3
    # ====================================================================
    print("Writing Chapter 3...")
    add_chapter_header(pdf, "3", "Requirements and Analysis")
    
    add_section_header(pdf, "3.1", "Requirement Specification")
    add_body_p(pdf,
        "To ensure the system satisfies both operational clinic workflows and database design principles, we specify requirements as follows:"
    )
    add_bullet_point(pdf, "Functional Requirements", "Patients must register with valid emails; booking engines must map patient/doctor foreign keys to target slots; system must record logs dynamically; admins must run daily cursor reports on any date.")
    add_bullet_point(pdf, "Non-Functional Requirements - Integrity", "The database must prevent database inconsistencies using foreign key constraints and cascading deletes.")
    add_bullet_point(pdf, "Non-Functional Requirements - Performance", "Index structures and virtual SQL views must optimize lookups, returning results under 50ms.")
    add_bullet_point(pdf, "Non-Functional Requirements - Security", "Triggers must enforce audit logs automatically, preventing admins or developers from editing appointment details without an immutable trail.")
    
    add_section_header(pdf, "3.2", "Hardware and Software Requirements")
    add_bullet_point(pdf, "Development OS", "Windows 10 / Windows 11 (x64 architecture)")
    add_bullet_point(pdf, "Processor & RAM", "Intel Core i3/i5 or AMD Ryzen 3/5, 4 GB RAM minimum (8 GB recommended)")
    add_bullet_point(pdf, "Database Server", "MySQL Community Server 8.0.x (packaged with XAMPP 8.1.x+) running on port 3307")
    add_bullet_point(pdf, "Application Runtime", "Node.js v18.x or newer with npm package manager")
    add_bullet_point(pdf, "Web Browser", "Modern evergreen browser with JavaScript enabled (e.g., Google Chrome)")
    
    pdf.add_page()
    add_section_header(pdf, "3.3", "Data Flow Diagrams (DFD)")
    add_body_p(pdf,
        "Data Flow Diagrams model the movement of data elements through the clinic scheduling system, mapping processes, data stores, external entities, and data flows."
    )
    
    add_subsection_header(pdf, "3.3.1", "Level 0 DFD (Context Diagram)")
    add_body_p(pdf,
        "The Context Diagram establishes system boundaries. It shows the main system (MediFlow DBMS) interacting with two external entities: Patients (who register and book slots) and Doctors/Admins (who configure schedules and run reports)."
    )
    add_diagram_with_caption(pdf, "dfd_level_0.png", width=160, height=80, caption_text="Figure 3.1: Level 0 DFD - Context Diagram")
    
    pdf.add_page()
    add_subsection_header(pdf, "3.3.2", "Level 1 DFD (Functional Processes)")
    add_body_p(pdf,
        "The Level 1 DFD decomposes the system into functional process nodes. It shows how patient details flow into process 1.0 (Patient Registration) to write to the 'patients' data store, how slots map to process 3.0 (Book Appointment) connecting to 'doctors' and 'appointments' stores, how updates run through process 4.0 to generate audit logs, and how process 5.0 compiles daily agenda reports."
    )
    add_diagram_with_caption(pdf, "dfd_level_1.png", width=160, height=86.6, caption_text="Figure 3.2: Level 1 DFD - Functional Processes and Data Stores")
    
    pdf.add_page()
    add_subsection_header(pdf, "3.3.3", "Level 2 DFD (DBMS Internal Processing)")
    add_body_p(pdf,
        "The Level 2 DFD details the internal database execution sequences. It visualizes the flow when SQL statements hit the DBMS: how inserts/updates trigger 'after_appointment_insert' and 'after_appointment_update' to write automatically to 'appointment_logs', and how executing the Stored Procedure initializes a cursor loop on the joined tables to output summary blocks to 'daily_reports'."
    )
    add_diagram_with_caption(pdf, "dfd_level_2.png", width=160, height=80, caption_text="Figure 3.3: Level 2 DFD - Internal Database Event Processing")
    
    # 3.4 Data Dictionary
    pdf.add_page()
    add_section_header(pdf, "3.4", "Data Dictionary")
    add_body_p(pdf,
        "The Data Dictionary defines metadata descriptions, types, keys, and constraint rules for the database schemas:"
    )
    
    def render_dd_table(table_name, columns):
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 6, f"Table: {table_name}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
        
        # Columns: Column Name, Data Type, Key, Description
        # We specify widths for A4: Total width = 170mm
        col_widths = (35, 35, 15, 85)
        headers = ("Field Name", "Data Type", "Key", "Description / Constraints")
        
        # Header Row
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(241, 245, 249) # slate-100
        pdf.set_text_color(51, 65, 85)
        
        for w, text in zip(col_widths, headers):
            pdf.cell(w, 7, text, border=1, fill=True, align="C")
        pdf.ln()
        
        # Data Rows
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(71, 85, 105)
        for col_name, col_type, col_key, col_desc in columns:
            # We use multi_cell or normal cell. Let's make sure it doesn't overflow.
            # Using multi_cell for description might wrap it. 
            # FPDF2 cell/multi_cell flow:
            # For simplicity, since description is long, we can use multi_cell or write a custom wrap function
            # Since FPDF2 supports pdf.table(), let's use that!
            pass

    # Actually, we can use the FPDF2 table API which is extremely robust and does auto-wrapping!
    # Let's define tables using fpdf2 table class:
    def write_table_dictionary(pdf, title, rows):
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 6, f"Table Structure: {title}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
        
        # Using FPDF2's pdf.table() API
        with pdf.table(col_widths=(22, 22, 10, 46), 
                       text_align=("LEFT", "LEFT", "CENTER", "LEFT")) as table:
            # Header
            header_row = table.row()
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(30, 41, 59)
            header_row.cell("Field")
            header_row.cell("Type")
            header_row.cell("Key")
            header_row.cell("Constraints / Purpose")
            
            # Data rows
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(71, 85, 105)
            for r in rows:
                data_row = table.row()
                data_row.cell(r[0])
                data_row.cell(r[1])
                data_row.cell(r[2])
                data_row.cell(r[3])
        pdf.ln(3)

    write_table_dictionary(pdf, "patients", [
        ("patient_id", "INT", "PK", "Primary Key, Auto increment, uniquely identifies each patient."),
        ("name", "VARCHAR(100)", "-", "Not Null, patient's full name."),
        ("email", "VARCHAR(100)", "U", "Unique, Not Null, patient's email address."),
        ("phone", "VARCHAR(15)", "-", "Not Null, phone number for contact."),
        ("dob", "DATE", "-", "Not Null, date of birth."),
        ("gender", "ENUM('Male','Female','Other')", "-", "Not Null, gender classification."),
        ("created_at", "TIMESTAMP", "-", "Default current timestamp, record creation date.")
    ])

    write_table_dictionary(pdf, "doctors", [
        ("doctor_id", "INT", "PK", "Primary Key, Auto increment, uniquely identifies each doctor."),
        ("name", "VARCHAR(100)", "-", "Not Null, doctor's full name."),
        ("specialization", "VARCHAR(100)", "-", "Not Null, medical specialty field."),
        ("email", "VARCHAR(100)", "U", "Unique, Not Null, professional contact email."),
        ("phone", "VARCHAR(15)", "-", "Not Null, contact number."),
        ("created_at", "TIMESTAMP", "-", "Default current timestamp, record creation date.")
    ])

    write_table_dictionary(pdf, "appointments", [
        ("appointment_id", "INT", "PK", "Primary Key, Auto increment, appointment transaction ID."),
        ("patient_id", "INT", "FK", "Foreign Key references patients(patient_id) with cascading delete."),
        ("doctor_id", "INT", "FK", "Foreign Key references doctors(doctor_id) with cascading delete."),
        ("appointment_date", "DATE", "-", "Not Null, target date of consultation."),
        ("appointment_time", "TIME", "-", "Not Null, target slot time."),
        ("status", "ENUM('Scheduled','Completed','Cancelled')", "-", "Default 'Scheduled', status indicator."),
        ("reason", "VARCHAR(255)", "-", "Not Null, patient's complaints or notes."),
        ("created_at", "TIMESTAMP", "-", "Default current timestamp, booking timestamp.")
    ])

    write_table_dictionary(pdf, "appointment_logs", [
        ("log_id", "INT", "PK", "Primary Key, Auto increment, logs audit identifier."),
        ("appointment_id", "INT", "-", "Not Null, links log to target appointment ID."),
        ("action_type", "ENUM('CREATE','UPDATE','DELETE')", "-", "Not Null, SQL operation type caught by trigger."),
        ("old_status", "VARCHAR(20)", "-", "Nullable, previous status of updated booking."),
        ("new_status", "VARCHAR(20)", "-", "Not Null, status after trigger execution."),
        ("log_timestamp", "TIMESTAMP", "-", "Default current timestamp, log execution date/time."),
        ("description", "TEXT", "-", "Constructed text detailing the exact data changes.")
    ])

    write_table_dictionary(pdf, "daily_reports", [
        ("report_id", "INT", "PK", "Primary Key, Auto increment, daily summary report ID."),
        ("report_date", "DATE", "U", "Unique, Not Null, target report agenda date."),
        ("report_summary", "TEXT", "-", "Not Null, aggregated text generated by cursor procedure."),
        ("generated_at", "TIMESTAMP", "-", "Auto-timestamps compilation date/time updates.")
    ])

    # 3.5 ER Diagram
    pdf.add_page()
    add_section_header(pdf, "3.5", "Entity-Relationship (ER) Diagram")
    add_body_p(pdf,
        "The Entity-Relationship Diagram maps the structural relationships between logical entities in the MediFlow system. The schema enforces strict referential mappings:"
    )
    add_bullet_point(pdf, "Patient to Appointment", "One patient can book multiple appointments (1-to-Many), mapped via patient_id foreign key constraint.")
    add_bullet_point(pdf, "Doctor to Appointment", "One doctor can consult for multiple appointments (1-to-Many), mapped via doctor_id foreign key constraint.")
    add_bullet_point(pdf, "Appointment to Log Record", "One appointment modification event generates logs (1-to-Many history tracking) written automatically via MySQL triggers.")
    add_bullet_point(pdf, "Daily Report", "An independent report compilation object mapping report summaries to unique dates.")
    
    # Embed ERD Image
    add_diagram_with_caption(pdf, "erd.png", width=160, height=100, caption_text="Figure 3.4: Entity-Relationship Diagram (ERD)")
    
    # 3.6 Normalization
    pdf.add_page()
    add_section_header(pdf, "3.6", "Normalization (1NF to 3NF)")
    add_body_p(pdf,
        "To avoid database design flaws (update, insertion, and deletion anomalies) and optimize storage, the MediFlow schema is normalized systematically from Unnormalized Form (UNF) through First (1NF), Second (2NF), and Third Normal Form (3NF)."
    )
    add_subsection_header(pdf, "3.6.1", "First Normal Form (1NF)")
    add_body_p(pdf,
        "A relation is in 1NF if all attributes contain only atomic (indivisible) values, and there are no repeating groups. In our design, all columns contain single values (e.g. no comma-separated text lists of multiple phone numbers or composite addresses in a single slot). Unique primary keys (patient_id, doctor_id, appointment_id, log_id, report_id) are defined to uniquely identify rows, thereby satisfying 1NF requirements."
    )
    add_subsection_header(pdf, "3.6.2", "Second Normal Form (2NF)")
    add_body_p(pdf,
        "A relation is in 2NF if it satisfies 1NF and contains no partial dependencies (i.e., no non-key attribute is dependent on only a subset of a composite primary key). Because all tables in MediFlow use single-attribute surrogate primary keys (e.g., patient_id, doctor_id, appointment_id) rather than composite keys, there is no possibility of partial dependencies. Every non-prime attribute (like name, email, specializing, date, status) depends fully on the whole single primary key. Thus, all tables satisfy 2NF."
    )
    add_subsection_header(pdf, "3.6.3", "Third Normal Form (3NF)")
    add_body_p(pdf,
        "A relation is in 3NF if it satisfies 2NF and contains no transitive dependencies (i.e. no non-key attribute is functionally dependent on another non-key attribute). Every non-key column in our tables depends directly and exclusively on the primary key, and nothing else (e.g., in patients table, email depends on patient_id, name depends on patient_id. In appointments table, status, reason, date, and time depend directly on appointment_id; the keys patient_id and doctor_id reference their respective primary keys without transitively linking names or specialties in the appointments table). Because no transitive dependencies exist, the schema satisfies 3NF."
    )

    # ====================================================================
    # CHAPTER 4
    # ====================================================================
    print("Writing Chapter 4...")
    add_chapter_header(pdf, "4", "Program Code")
    
    add_section_header(pdf, "4.1", "Code Details and Code Efficiency")
    add_body_p(pdf,
        "The project code is optimized to enforce data processing logic directly at the database engine level wherever possible, yielding high code efficiency and minimal latency:"
    )
    add_bullet_point(pdf, "SQL View Efficiency", "By joining patients, doctors, and appointments inside the SQL View 'upcoming_appointments_view', the Express API server only performs a simple 'SELECT * FROM upcoming_appointments_view' query. This shifts join computation to MySQL's query optimizer and reduces Express server overhead.")
    add_bullet_point(pdf, "Trigger Autonomy", "The MySQL triggers run automatically on row insertions or updates. This ensures that even if developers execute manual SQL updates bypassing the Node.js Express API, the audit trail in appointment_logs remains intact and secure.")
    add_bullet_point(pdf, "Stored Procedure with Cursor", "The procedure 'generate_daily_report' uses a MySQL cursor to compile daily schedules. Running this cursor loop inside the database server eliminates the need to execute multiple SELECT roundtrips from Node.js, reducing network overhead.")
    
    # Read files to inject
    print("Reading project files to inject...")
    
    schema_path = "database/schema.sql"
    server_path = "server.js"
    app_path = "public/app.js"
    
    # Read SQL Schema
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            sql_code = clean_for_pdf(f.read())
    except Exception as e:
        sql_code = f"Error reading {schema_path}: {str(e)}"
        
    # Read server.js
    try:
        with open(server_path, "r", encoding="utf-8") as f:
            server_code = clean_for_pdf(f.read())
    except Exception as e:
        server_code = f"Error reading {server_path}: {str(e)}"
        
    # Read app.js
    try:
        with open(app_path, "r", encoding="utf-8") as f:
            app_code = clean_for_pdf(f.read())
    except Exception as e:
        app_code = f"Error reading {app_path}: {str(e)}"
        
    # Print SQL schema in PDF
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "4.1.1 MySQL Database Schema Definition (schema.sql)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    # We will split sql_code into chunks to fit on pages cleanly, or write it directly
    # Since SQL schema is ~280 lines, fpdf2 multi_cell handles it.
    add_code_block(pdf, "database/schema.sql", sql_code)
    
    # Print Express Backend in PDF
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "4.1.2 Node.js Express Backend API Router (server.js)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    add_code_block(pdf, "server.js", server_code)
    
    # Print Frontend app.js snippets (extract key sections to keep it readable, or print whole file if small, 
    # but since app.js is 695 lines, let's inject a selected portion of it, e.g. lines 260 to 500)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "4.1.3 Frontend Portal JavaScript Controllers (app.js - Excerpt)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    # Extract lines from app_code
    app_lines = app_code.splitlines()
    excerpt_lines = app_lines[260:480] # lines 261 to 480 contains booking and report functions
    excerpt_code = "\n".join(excerpt_lines)
    add_code_block(pdf, "public/app.js (Selected API Integration Functions)", excerpt_code)

    # ====================================================================
    # CHAPTER 5
    # ====================================================================
    print("Writing Chapter 5...")
    add_chapter_header(pdf, "5", "Result and Discussion")
    
    add_section_header(pdf, "5.1", "User Documentation")
    add_body_p(pdf,
        "The MediFlow application is designed with user ease-of-use in mind. To set up and run the system locally, follow these instructions:"
    )
    
    add_subsection_header(pdf, "5.1.1", "Database Setup using XAMPP")
    add_bullet_point(pdf, "Step 1: Start MySQL in XAMPP", "Open XAMPP Control Panel and start MySQL on default port 3307 or 3306.")
    add_bullet_point(pdf, "Step 2: Install Node.js Dependencies", "Open a command prompt in the project root and run 'npm install' to resolve dependencies.")
    add_bullet_point(pdf, "Step 3: Auto-Setup Database", "Run 'node import-db.js'. This script connects to your running MySQL and imports database/schema.sql, inserting tables, trigger, procedures, and seed data automatically.")
    
    add_subsection_header(pdf, "5.1.2", "Application Operations")
    add_bullet_point(pdf, "Start Server", "Run 'npm start' to start the Node.js server. The server runs at http://localhost:3000.")
    add_bullet_point(pdf, "Patient Portal", "Patients can access http://localhost:3000, register their profiles, select their profiles, view upcoming bookings, and book slots with specialist doctors.")
    add_bullet_point(pdf, "Doctor Portal", "Doctors select their name to load their queue of upcoming consultations, mark appointments 'Completed' or 'Cancelled', and run daily cursor stored procedure reports.")
    add_bullet_point(pdf, "Developer Lab Dashboard", "Developers can inspect raw database statistics (patient/doctor/appointment counts), watch database triggers log changes dynamically, and browse history logs.")

    # ====================================================================
    # CHAPTER 6
    # ====================================================================
    print("Writing Chapter 6...")
    add_chapter_header(pdf, "6", "Testing")
    
    add_section_header(pdf, "6.1", "Unit Testing")
    add_body_p(pdf,
        "Unit testing validates individual components and constraints to verify correct schema behavior:"
    )
    add_bullet_point(pdf, "Constraint Validation Test", "Assert that inserting a patient with a duplicate email fails with ER_DUP_ENTRY error code.")
    add_bullet_point(pdf, "Foreign Key Bounds Test", "Confirm that booking an appointment with a non-existent doctor_id (e.g. 99) fails with foreign key constraint errors.")
    add_bullet_point(pdf, "Enum Constraints Test", "Verify that appointments only accept 'Scheduled', 'Completed', and 'Cancelled' as statuses.")
    
    add_section_header(pdf, "6.2", "Integration Testing")
    add_body_p(pdf,
        "Integration testing validates functional pipelines, tracing flows between the client web page, backend server routes, and database objects:"
    )
    add_bullet_point(pdf, "Booking to View Integration Flow", "Register patient John -> Select John -> Submit Booking with Dr. Sarah -> Confirm that the client queries 'upcoming_appointments_view' and displays the new booking correctly.")
    add_bullet_point(pdf, "Trigger Integration Test", "Insert appointment -> Verify that the MySQL engine immediately executes trigger 'after_appointment_insert' and creates an audit row in 'appointment_logs'. Update status -> Confirm that 'after_appointment_update' records the state change details.")
    
    add_section_header(pdf, "6.3", "System Testing")
    add_body_p(pdf,
        "System testing evaluates the performance and concurrency limits under heavy load:"
    )
    add_bullet_point(pdf, "Connection Pool Verification", "Simulate multiple simultaneous requests using Apache Bench. Confirm that the Node.js mysql2 connection pool recycles database threads without timing out.")
    add_bullet_point(pdf, "Cascading Deletions Test", "Delete a patient profile -> Confirm that MySQL cascades the delete and automatically wipes all linked appointments for that patient, preventing orphan records.")
    
    add_section_header(pdf, "6.4", "Acceptance Testing")
    add_body_p(pdf,
        "Acceptance testing verifies that all project requirements specified by the user are satisfied:"
    )
    add_bullet_point(pdf, "User Acceptance Criteria", "Validate that the web interface is functional, responsive, and provides interactive tabs for patient profiles, doctor queues, database logs, and daily cursor reports.")
    add_bullet_point(pdf, "DBMS Features Checklist", "Verify that the three core elements (SQL View, SQL Triggers, and Cursor Stored Procedure) run successfully and integrate with the Node.js API endpoints.")

    # ====================================================================
    # CHAPTER 7
    # ====================================================================
    print("Writing Chapter 7...")
    add_chapter_header(pdf, "7", "Conclusion")
    
    add_section_header(pdf, "7.1", "Conclusion & Future Enhancements")
    add_body_p(pdf,
        "The development of the Patient Appointment Scheduling System ('MediFlow') demonstrates the effectiveness of relational databases in streamlining medical clinic workflows. By implementing constraints, views, triggers, and stored procedures directly at the database level, the system ensures data consistency, automates audit trails, and simplifies scheduling lookups. The 3-tier decoupling guarantees web responsiveness and clean server-client API integration."
    )
    add_body_p(pdf,
        "Future enhancements could include:"
    )
    add_bullet_point(pdf, "Doctor Shift Rosters", "Develop a calendar module to restrict bookings to the doctor's specific working hours.")
    add_bullet_point(pdf, "Real-time Notifications", "Integrate SMS/Email API services (like Twilio or Nodemailer) to email patients their booking details.")
    add_bullet_point(pdf, "Patient Authentications", "Add JWT-based user login authentication to secure patient and doctor portals.")
    add_bullet_point(pdf, "Horizontal Clustering", "Set up database replication (Master-Slave) to allow high availability and backup support.")

    # Save PDF
    temp_filename = "temp_report.pdf"
    output_filename = "patient_appointment_system_report_v4.pdf"
    print(f"Saving compiled PDF to {temp_filename}...")
    try:
        pdf.output(temp_filename)
        merge_preliminary_pages(temp_filename, output_filename)
        print("PDF generation completed successfully!")
    except PermissionError:
        temp_filename = "temp_report_v2.pdf"
        output_filename = "patient_appointment_system_report_v5.pdf"
        print(f"Permission denied for writing. Retrying with fallback filenames: {output_filename}...")
        try:
            pdf.output(temp_filename)
            merge_preliminary_pages(temp_filename, output_filename)
            print("PDF generation completed successfully to fallback filename!")
        except Exception as e:
            print(f"Failed to generate fallback: {str(e)}")

def merge_preliminary_pages(temp_report_path, final_output_path):
    downloads_path = r"C:\Users\HP\Downloads\reppppppppp.pdf"
    if not os.path.exists(downloads_path):
        print(f"Warning: {downloads_path} not found. Saving PDF without preliminary pages.")
        try:
            if os.path.exists(final_output_path):
                os.remove(final_output_path)
            os.rename(temp_report_path, final_output_path)
            print(f"Saved PDF to {final_output_path}")
        except:
            pass
        return
    
    print(f"Prepending first 4 pages of {downloads_path}...")
    try:
        from pypdf import PdfReader, PdfWriter
        reader_source = PdfReader(downloads_path)
        reader_report = PdfReader(temp_report_path)
        writer = PdfWriter()
        
        # Add first 4 pages
        for i in range(min(4, len(reader_source.pages))):
            writer.add_page(reader_source.pages[i])
        # Add report pages
        for page in reader_report.pages:
            writer.add_page(page)
            
        with open(final_output_path, "wb") as f:
            writer.write(f)
        print(f"Saved merged PDF to {final_output_path}")
        # Clean up temp file
        try:
            os.remove(temp_report_path)
        except:
            pass
    except Exception as e:
        print(f"Error merging PDFs: {str(e)}")
        try:
            if os.path.exists(final_output_path):
                os.remove(final_output_path)
            os.rename(temp_report_path, final_output_path)
        except:
            pass

if __name__ == "__main__":
    generate_diagrams()
    build_pdf_report()
