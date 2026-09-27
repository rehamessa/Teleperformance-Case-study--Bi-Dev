"""
Task 8 — Classify employees into experience levels
=====================================================
Rule (based on TotalWorkingYears):
    Junior : < 5 years
    Mid    : 5 to 9 years
    Senior : 10+ years

Output: a summary table with two columns — ExperienceLevel, EmployeeCount
"""

import pandas as pd

# ---------------------------------------------------------------
# 1) Load the data
# ---------------------------------------------------------------
FILE_PATH = "Data/GBS BI HUB - BI Developer - HR Attrition Case Study (1).xlsx"
SHEET_NAME = "WA_Fn-UseC_-HR-Employee-Attriti"

df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)

# ---------------------------------------------------------------
# 2) Classify each employee by TotalWorkingYears
# ---------------------------------------------------------------
def classify_experience(years: int) -> str:
    """Return the experience-level label for a given TotalWorkingYears value."""
    if years < 5:
        return "Junior"
    elif years < 10:          # covers 5, 6, 7, 8, 9
        return "Mid"
    else:                     # 10 and above
        return "Senior"

df["ExperienceLevel"] = df["TotalWorkingYears"].apply(classify_experience)

# ---------------------------------------------------------------
# 3) Build the summary table (ExperienceLevel, EmployeeCount)
# ---------------------------------------------------------------
summary = (
    df.groupby("ExperienceLevel")
    .size()
    .rename("EmployeeCount")
    .reset_index()
)

# Order the rows logically (Junior -> Mid -> Senior) instead of alphabetically
level_order = pd.CategoricalDtype(["Junior", "Mid", "Senior"], ordered=True)
summary["ExperienceLevel"] = summary["ExperienceLevel"].astype(level_order)
summary = summary.sort_values("ExperienceLevel").reset_index(drop=True)

# ---------------------------------------------------------------
# 4) Display the result
# ---------------------------------------------------------------
print(summary.to_string(index=False))

# ---------------------------------------------------------------
# 5) Sanity check: every employee must be classified, none lost
# ---------------------------------------------------------------
assert summary["EmployeeCount"].sum() == len(df), "Row count mismatch after classification!"