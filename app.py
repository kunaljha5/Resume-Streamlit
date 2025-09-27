from pathlib import Path
import base64
import streamlit as st
from PIL import Image

import resources.config as cfg

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
# resume_file = current_dir / "assets" / "CV.pdf"
profile_pic = current_dir / "assets" / "profile-pic.png"
bvs_logo = current_dir / "assets" / "bvs.png"
gp_logo = current_dir / "assets" / "gp.svg"

# --- GENERAL SETTINGS ---


st.set_page_config(page_title=cfg.PAGE_TITLE, page_icon=cfg.PAGE_ICON, initial_sidebar_state="expanded", layout="wide")

# --- LOAD CSS, PDF & PROFILE PIC ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
# with open(resume_file, "rb") as pdf_file:
#    PDFbyte = pdf_file.read()
profile_pic = Image.open(profile_pic)

# --- MODERN HERO SECTION ---
# Create a more professional header layout
st.markdown('<div class="hero-container">', unsafe_allow_html=True)

# Top row: Image and basic info with better spacing
col1, col2, col3 = st.columns([1, 2, 1], gap="large")

with col1:
    st.markdown('<div class="profile-container">', unsafe_allow_html=True)
    st.image(profile_pic, width=200, channels="BGR")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="header-content">', unsafe_allow_html=True)
    st.title(cfg.NAME)
    st.markdown(f'<div class="job-titles">{cfg.HEADER_TITLE}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    contact_html = cfg.HEADER_CONTACT.replace("\n", "<br>")
    st.markdown(f'<div class="job-titles">{contact_html}</div>', unsafe_allow_html=True)


with st.expander("📌 Contact Info"):
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        st.markdown(f'<a href="mailto:{cfg.EMAIL}">📧 Email</a>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<a href="{cfg.SOCIAL_MEDIA["LinkedIn"]}" target="_blank">💼 LinkedIn</a>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<a href="{cfg.SOCIAL_MEDIA["GitHub"]}" target="_blank">💻 GitHub</a>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<a href="{cfg.SOCIAL_MEDIA["Mobile"]}" target="_blank">📞 Mobile</a>', unsafe_allow_html=True)


st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

def get_base64_image(image_path):
    """Convert image to base64 string for HTML embedding"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

def get_image_mime_type(image_path):
    """Get MIME type for image based on file extension"""
    if str(image_path).lower().endswith('.svg'):
        return 'image/svg+xml'
    elif str(image_path).lower().endswith('.png'):
        return 'image/png'
    elif str(image_path).lower().endswith('.jpg') or str(image_path).lower().endswith('.jpeg'):
        return 'image/jpeg'
    else:
        return 'image/png'  # default

def work_history(index):
    st.markdown('<div class="work-history-item">', unsafe_allow_html=True)

    # Company header with modern card design
    # st.markdown(f'<div class="company-header">', unsafe_allow_html=True)
    logo_path = current_dir /  cfg.JOBS[index]["LOGO"]
    base64_image = get_base64_image(logo_path)
    mime_type = get_image_mime_type(logo_path)
    # st.markdown(f'<h3 style="margin-bottom: 0.5rem;">🏢 {cfg.JOBS[index]["COMPANY"]}</h3>', unsafe_allow_html=True)
    if base64_image:
        company_header_html = f'''
                    <h3 style="margin-bottom: 0.5rem;">
                        <img src="data:{mime_type};base64,{base64_image}"
                             style="width: 22px; height: 22px; margin-right: 10px; vertical-align: middle; border-radius: 4px;" />
                        {cfg.JOBS[index]["COMPANY"]}
                    </h3>
                    '''
    else:
        company_header_html = f'''
                    <h3 style="margin-bottom: 0.5rem;">
                        🏢 {cfg.JOBS[index]["COMPANY"]}
                    </h3>
                    '''
    st.markdown(company_header_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Impact statement with modern design
    # if 'IMPACT' in cfg.JOBS[index]:
    #     st.info(f"🎯 **Impact Scope:** {cfg.JOBS[index]['IMPACT']}")

    # Main company expander (Level 1) with tabs inside
    with st.expander(f"{cfg.JOBS[index]['POSITION']}", expanded=False):

        # Create tabs for the three sections
        tab1, tab2, tab3 = st.tabs(
            ["⏱️ Duration & Overview", "📋 Roles & Career Progression", "🚀 Key Achievements & Responsibilities"])

        with tab1:
            # Create data for the table
            table_data = []

            # Add duration
            table_data.append(["Duration", cfg.JOBS[index]['DURATION']])

            # Add position if available
            if 'POSITION' in cfg.JOBS[index]:
                table_data.append(["Position", cfg.JOBS[index]['POSITION']])

            # Add location if available
            if 'LOCATION' in cfg.JOBS[index]:
                table_data.append(["Location", cfg.JOBS[index]['LOCATION']])

            # Add impact if available
            if 'IMPACT' in cfg.JOBS[index]:
                table_data.append(["Impact Scope", cfg.JOBS[index]['IMPACT']])

            # Create and display the table
            import pandas as pd
            df = pd.DataFrame(table_data, columns=["Key", "Value"])
            st.dataframe(df, hide_index=True, width='content')

        with tab2:
            st.markdown(cfg.JOBS[index]['ROLES'])

        with tab3:
            st.markdown('<div class="achievements-section">', unsafe_allow_html=True)
            st.markdown(cfg.JOBS[index]['RESP'])
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# Enhanced Sidebar Navigation
with st.sidebar:
    st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
    st.title('📋 Navigation')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Add current section indicator
    st.markdown("**Current Section:**")
    st_section = st.radio(
        "Choose a section:",
        cfg.SECTIONS,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Add quick stats or info
    st.markdown("**Quick Stats:**")
    st.markdown("📊 13+ Years Experience")
    st.markdown("☁️ AWS & DevOps Expert")
    st.markdown("🚀 50+ Deployments")
    st.markdown("🏆 5+ Certifications")

if st_section == "Executive Summary":
    # --- EXECUTIVE SUMMARY ---
    st.write('\n')
    st.subheader("_Executive Summary_")
#     st.markdown('<div class="executive-summary">', unsafe_allow_html=True)
    st.markdown(cfg.EXECUTIVE_SUMMARY)
#    st.markdown('</div>', unsafe_allow_html=True)

elif st_section == "Core Competencies":
    # --- ENHANCED SKILLS SECTION ---
    st.markdown('<div class="skills-section">', unsafe_allow_html=True)
    st.subheader("_Core Competencies & Technical Expertise_")

    # Add a brief intro
    # st.markdown("**🎯 Specialized in cloud-native solutions and enterprise-scale infrastructure automation**")
    st.write("")

    # Enhanced tabs with better organization
    tabs = st.tabs([
        "☁️ Cloud Architecture",
        "🔒 DevSecOps",
        "📊 Site Reliability",
        "🔄 CI/CD & Release",
        "💻 Development & Data"
    ])

    with tabs[0]:
        st.markdown("""
        **AWS:** 
        - EC2, S3, EKS, Lambda, CloudWatch, MSK, IAM, Route53, API Gateway, Connect\n
        **Infrastructure as Code:** 
        -  Terraform, Ansible, CloudFormation, GitOps Workflows\n
        **Container Orchestration:** 
        - Docker, Kubernetes, EKS, Service Mesh Architecture
        """)

    with tabs[1]:
        st.markdown("""
        **Security Automation:** 
        - HashiCorp Vault, AWS Secrets Manager, SonarQube, Trivy Scanner\n
        **DevSecOps Practices:** 
        - Zero-Trust Architecture, Compliance Automation, Vulnerability Management\n
        **Identity & Access:** 
        - RBAC, Federated Authentication, SSO Integration\n
        """)

    with tabs[2]:
        st.markdown("""
        **Monitoring Platforms:** 
        - Prometheus, Grafana, AlertManager, PagerDuty, Elastic Stack (ELK/EFK)\n
        **APM & Tracing:** 
        - Distributed tracing, Performance optimization, Capacity planning\n
        **Incident Management:** 
        - SLA/SLO definition, MTTR optimization, Blameless post-mortems\n
        """)

    with tabs[3]:
        st.markdown("""
        **Pipeline Orchestration:** 
        - Jenkins, GitLab CI/CD, GitHub Actions, Bamboo\n
        **Release Management:** 
        - Blue-green deployments, Canary releases, Feature flagging\n
        **Quality Engineering:** 
        - Automated testing, Code quality gates, Security scanning\n
        """)

    with tabs[4]:
        st.markdown("""
        **Languages:** 
        - Python, Shell/Bash, Groovy, Perl, SQL\n
        **Databases:** 
        - MySQL, PostgreSQL, Redis, Elasticsearch, MinIO\n
        **API Management:** 
        - RESTful services, GraphQL, Microservices communication\n
        """)

elif st_section == "Current & Past Roles":
    # --- CURRENT ROLE ---
    st.write('\n')
    st.subheader("_Current Role_")
    work_history(0)
#
# elif st_section == "Previous Roles - Transformation Journey":
#     # --- PREVIOUS ROLES ---
#     st.write('\n')
#     st.subheader("_Previous Roles - Transformation Journey_")
    for each in range(1, len(cfg.JOBS)):
        work_history(each)

elif st_section == "Key Achievements & Recognition":
    # --- Enhanced Projects & Accomplishments ---
    st.markdown('<div class="achievements-section">', unsafe_allow_html=True)
    st.subheader("_Key Achievements & Recognition_")

    st.markdown("**🏆 Notable accomplishments and successful project deliveries**")
    st.write("")

    # Display achievements with better styling
    for i, (project, link) in enumerate(cfg.PROJECTS.items(), 1):
        with st.container():
            st.markdown(f'<div class="achievement-item">', unsafe_allow_html=True)
            st.markdown(f"**{i}.** {project}")
            if link:  # If there's a link, display it
                st.markdown(f"[View Details]({link})")
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("")  # Add spacing

    st.markdown('</div>', unsafe_allow_html=True)

elif st_section == "Professional Development":
    # --- Enhanced Certifications Section ---
    st.markdown('<div class="certifications-section">', unsafe_allow_html=True)
    st.subheader("_Professional Development & Certifications_")

    st.markdown("**📚 Continuous learning and industry-recognized expertise**")
    st.write("")

    # Create tabs for better organization
    cert_tabs = st.tabs(["🏅 Current Certifications", "📖 Learning Path"])

    with cert_tabs[0]:
        st.markdown(cfg.CERTIFICATIONS)

    with cert_tabs[1]:
        st.markdown("""
        **Ongoing Professional Development:**
        - 🎯 Advanced Kubernetes Administration (CKA preparation)
        - 🎯 AWS Solutions Architect Professional track
        - 🎯 HashiCorp Terraform Associate certification
        - 🎯 Certified Information Systems Security Professional (CISSP)
        """)

    st.markdown('</div>', unsafe_allow_html=True)

elif st_section == "Education & Background":
    # --- Enhanced Education Section ---
    st.markdown('<div class="education-section">', unsafe_allow_html=True)
    st.subheader("_Education & Academic Foundation_")

    st.markdown("**🎓 Academic background and foundational knowledge**")
    st.write("")

    st.markdown(cfg.EDUCATION)
    st.markdown('</div>', unsafe_allow_html=True)

