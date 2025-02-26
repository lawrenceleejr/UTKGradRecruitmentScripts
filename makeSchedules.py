import csv
import os
from collections import defaultdict
import shlex

def read_csv_schedule(filename):
    with open(filename, newline='') as csvfile:
        reader = list(csv.reader(csvfile))
        
        # Extract column headers (names of people being met)
        headers = reader[0]  # Row 1
        locations = reader[1]  # Row 2
        
        # Extract times from column A (first column)
        times = [row[0] for row in reader[2:22]]  # Rows 3 to 22
        
        # Extract the names below row 24
        unique_names = set()
        for row in reader[24:]:
            for name in row:
                if name.strip():
                    unique_names.add(name.strip())
        
        # Create schedules for each unique name
        schedules = defaultdict(list)
        for row_index, row in enumerate(reader[2:22], start=2):
            for col_index, name in enumerate(row[1:], start=1):
                if name.strip() in unique_names:
                    schedules[name.strip()].append({
                        "time": times[row_index - 2],
                        "meeting_with": headers[col_index],
                        "location": locations[col_index]
                    })
        
        return schedules

def generate_latex(name, meetings):
    latex_content = f"""\\documentclass{{article}}
\\usepackage{{graphicx}}
\\usepackage{{hyperref}}
\\begin{{document}}

\\begin{{center}}
\\center
\\includegraphics[width=0.5\\textwidth]{{University - CenteredLogo (RGB).jpg}}
\\end{{center}}

\\section*{{Schedule for {name}}}

We're happy to welcome you to the UTK Physics and Astronomy department. Below is your personal schedule of one-on-one meetings with faculty. You can find the shared schedule for the rest of your visit at \\href{{https://indico.phys.utk.edu/event/8/}}{{https://indico.phys.utk.edu/event/8/}}.

\\begin{{itemize}}
"""
    for meeting in meetings:
        latex_content += f"  \\item {meeting['time']} with {meeting['meeting_with']} at {meeting['location']}\n"
    
    latex_content += "\\end{itemize}\n\\end{document}"
    print(latex_content)
    filename = f"{name.replace(' ', '_')}.tex"
    with open(filename, "w") as tex_file:
        tex_file.write(latex_content)
    
    print(filename)
    return filename

def compile_latex(filename):
    # print(f"pdflatex {filename} > /dev/null 2>&1")
    os.system(f"pdflatex {shlex.quote(filename)}")
    temp_files = [filename, filename.replace('.tex', '.aux'), filename.replace('.tex', '.log')]
    for temp in temp_files:
        os.remove(temp)

def main():
    filename = "Meetings with Faculty - Prospective Grad Visit, March 2025 - Sheet1.csv"  # Updated file name
    schedules = read_csv_schedule(filename)
    
    for name, meetings in schedules.items():
        tex_file = generate_latex(name, meetings)
        compile_latex(tex_file)

if __name__ == "__main__":
    main()

