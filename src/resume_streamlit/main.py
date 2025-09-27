import base64
import sys
from pathlib import Path

import streamlit as st
from PIL import Image
from resources import config as cfg

sys.path.append(str(Path(__file__).parent))


def get_image_mime_type(image_path):
    """Get MIME type for image based on file extension"""
    path_str = str(image_path).lower()
    if path_str.endswith(".svg"):
        return "image/svg+xml"
    elif path_str.endswith(".png"):
        return "image/png"
    elif path_str.endswith((".jpg", ".jpeg")):
        return "image/jpeg"
    else:
        return "image/png"  # default


def get_resource_path(resource_path):
    """Get the correct path to package resources."""
    try:
        from importlib.resources import files

        package_dir = files("resume_streamlit")
        return package_dir / resource_path
    except (ImportError, ModuleNotFoundError):
        # Fallback to file-based path for development
        current_dir = Path(__file__).parent
        return current_dir / resource_path


def get_base64_image(image_path):
    """Convert image to base64 string for HTML embedding"""
    try:
        # Handle both Path objects and strings
        if hasattr(image_path, "open"):
            # It's a Path-like object from importlib.resources
            with image_path.open("rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        else:
            # It's a regular file path
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    except (FileNotFoundError, AttributeError):
        st.warning(f"Could not load image: {image_path}")
        return None


def work_history(index):
    st.markdown('<div class="work-history-item">', unsafe_allow_html=True)

    # Company header with modern card design
    logo_filename = cfg.JOBS[index]["LOGO"]
    logo_resource = get_resource_path(f"{logo_filename}")
    base64_image = get_base64_image(logo_resource)
    mime_type = get_image_mime_type(logo_filename)

    if base64_image:
        company_header_html = f"""
                        <h3 style="margin-bottom: 0.5rem;">
                            <img src="data:{mime_type};base64,{base64_image}"
                                 style="width: 22px; height: 22px; margin-right: 10px; vertical-align: middle; border-radius: 4px;" />
                            {cfg.JOBS[index]["COMPANY"]}
                        </h3>
                        """
    else:
        company_header_html = f"""
                        <h3 style="margin-bottom: 0.5rem;">
                            🏢 {cfg.JOBS[index]["COMPANY"]}
                        </h3>
                        """
    st.markdown(company_header_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Main company expander (Level 1) with tabs inside
    with st.expander(f"{cfg.JOBS[index]['POSITION']}", expanded=False):
        # Create tabs for the three sections
        tab1, tab2, tab3 = st.tabs(
            [
                "⏱️ Duration & Overview",
                "📋 Roles & Career Progression",
                "🚀 Key Achievements & Responsibilities",
            ]
        )

        with tab1:
            # Create data for the table
            table_data = [["Duration", cfg.JOBS[index]["DURATION"]]]

            # Add position if available
            if "POSITION" in cfg.JOBS[index]:
                table_data.append(["Position", cfg.JOBS[index]["POSITION"]])

            # Add location if available
            if "LOCATION" in cfg.JOBS[index]:
                table_data.append(["Location", cfg.JOBS[index]["LOCATION"]])

            # Add impact if available
            if "IMPACT" in cfg.JOBS[index]:
                table_data.append(["Impact Scope", cfg.JOBS[index]["IMPACT"]])

            # Create and display the table
            import pandas as pd

            df = pd.DataFrame(table_data, columns=["Key", "Value"])
            st.dataframe(df, hide_index=True, width="content")

        with tab2:
            st.markdown(cfg.JOBS[index]["ROLES"])

        with tab3:
            st.markdown('<div class="achievements-section">', unsafe_allow_html=True)
            st.markdown(cfg.JOBS[index]["RESP"])
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def load_resource_safely(resource_path, is_image=False, is_text=False):
    """Safely load a resource file."""
    try:
        # Try importlib.resources first
        from importlib.resources import files

        package_dir = files("resume_streamlit")
        resource_file = package_dir / resource_path

        if is_image:
            # For images, we need to handle them as binary
            with resource_file.open("rb") as f:
                return Image.open(f).copy()
        elif is_text:
            # For text files like CSS
            return resource_file.read_text(encoding="utf-8")
        else:
            return resource_file

    except (ImportError, ModuleNotFoundError, FileNotFoundError, AttributeError):
        # Fallback to file system path
        current_dir = Path(__file__).parent
        file_path = current_dir / resource_path

        if is_image and file_path.exists():
            return Image.open(file_path)
        elif is_text and file_path.exists():
            return file_path.read_text(encoding="utf-8")
        elif file_path.exists():
            return file_path
        else:
            return None


def home_page():
    # --- PAGE CONFIG ---
    st.set_page_config(
        page_title=cfg.PAGE_TITLE,
        page_icon=cfg.PAGE_ICON,
        # initial_sidebar_state="expanded",
        layout="wide",
    )

    # --- LOAD RESOURCES ---
    # Load CSS
    css_content = load_resource_safely("styles/main.css", is_text=True)
    if css_content:
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        st.warning("CSS file not found. Please ensure styles/main.css exists in your package.")

    # Load profile picture
    profile_pic = load_resource_safely("assets/profile-pic.png", is_image=True)
    if not profile_pic:
        st.error("Profile picture not found. Please ensure assets/profile-pic.png exists in your package.")
        return

    # --- MODERN HERO SECTION ---
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)

    # Top row: Image and basic info with better spacing
    col1, col2, col3 = st.columns([1, 2, 1], gap="large")

    with col1:
        st.markdown('<div class="profile-container">', unsafe_allow_html=True)
        if profile_pic:
            st.image(profile_pic, width=200)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="header-content">', unsafe_allow_html=True)
        st.title(cfg.NAME)
        st.markdown(f'<div class="job-titles">{cfg.HEADER_TITLE}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        contact_html = cfg.HEADER_CONTACT.replace("\n", "<br>")
        st.markdown(f'<div class="job-titles">{contact_html}</div>', unsafe_allow_html=True)

    with st.expander("📌 Contact Info"):
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            st.markdown(f'<a href="mailto:{cfg.EMAIL}">📧 Email</a>', unsafe_allow_html=True)
        with col2:
            st.markdown(
                f'<a href="{cfg.SOCIAL_MEDIA["LinkedIn"]}" target="_blank">💼 LinkedIn</a>',
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                f'<a href="{cfg.SOCIAL_MEDIA["GitHub"]}" target="_blank">💻 GitHub</a>',
                unsafe_allow_html=True,
            )
        with col4:
            st.markdown(
                f'<a href="{cfg.SOCIAL_MEDIA["Mobile"]}" target="_blank">📞 Mobile</a>',
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
        st.title("📋 Navigation")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # Add current section indicator
        st.markdown("**Current Section:**")
        st_section = st.radio("Choose a section:", cfg.SECTIONS, label_visibility="collapsed")

        st.markdown("---")

        # Add quick stats or info
        st.markdown("**Quick Stats:**")
        st.markdown("📊 13+ Years Experience")
        st.markdown("☁️ AWS & DevOps Expert")
        st.markdown("🚀 50+ Deployments")
        st.markdown("🏆 5+ Certifications")
    return st_section


# def st_routing(st_section):
#     if st_section == "Executive Summary":
#         st.write("\n")
#         st.markdown(cfg.EXECUTIVE_SUMMARY)
#
#     elif st_section == "Core Competencies":
#         st.markdown('<div class="skills-section">', unsafe_allow_html=True)
#         st.subheader("_Core Competencies & Technical Expertise_")
#         st.write("")
#
#         tabs = st.tabs(
#             [
#                 "☁️ Cloud Architecture",
#                 "🔒 DevSecOps",
#                 "📊 Site Reliability",
#                 "🔄 CI/CD & Release",
#                 "💻 Development & Data",
#             ]
#         )
#
#         skills_mapping = {
#             0: "Cloud & Infrastructure Excellence",
#             1: "DevSecOps & Security",
#             2: "Observability & Site Reliability Engineering",
#             3: "CI/CD & Release Engineering",
#             4: "Programming & Automation",
#         }
#
#         for i, tab in enumerate(tabs):
#             with tab:
#                 if i in skills_mapping and skills_mapping[i] in cfg.SKILLS:
#                     section_data = cfg.SKILLS[skills_mapping[i]]
#                     for category, skills_list in section_data.items():
#                         st.markdown(f"**{category}:**")
#                         st.markdown(" - " + ", ".join(skills_list))
#                         st.markdown("")
#                 else:
#                     st.markdown("*Section content not available*")
#
#     elif st_section == "Current & Past Roles":
#         st.write("\n")
#         st.subheader("_Current Role_")
#         work_history(0)
#
#         for each in range(1, len(cfg.JOBS)):
#             work_history(each)
#
#     elif st_section == "Key Achievements & Recognition":
#         st.markdown('<div class="achievements-section">', unsafe_allow_html=True)
#         st.subheader("_Key Achievements & Recognition_")
#         st.markdown("**🏆 Notable accomplishments and successful project deliveries**")
#         st.write("")
#
#         for i, project in enumerate(cfg.PROJECTS.keys(), 1):
#             with st.container():
#                 st.markdown(f"**{i}.** {project}")
#                 st.write("")
#
#         st.markdown("</div>", unsafe_allow_html=True)
#
#     elif st_section == "Professional Development":
#         st.markdown('<div class="certifications-section">', unsafe_allow_html=True)
#         st.subheader("_Professional Development & Certifications_")
#
#         cert_tabs = st.tabs(["🏅 Current Certifications", "📖 Learning Path"])
#
#         with cert_tabs[0]:
#             st.markdown(cfg.CERTIFICATIONS)
#
#         with cert_tabs[1]:
#             st.markdown(cfg.ONGOING_FUTURE_DEVELOPMENT)
#         st.markdown("</div>", unsafe_allow_html=True)
#
#     elif st_section == "Education & Background":
#         st.markdown('<div class="education-section">', unsafe_allow_html=True)
#         st.subheader("_Education & Academic Foundation_")
#         st.markdown("**🎓 Academic background and foundational knowledge**")
#         st.write("")
#         st.markdown(cfg.EDUCATION)
#         st.markdown("</div>", unsafe_allow_html=True)


def render_executive_summary():
    st.write("\n")
    st.markdown(cfg.EXECUTIVE_SUMMARY)


def render_core_competencies():
    st.markdown('<div class="skills-section">', unsafe_allow_html=True)
    st.subheader("_Core Competencies & Technical Expertise_")
    st.write("")

    tabs = st.tabs(
        [
            "☁️ Cloud Architecture",
            "🔒 DevSecOps",
            "📊 Site Reliability",
            "🔄 CI/CD & Release",
            "💻 Development & Data",
        ]
    )

    skills_mapping = {
        0: "Cloud & Infrastructure Excellence",
        1: "DevSecOps & Security",
        2: "Observability & Site Reliability Engineering",
        3: "CI/CD & Release Engineering",
        4: "Programming & Automation",
    }

    for i, tab in enumerate(tabs):
        with tab:
            if i in skills_mapping and skills_mapping[i] in cfg.SKILLS:
                section_data = cfg.SKILLS[skills_mapping[i]]
                for category, skills_list in section_data.items():
                    st.markdown(f"**{category}:**")
                    st.markdown(" - " + ", ".join(skills_list))
                    st.markdown("")
            else:
                st.markdown("*Section content not available*")


def render_current_roles():
    st.write("\n")
    st.subheader("_Current Role_")
    work_history(0)

    for each in range(1, len(cfg.JOBS)):
        work_history(each)


def render_achievements():
    st.markdown('<div class="achievements-section">', unsafe_allow_html=True)
    st.subheader("_Key Achievements & Recognition_")
    st.markdown("**🏆 Notable accomplishments and successful project deliveries**")
    st.write("")

    for i, project in enumerate(cfg.PROJECTS.keys(), 1):
        with st.container():
            st.markdown(f"**{i}.** {project}")
            st.write("")

    st.markdown("</div>", unsafe_allow_html=True)


def render_professional_development():
    st.markdown('<div class="certifications-section">', unsafe_allow_html=True)
    st.subheader("_Professional Development & Certifications_")

    cert_tabs = st.tabs(["🏅 Current Certifications", "📖 Learning Path"])

    with cert_tabs[0]:
        st.markdown(cfg.CERTIFICATIONS)

    with cert_tabs[1]:
        st.markdown(cfg.ONGOING_FUTURE_DEVELOPMENT)

    st.markdown("</div>", unsafe_allow_html=True)


def render_education():
    st.markdown('<div class="education-section">', unsafe_allow_html=True)
    st.subheader("_Education & Academic Foundation_")
    st.markdown("**🎓 Academic background and foundational knowledge**")
    st.write("")
    st.markdown(cfg.EDUCATION)
    st.markdown("</div>", unsafe_allow_html=True)


def st_routing(st_section):
    routing_map = {
        "Executive Summary": render_executive_summary,
        "Core Competencies": render_core_competencies,
        "Current & Past Roles": render_current_roles,
        "Key Achievements & Recognition": render_achievements,
        "Professional Development": render_professional_development,
        "Education & Background": render_education,
    }

    # Call the correct function, or show fallback if not found
    func = routing_map.get(st_section)
    if func:
        func()
    else:
        st.write("⚠️ Section not implemented.")


def main():
    home_page()
    # Enhanced Sidebar Navigation
    st_section = sidebar()
    # --- SECTION ROUTING ---
    st_routing(st_section)


if __name__ == "__main__":
    main()
