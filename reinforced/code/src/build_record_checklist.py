"""Builds reinforced/manuscript/RECORD_STROBE_checklist.docx (supplement)."""
import os
from docx import Document
from docx.shared import Pt, Cm
RR = "/home/user/rp_c_8/reinforced"
items = [
 ("STROBE 1a", "Title indicates study design; RECORD 1.1 type of data", "Title; Abstract (Methods)", "Done: title and abstract name the linkage of Crossref dates with the Retraction Watch database."),
 ("STROBE 1b", "Informative, balanced abstract", "Abstract", "Done (structured, 4 headings)."),
 ("STROBE 2, 3", "Background, rationale and objectives", "Background", "Done; four questions stated."),
 ("STROBE 4", "Key elements of study design", "Methods: Design, reporting and pre-specification", "Done; protocol and amendments E-A1 to E-A6 in the repository."),
 ("STROBE 5", "Setting, dates, follow-up", "Methods: Data and cohort", "Done: Crossref records 2020–2026, retraction snapshot 24 Nov 2026."),
 ("STROBE 6; RECORD 6.1", "Participants: eligibility, sources, selection codes/algorithms", "Methods: Data and cohort; Table 1", "Done: cohort cleaning rules listed; code in repository (e_build.py)."),
 ("RECORD 6.2", "Validation studies of codes or algorithms", "Limitations", "Not done: Retraction Watch reason labels and the 'process-related' definition were not validated against full notices."),
 ("RECORD 6.3, 12.2", "Linkage of databases, methods and quality", "Methods: Data and cohort", "Done: linkage by lower-cased DOI; coverage and unmatched counts in Table 1; no probabilistic linkage."),
 ("STROBE 7; RECORD 7.1", "Variables: outcomes, exposures, confounders; definitions", "Methods: Outcomes; Exposures", "Done."),
 ("STROBE 8", "Data sources and measurement", "Methods: Data and cohort", "Done."),
 ("STROBE 9", "Bias", "Methods; Discussion; Strengths and limitations", "Done: negative control, circular ascertainment, cohort-selection bias, left truncation discussed."),
 ("STROBE 10", "Study size", "Results: Cohort and outcomes", "Done: whole available population; no sample-size calculation."),
 ("STROBE 11", "Quantitative variables", "Methods: Exposures", "Done: percentile-based flags, bins."),
 ("STROBE 12a–e", "Statistical methods; subgroups; missing data; loss to follow-up; sensitivity", "Methods: Statistical analysis; Results", "Done; missing first-online dates handled by restricting analyses; follow-up handled by strata, Cox model and 24-month window."),
 ("RECORD 12.1", "Extent of data cleaning", "Methods; Table 1; Discussion", "Done; cleaning error found and corrected (amendment E-A6)."),
 ("STROBE 13; RECORD 13.1", "Participants and flow diagram", "Table 1", "Done as a flow table."),
 ("STROBE 14", "Descriptive data", "Tables 1–2", "Done."),
 ("STROBE 15", "Outcome data", "Tables 1–2", "Done."),
 ("STROBE 16", "Main results with precision", "Table 3; Results", "Done: odds ratios with journal-cluster 95% intervals."),
 ("STROBE 17", "Other analyses", "Tables 4–6; Figures 3–4", "Done."),
 ("STROBE 18", "Key results", "Abstract; Discussion", "Done."),
 ("STROBE 19; RECORD 19.1", "Limitations; implications of using routinely collected data", "Strengths and limitations", "Done."),
 ("STROBE 20, 21", "Interpretation; generalisability", "Discussion; Strengths and limitations", "Done."),
 ("STROBE 22; RECORD 22.1", "Funding; availability of protocol, raw data and code", "Declarations", "Partly: protocol, code and data are in a public repository; a DOI-bearing archive and funding statement are to be completed by the authors."),
]
d = Document(); st = d.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(10)
for s in d.sections: s.left_margin = s.right_margin = Cm(2)
d.add_heading("Supplement: STROBE and RECORD checklist", 1)
d.add_paragraph("Manuscript: Fast editorial handling and later retraction for peer-review-related reasons: a journal-adjusted, out-of-time analysis of 1.8 million articles.")
t = d.add_table(rows=1, cols=4); t.style = "Table Grid"
for i, h in enumerate(["Item", "Recommendation", "Location in manuscript", "Status"]): t.rows[0].cells[i].text = h
for r in items:
    cells = t.add_row().cells
    for i, v in enumerate(r): cells[i].text = v
d.save(f"{RR}/manuscript/RECORD_STROBE_checklist.docx"); print("checklist saved")
