import os
import pandas as pd
from AuD_Utilities import AuD

self = AuD.AuDAccess()
script_dir = os.path.dirname(os.path.abspath(__file__))
print(script_dir)
excel_path = os.path.join(script_dir, "AutomationProjects.xlsx")
print(excel_path)
project_root = os.path.dirname(script_dir)
print(project_root)

import pandas as pd

df = pd.read_excel(excel_path, engine="openpyxl")

if "ProjectName" in df.columns:
    projects = df["ProjectName"].dropna().tolist()
    print("Projects found:")
    for p in projects:
        print("Project------->",p)
        FileName = os.path.join(project_root, p)
        print("Project Exists-->",os.path.exists(FileName),"Project Name-->",FileName)
        self.Start()
        self.Show()
        Project = self.OpenProject(FileName)
        self.ExecuteProject(Project,1,"Report")       