from pathlib import Path

import streamlit as st
from PIL import Image

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
# resume_file = current_dir / "assets" / "CV.pdf"
profile_pic = current_dir / "assets" / "profile-pic.png"

# --- GENERAL SETTINGS ---
PAGE_TITLE = "DevOps Professional | Kunal Jha"
PAGE_ICON = ":wave:"
NAME = "_Kunal Jha_"
DESCRIPTION = f"Senior DevOps Engineer, specializing in automation and optimizing CI/CD processes " \
              f"for seamless and efficient software delivery in enterprise environments."
EMAIL = "kunaljha5@gmail.com"
SOCIAL_MEDIA = {
    "LinkedIn": "https://linkedin.com/in/kunaljha5",
    "GitHub": "https://github.com/kunaljha5"
}

PROJECTS = {
    "🏆 AWS Dev Environment - Full infrastructure setup on AWS Cloud for Clearance and Settlement platform": "cloud/"
                                                                                                            "internal",
    "🏆 Jenkins Migration - Migrated Pipelines from Bamboo to Jenkins": "CICD/internal",
    "🏆 Slack Commands - Slack Commands to to giving easy access to applications and environment": "automation/internal",
    "🏆 Release Automation - Create Release Automation Framework in python to automate the Release work.": "automation"
                                                                                                          "/internal"
}


st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# --- LOAD CSS, PDF & PROFIL PIC ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
# with open(resume_file, "rb") as pdf_file:
#    PDFbyte = pdf_file.read()
profile_pic = Image.open(profile_pic)

# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small")
with col1:
    st.image(profile_pic, width=230)

with col2:
    st.title(NAME)
    st.write(DESCRIPTION)
    st.write("📫", EMAIL)


# --- SOCIAL LINKS ---
st.write('\n')
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f"[{platform}]({link})")

# --- EXPERIENCE & QUALIFICATIONS ---
st.write('\n')
st.subheader("_Experience & Qualifications_")
st.write(
    """
- ✔️ 11+ Years of Experience in optimizing critical deployments across large infrastructure
- ✔️ Strong hands on experience in Linux, AWS, Terraform, Python & Jenkins
- ✔️ Good understanding of CI/CD , Change and Release processes
- ✔️ Excellent team-player and displaying strong sense of initiative on tasks
"""
)


# --- SKILLS ---
st.write('\n')
st.subheader("Hard Skills")
st.write(
    """
- 👩‍💻 Programming: Python, Groovy, Bash Scripting
- 📊 CI CD Tools: Jenkins, Bamboo, Artifactory, Bitbucket, Jira, Confluence, 
- 🗄️ Databases: Oracle, MySQL
"""
)


# --- WORK HISTORY ---
st.write('\n')
st.subheader("Work History")
st.write("---")

# --- JOB 1
st.header(":point_right: Global Payments | `JUN/2018 - Present`")
role_details_job1 = """\n
|             Role              |       Duration        |
|:-----------------------------:|:---------------------:|
| `Associate DevOps Consultant` | `JUL/2022 - Present`  |
|    `Lead DevOps Engineer`     | `JAN/2021 - JUL/2022` |
|       `DevOps Engineer`       | `OCT/2019 - JAN/2021` |
|        `SDET Engineer`        | `JUN/2018 - OCT/2019` |
"""
st.markdown(role_details_job1)
st.write("\n")
st.write(
    """\n
- ► AWS Dev Account Setup & Integration with On Prem
- ► Terraform Module Development
- ► Release Automation
- ► Slack Command Automation
- ► Bamboo to Jenkins Migration
- ► AWS PinPoint Integration
- ► AWS API Gateway Development for CMT
- ► CI/CD Tools Upgrade & Maintenance
"""
)

# --- JOB 2
st.write('\n---')
st.header(":point_right: Ericsson | `DEC/2011 - JUN/2018`")
role_details_job2 = """
|              Role              |        Duration        |
|:------------------------------:|:----------------------:|
| `Senior Integration Engineer`  | `SEP/2017 - JUN/2018`  |
|       `Senior Engineer`        | `APR/2015 - SEP/2017`  |
|      `Services Engineer`       | `DEC/2011 - APR/2015`  |
"""
st.markdown(role_details_job2)
st.write(
    """
- ► 
"""
)
