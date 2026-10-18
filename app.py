from pathlib import Path
import subprocess
import sys
import shutil

import streamlit as st


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
SRC_DIR = PROJECT_DIR / "src"
REPORT_DIR = PROJECT_DIR / "reports"

SCAN_SCRIPT = SRC_DIR / "local_scan.py"
ANALYSIS_SCRIPT = SRC_DIR / "analyze_report.py"

SCAN_REPORT = REPORT_DIR / "localhost_scan.txt"
SUMMARY_REPORT = REPORT_DIR / "assessment_summary.txt"


# --------------------------------------------------
# STREAMLIT PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Ethical Hacking Lab",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ Ethical Hacking Lab")
st.subheader("Local Security Assessment Dashboard")

st.markdown(
    """
    An educational security assessment dashboard using
    Python and Nmap.
    """
)

st.warning(
    "**Authorized lab use only.** The scan target is fixed "
    "at `127.0.0.1`. On a cloud deployment, this is the "
    "cloud server itself, not your personal computer."
)


# --------------------------------------------------
# PROJECT INFORMATION
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Scan Target", "127.0.0.1")

with col2:
    st.metric("Scanner", "Nmap")

with col3:
    st.metric("Report Analyzer", "Python")

st.divider()


# --------------------------------------------------
# RUN LOCAL SECURITY ASSESSMENT
# --------------------------------------------------

st.header("🔍 Run Local Assessment")

st.write(
    "Run an Nmap service scan against the fixed localhost "
    "target and generate an assessment summary."
)

if st.button("▶ Run Localhost Scan", type="primary"):

    if not SCAN_SCRIPT.is_file():
        st.error("Scanner script not found: src/local_scan.py")

    elif not ANALYSIS_SCRIPT.is_file():
        st.error(
            "Analyzer script not found: src/analyze_report.py"
        )

    elif shutil.which("nmap") is None:
        st.error(
            "Nmap is not installed or is unavailable in PATH. "
            "Install Nmap locally, or check packages.txt and "
            "the deployment build logs on Streamlit Cloud."
        )

    else:
        with st.spinner("Running localhost security scan..."):

            try:
                scan_result = subprocess.run(
                    [
                        sys.executable,
                        str(SCAN_SCRIPT),
                    ],
                    cwd=str(PROJECT_DIR),
                    capture_output=True,
                    text=True,
                    timeout=150,
                    check=False,
                )

                # Display scanner output.
                if scan_result.stdout:
                    st.text("Scanner Output")
                    st.code(
                        scan_result.stdout,
                        language="text",
                    )

                if scan_result.stderr:
                    st.text("Diagnostic Output")
                    st.code(
                        scan_result.stderr,
                        language="text",
                    )

                # The existing scanner catches some errors
                # internally, so also inspect its output.
                scan_succeeded = (
                    scan_result.returncode == 0
                    and "Scan finished." in scan_result.stdout
                    and SCAN_REPORT.is_file()
                )

                if scan_succeeded:

                    analysis_result = subprocess.run(
                        [
                            sys.executable,
                            str(ANALYSIS_SCRIPT),
                        ],
                        cwd=str(PROJECT_DIR),
                        capture_output=True,
                        text=True,
                        timeout=30,
                        check=False,
                    )

                    if analysis_result.stdout:
                        st.code(
                            analysis_result.stdout,
                            language="text",
                        )

                    if analysis_result.returncode == 0:
                        st.success(
                            "Scan completed and the assessment "
                            "summary was generated."
                        )
                    else:
                        st.error(
                            "The scan ran, but summary generation "
                            "failed."
                        )

                        if analysis_result.stderr:
                            st.code(analysis_result.stderr)

                else:
                    st.error(
                        "The scan did not complete successfully. "
                        "Any previously saved report may be from "
                        "an earlier scan."
                    )

            except subprocess.TimeoutExpired:
                st.error(
                    "The scan exceeded the time limit and was stopped."
                )

            except OSError as error:
                st.error(f"Unable to execute the script: {error}")


st.divider()


# --------------------------------------------------
# DISPLAY REPORTS
# --------------------------------------------------

st.header("📄 Assessment Reports")

tab1, tab2 = st.tabs(
    [
        "Scan Report",
        "Assessment Summary",
    ]
)


# --------------------------------------------------
# SCAN REPORT TAB
# --------------------------------------------------

with tab1:

    if SCAN_REPORT.is_file():

        scan_text = SCAN_REPORT.read_text(
            encoding="utf-8",
            errors="replace",
        )

        st.caption(
            "Saved report. Its presence does not mean the latest "
            "scan succeeded."
        )

        st.code(
            scan_text,
            language="text",
        )

        st.download_button(
            label="⬇ Download Scan Report",
            data=scan_text,
            file_name="localhost_scan.txt",
            mime="text/plain",
            key="download_scan_report",
        )

    else:
        st.info(
            "No scan report is available. Run an assessment first."
        )


# --------------------------------------------------
# ASSESSMENT SUMMARY TAB
# --------------------------------------------------

with tab2:

    if SUMMARY_REPORT.is_file():

        summary_text = SUMMARY_REPORT.read_text(
            encoding="utf-8",
            errors="replace",
        )

        st.caption(
            "Saved summary. Check the scan date before relying "
            "on these results."
        )

        st.code(
            summary_text,
            language="text",
        )

        st.download_button(
            label="⬇ Download Assessment Summary",
            data=summary_text,
            file_name="assessment_summary.txt",
            mime="text/plain",
            key="download_assessment_summary",
        )

    else:
        st.info(
            "No assessment summary is available. "
            "Complete a scan first."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Ethical Hacking Lab | Educational project | "
    "An open port is not automatically a vulnerability. "
    "This tool is not a complete security audit."
)