import streamlit as st
import pandas as pd
from pdf_report import generate_assessment_pdf

st.set_page_config(
    page_title="MHDRM Data Readiness Assessment",
     page_icon="🏥",
     layout="wide",
)

# colors and styling
st.markdown(
    """
    <style>
    /* Main page */
    .stApp {
        background-color: #f5f8fa;
    }

    /* Limit width and improve spacing */
    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Main headings */
    h1 {
        color: #123b5d;
    }

    h2 {
        color: #176b78;
        border-bottom: 2px solid #d5e5e8;
        padding-bottom: 0.35rem;
    }

    h3 {
        color: #24556f;
    }

    /* Expanders containing the seven pillars */
    [data-testid="stExpander"] {
        background-color: #ffffff;
        border: 1px solid #c9dce3;
        border-left: 5px solid #258395;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(18, 59, 93, 0.07);
        margin-bottom: 0.75rem;
    }

    /* Text inputs and text areas */
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {
        background-color: #ffffff;
        border-color: #abc9d1;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #c9dce3;
        border-top: 4px solid #258395;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 6px rgba(18, 59, 93, 0.07);
    }

    /* Primary buttons */
    .stButton > button,
    .stDownloadButton > button {
        background-color: #176b78;
        color: white;
        border: none;
        border-radius: 6px;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background-color: #123b5d;
        color: white;
        border: none;
    }

    /* Captions */
    [data-testid="stCaptionContainer"] {
        color: #55717e;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("MHDRM Cross-Site Data Readiness Assessment Tool")

# add colored banner
st.markdown(
    """
    <div style="
        background: linear-gradient(90deg, #123b5d, #258395);
        padding: 1.25rem 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1.25rem;
    ">
        <div style="font-size: 1.15rem; font-weight: 600;">
            Cross-Site Multimodal Federated Learning
        </div>
        <div style="margin-top: 0.35rem;">
            Evaluate preliminary data compatibility across prospective
            healthcare participants.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("""
    This prototype assessment tool evaluates whether 
    participating healthcare organizations have the data, 
    standards, controls, and governance needed for a 
    defined cross-site multimodal federated learning use 
    case. Ratings should reflect current, documented 
    capabilities rather than planned future capabilities.

    NOTE: This tool provides a preliminary preimplementation assessment. 
        Its results are not an empirical validation, certification, privacy
        determination, or guarantee of MMFL project success.
""")

# collect data on the project, participating sites, and data requirements
st.header("Assessment Context")

st.caption(
    """
    Provide context for the proposed MMFL initiative. This information will
    be included in the downloadable assessment report.
    """
)

project_name = st.text_input(
    "Proposed MMFL initiative",
    placeholder="Give the project a title.",
)

use_case = st.text_area(
    "MMFL use case",
    placeholder="Describe the specific MMFL use case to be implemented.",
)

outcome_variable = st.text_area(
    "Common learning objective",
    placeholder="Describe the outcome the participating sites intend to model.",
)

sites = st.text_area(
    "Participating sites",
    placeholder=("Enter one site per line. (A site is a participating healthcare "
    "organization or data-contributing entity.)"),
)

target_population = st.text_area(
    "Target population",
    placeholder="Describe the patient population to be modeled and any relevant subgroups.",
)

required_modalities = st.multiselect(
    "Required data modalities",
    options=[
        "Structured EHR data",
        "Unstructured EHR data (e.g., clinical notes)",
        "Medical imaging (e.g., X-ray, CT, MRI)",
        "Lab test results",
        "Genomic data",
        "Wearable device data",
        "Patient-generated data",
        "Other",
    ],
)

# configuration
CATEGORY_COLORS = {
    "Data Characteristics": "#258395",
    "Integration Readiness": "#C56A32",
    "Organizational Readiness": "#725c9e",
}

ASSESSMENT_ITEMS = [
    {
        "category": "Data Characteristics",
        "pillar": "Modality Availability",
        "question": ("How consistently have participating sites documented and maintained sufficient coverage "
            "of every data type (modality) required for the proposed MMFL use case?"),
        "anchors": {
            "N/E": (
                "Insufficient evidence: Required modalities are unclear, or "
                "site-level availability, counts, coverage, or missingness are unavailable."
            ),
            "0": (
                "Not demonstrated: Multiple required modalities are unavailable "
                "or do not satisfy predefined coverage requirements."
            ),
            "1": (
                "Partially demonstrated: Required modalities are mostly available, "
                "but meaningful differences in coverage or missingness remain."
            ),
            "2": (
                "Demonstrated: All required modalities are available, and their "
                "counts, coverage, and missingness satisfy documented use-case requirements."
            ),
        },
        "evidence": [
            "Specification describing required modalities.",
            "Site-level data inventories.",
            "Patient or observation counts by modality and site.",
            "Modality coverage and missingness reports.",
        ],
    },
    {
        "category": "Data Characteristics",
        "pillar": "Data Quality and Completeness",
        "question": (
            "To what degree has the quality and completeness of each required modality "
            "been measured using comparable expectations across participating sites?"
        ),
        "anchors": {
            "N/E": (
                "Insufficient evidence: Quality requirements are undefined or "
                "site- and modality-level quality results are unavailable."
            ),
            "0": (
                "Not demonstrated: Common quality expectations are absent, or "
                "material quality problems make the data unsuitable."
            ),
            "1": (
                "Partially demonstrated: Quality expectations have been partially  "
                "applied, but some modalities, sites, or material issues remain unassessed."
            ),
            "2": (
                "Demonstrated: Common quality expectations have been applied across "
                "all required sites and modalities, with material issues documented and managed."
            ),
        },
        "evidence": [
            "Specification outlining data-quality requirements and acceptance thresholds.",
            "Accuracy or validity reports by modality and site.",
            "Missingness and completeness reports by modality and site.",
            "Data-refresh schedules and timeliness reports.",
            "Label or annotation quality documentation.",
        ],
    },
    {
        "category": "Data Characteristics",
        "pillar": "Population Representativeness",
        "question": (
            "To what extent do each site's eligible patient population and relevant subgroups adequately "
            "represent the target population for the proposed MMFL use case?"
        ),
        "anchors": {
            "N/E": (
                "Insufficient evidence: The target population is undefined or "
                "site-level population, subgroup, or modality-coverage data are unavailable."
            ),
            "0": (
                "Not demonstrated: Material underrepresentation or unequal modality "
                "coverage exists and has not been addressed."
            ),
            "1": (
                "Partially demonstrated: Representation has been partially assessed, "
                "but site differences or subgroup coverage gaps remain."
            ),
            "2": (
                "Demonstrated: The target population and relevant subgroups have been "
                "compared across sites, and material representation gaps are addressed."
            ),
        },
        "evidence": [
            "Specification defining the target population, with documented cohort inclusion and exclusion criteria.",
            "Demographic and clinical summaries by site.",
            "Patient counts for relevant subgroups by site.",
            "Modality coverage and missingness reports by subgroup.",
            "Cross-site population comparison reports.",
        ],
    },
    {
        "category": "Integration Readiness",
        "pillar": "Standardization and Interoperability",
        "question": (
            "How consistently can every site produce the required data elements, codes, units, cohorts, "
            "features, and outcome labels with the same meaning and format?"
        ),
        "anchors": {
            "N/E": (
                "Insufficient evidence: Schemas, codes, units, features, cohorts, "
                "or labels are not sufficiently documented."
            ),
            "0": (
                "Not demonstrated: Material incompatibilities exist without shared "
                "definitions or workable mappings."
            ),
            "1": (
                "Partially demonstrated: Definitions or mappings exist but are "
                "incomplete, inconsistently applied, unverified, or not version controlled."
            ),
            "2": (
                "Demonstrated: Shared definitions or verified mappings are documented, "
                "consistently applied, and version controlled across sites."
            ),
        },
        "evidence": [
            "Specification outlining common feature and outcome-label definitions.",
            "Documentation of allowable coding systems and measurement units.",
            "Site-level data dictionaries, schemas, and feature lists.",
            "Mapping between site-specific and common definitions, codes, or units.",
            "Version-controlled definitions, mappings, and change logs.",
        ],
    },
    {
        "category": "Integration Readiness",
        "pillar": "Cross-Modal Alignment",
        "question": (
            "How consistently can participating sites link the required modalities "
            "for the same patient, encounter, or clinical episode?"
        ),
        "anchors": {
            "N/E": (
                "Insufficient evidence: Linkage methods, event definitions, temporal "
                "rules, or linkage-coverage measures are unavailable."
            ),
            "0": (
                "Not demonstrated: Required modalities cannot be reliably linked, "
                "or sites use materially incompatible alignment rules."
            ),
            "1": (
                "Partially demonstrated: Modalities can be linked, but matching, "
                "event, temporal, coverage, or quality differences remain."
            ),
            "2": (
                "Demonstrated: Required modalities can be linked across sites using "
                "compatible documented rules that meet use-case requirements."
            ),
        },
        "evidence": [
            "Specification detailing patient and encounter linkage methods, event definitions, and temporal rules.",
            "Documented definitions of clinical episodes or events.",
            "Temporal alignment rules for each modality.",
            "Coverage rates for linked modalities by site.",
            "Linkage-quality reports and error-rate estimates.",
        ],
    },
    {
        "category": "Organizational Readiness",
        "pillar": "Privacy and Security by Modality",
        "question": (
            "To what extent can each site use the required data and share the model "
            "updates, metrics, or metadata needed while maintaining privacy and security in "
            "accordance with applicable laws, regulations, and policies?"
        ),
        "anchors": {
            "N/E": (
                "Insufficient evidence: Applicable requirements, risks, or controls "
                "have not been sufficiently documented."
            ),
            "0": (
                "Not demonstrated: Unresolved requirements, unaddressed risks, or "
                "missing controls prevent appropriate federated participation."
            ),
            "1": (
                "Partially demonstrated: Requirements and risks have been partially "
                "assessed, but modality-specific, combined-data, or model-update gaps remain."
            ),
            "2": (
                "Demonstrated: Site requirements and modality-specific and combined-data "
                "risks have been assessed, with compatible controls documented."
            ),
        },
        "evidence": [
            "Cross-site privacy and security requirements matrix.",
            "Modality-specific privacy and security risk assessments.",
            "Combined-modality re-identification risk assessment.",
            "Access-control and authorization documentation.",
            "Encryption and de-identification procedures and reports.",
            "Federated model-update privacy and security controls.",
        ],
    },
    {
        "category": "Organizational Readiness",
        "pillar": "Provenance and Governance",
        "question": (
            "How consistently are data origins, transformations, permitted uses, "
            "and governance responsibilities documented across participating sites?"
        ),
        "anchors": {
            "N/E": (
                "Insufficient evidence: Information about sources, transformations, "
                "permitted uses, ownership, or responsibilities is unavailable."
            ),
            "0": (
                "Not demonstrated: Material conflicts or gaps exist in provenance, "
                "permissions, agreements, ownership, or governance responsibilities."
            ),
            "1": (
                "Partially demonstrated: Documentation and governance arrangements "
                "exist for some sites or data components but remain incomplete or inconsistent."
            ),
            "2": (
                "Demonstrated: Sources, collection methods, lineage, transformations, "
                "permitted uses, ownership, agreements, and responsibilities are documented."
            ),
        },
        "evidence": [
            "Data source and collection method inventories.",
            "Data lineage and transformation records.",
            "Data use agreements and permitted-use documentation.",
            "Ownership and stewardship assignments.",
            "Governance charters, policies, and procedures.",
            "Audit logs and change-control documentation.",
        ],
    },
]

# display questions
st.header("Readiness Screening")

st.caption(
    """
    Select the level best supported by current evidence. When conditions differ
    across sites or essential indicators, select the lowest applicable level.
    """
)

# matches with the anchors in ASSESSMENT_ITEMS
response_options = {
    "Select a response": None,
    "N/E — Insufficient evidence": None,
    "0 — Not demonstrated": 0,
    "1 — Partially demonstrated": 1,
    "2 — Demonstrated": 2,
}

responses = []

# loop through the configured assessment items and display them in an expandable format
for index, item in enumerate(ASSESSMENT_ITEMS):
    with st.expander(
        f"{index + 1}. {item['pillar']} — {item['category']}",
        expanded=index == 0,
    ):

        # add the colors from above
        category_color = CATEGORY_COLORS[item["category"]]

        st.markdown(
            f"""
            <span style="
                display: inline-block;
                background-color: {category_color};
                color: white;
                padding: 0.25rem 0.65rem;
                border-radius: 999px;
                font-size: 0.8rem;
                font-weight: 600;
                margin-bottom: 0.75rem;
            ">
                {item["category"]}
            </span>
            """,
            unsafe_allow_html=True,
        )

        st.subheader(item["question"])

        st.markdown("**Response anchors**")

        for level, description in item["anchors"].items():
            st.write(f"**{level}:** {description}")

        selected_label = st.radio(
            "Assessment result",
            options=list(response_options.keys()),
            key=f"response_{index}",
        )

        evidence_notes = st.text_area(
            "Evidence reviewed and rationale",
            placeholder=(
                "Identify the evidence reviewed and explain why the selected "
                "response level applies."
            ),
            key=f"evidence_{index}",
        )

        st.markdown("**Examples of relevant evidence:**")

        for evidence_item in item["evidence"]:
            st.markdown(f"- {evidence_item}")

        responses.append(
            {
                "category": item["category"],
                "pillar": item["pillar"],
                "response": selected_label,
                "score": response_options[selected_label],
                "evidence_notes": evidence_notes,
            }
        )

# scoring model
st.header("Assessment Results")

answered_items = [
    response for response in responses
    if response["response"] != "Select a response"
]

scored_items = [
    response for response in answered_items
    if response["response"] != "N/E — Insufficient evidence"
]

# identify pillars with insufficient evidence, which may indicate gaps in assessment
evidence_gaps = [
    response["pillar"]
    for response in answered_items
    if response["response"] == "N/E — Insufficient evidence"
]

# identify pillars with a score of 0, which may indicate critical gaps
critical_gaps = [
    response["pillar"]
    for response in scored_items
    if response["score"] == 0
]

# check if all assessment items have been answered
if len(answered_items) < len(ASSESSMENT_ITEMS):
    st.warning(
        f"Complete all seven pillars to generate a readiness classification. "
        f"{len(answered_items)} of {len(ASSESSMENT_ITEMS)} have been completed."
    )
else:
    total_score = sum(
        response["score"] or 0
        for response in answered_items
    )

    maximum_score = len(ASSESSMENT_ITEMS) * 2
    readiness_percentage = total_score / maximum_score * 100

    # set thresholds for readiness classification based on percentage score
    if readiness_percentage < 40:
        readiness_level = "Substantial preparation needed"
    elif readiness_percentage < 70:
        readiness_level = "Partial cross-site compatibility"
    else:
        readiness_level = "Preliminary cross-site compatibility"

    col1, col2 = st.columns(2)

    col1.metric("Total score", f"{total_score}/{maximum_score}")
    col2.metric("Readiness percentage", f"{readiness_percentage:.1f}%")

    st.metric("Prototype classification", readiness_level)

    # warning and error messages for evidence gaps and critical gaps
    if evidence_gaps:
        st.warning(
            "Insufficient evidence was reported for: "
            + ", ".join(evidence_gaps)
        )

    if critical_gaps:
        st.error(
            "Potential critical gaps were identified for: "
            + ", ".join(critical_gaps)
        )

    # Prepare downloadable assessment results
    results_rows = []

    for response in responses:
        if response["response"] == "N/E — Insufficient evidence":
            gap_type = "Evidence gap"
        elif response["score"] == 0:
            gap_type = "Critical gap"
        else:
            gap_type = ""

        results_rows.append(
            {
                "Project Name": project_name,
                "MMFL Use Case": use_case,
                "Target Outcome": outcome_variable,
                "Participating Sites": sites.replace("\n", "; "),
                "Target Population": target_population,
                "Required Modalities": "; ".join(required_modalities),
                "Category": response["category"],
                "Pillar": response["pillar"],
                "Selected Response": response["response"],
                "Pillar Score": response["score"],
                "Evidence and Rationale": response["evidence_notes"],
                "Gap Type": gap_type,
                "Total Score": total_score,
                "Maximum Score": maximum_score,
                "Readiness Percentage": round(readiness_percentage, 1),
                "Compatibility Classification": readiness_level,
            }
        )

    results_df = pd.DataFrame(results_rows)

    pdf_data = generate_assessment_pdf(
        project_name=project_name,
        use_case=use_case,
        outcome_variable=outcome_variable,
        sites=sites,
        target_population=target_population,
        required_modalities=required_modalities,
        responses=responses,
        total_score=total_score,
        maximum_score=maximum_score,
        readiness_percentage=readiness_percentage,
        readiness_level=readiness_level,
        critical_gaps=critical_gaps,
        evidence_gaps=evidence_gaps,
    )

    # display the results and make them available for download
    st.subheader("Download Results")

    st.dataframe(
        results_df[
            [
                "Category",
                "Pillar",
                "Selected Response",
                "Pillar Score",
                "Gap Type",
                "Evidence and Rationale",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        label="Download assessment report as PDF",
        data=pdf_data,
        file_name="mhdrm_assessment_report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

    st.caption(
        """
        The thresholds are illustrative prototype thresholds and have not been
        empirically validated. An overall score does not override evidence gaps
        or pillar-level critical gaps.
        """
    )