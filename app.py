from pathlib import Path

import streamlit as st
from PIL import Image

import resources.config as cfg

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
# resume_file = current_dir / "assets" / "CV.pdf"
profile_pic = current_dir / "assets" / "profile-pic.png"

# --- GENERAL SETTINGS ---


st.set_page_config(page_title=cfg.PAGE_TITLE, page_icon=cfg.PAGE_ICON)

# --- LOAD CSS, PDF & PROFILE PIC ---
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
    st.title(cfg.NAME)
    st.write(cfg.DESCRIPTION)
    st.write("📫", cfg.EMAIL)


# --- SOCIAL LINKS ---
st.write('\n')
cols = st.columns(len(cfg.SOCIAL_MEDIA))
for index, (platform, link) in enumerate(cfg.SOCIAL_MEDIA.items()):
    cols[index].write(f"[{platform}]({link})")


def work_history(index):
    st.write("---")
    st.header(f":point_right: | `{cfg.JOBS[index]['COMPANY']}` | `{cfg.JOBS[index]['DURATION']}`")
    st.write("---")
    st.subheader("_Roles_")
    st.write("---")
    st.markdown(cfg.JOBS[index]['ROLES'])
    st.write("\n")
    st.subheader("_Responsibilities_")
    st.write("---")
    st.write(cfg.JOBS[index]['RESP'])


# Sidebar section
st.sidebar.title('Jump to Sections')
st_section = st.sidebar.radio(" ", cfg.SECTIONS)

if st_section == "Experience Qualifications":
    # --- EXPERIENCE & QUALIFICATIONS ---
    st.write('\n')
    st.subheader("_Experience & Qualifications_")
    st.write(
      cfg.SUMMARY
    )
    st.write("---\n")
    st.subheader("_Education_")
    st.markdown(cfg.EDUCATION)


elif st_section == "Skills":
    # --- SKILLS ---
    st.write('\n')
    st.subheader("_Skills & Certifications_")
    st.write(cfg.SKILLS)

elif st_section in ["Current Employer", "Past Employer"]:
    # --- WORK HISTORY ---
    st.write('\n')
    st.subheader("_Work History_")
    if st_section == "Current Employer":
        index = -1
        work_history( index=index)
    else:
        for each in range(len(cfg.JOBS)-1):
            work_history(each)

elif st_section == "Accomplishments":
    # --- Projects & Accomplishments ---
    st.write('\n')
    st.subheader("_Accomplishments_")
    st.write("---")
    for project, link in cfg.PROJECTS.items():
        st.write(f"[{project}]({link})")

