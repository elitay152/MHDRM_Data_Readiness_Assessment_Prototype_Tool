from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def safe_text(value):
    """Prepare user-provided text for a ReportLab paragraph."""
    if value is None or str(value).strip() == "":
        return "Not provided"

    return escape(str(value)).replace("\n", "<br/>")


def generate_assessment_pdf(
    project_name,
    use_case,
    outcome_variable,
    sites,
    target_population,
    required_modalities,
    responses,
    total_score,
    maximum_score,
    readiness_percentage,
    readiness_level,
    critical_gaps,
    evidence_gaps,
):
    """Generate a PDF report for the MHDRM Cross-Site Readiness Assessment."""
    pdf_buffer = BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
        title="MHDRM Cross-Site Readiness Assessment",
    )

    styles = getSampleStyleSheet()

    # format the title, subtitle, headings, and body text
    title_style = ParagraphStyle(
        name="AssessmentTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#123B5D"),
        alignment=TA_CENTER,
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        name="AssessmentSubtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#176B78"),
        alignment=TA_CENTER,
        spaceAfter=14,
    )

    heading_style = ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#176B78"),
        spaceBefore=6,
        spaceAfter=7,
    )

    body_style = ParagraphStyle(
        name="AssessmentBody",
        parent=styles["BodyText"],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#303744"),
    )

    label_style = ParagraphStyle(
        name="ContextLabel",
        parent=body_style,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#123B5D"),
    )

    small_style = ParagraphStyle(
        name="SmallText",
        parent=body_style,
        fontSize=7.5,
        leading=9.5,
    )

    classification_style = ParagraphStyle(
        name="ClassificationText",
        parent=body_style,
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#123B5D"),
    )

    # Build the PDF content
    story = []

    story.append(
        Paragraph(
            "MHDRM Cross-Site Readiness Assessment",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Prototype screening report for multimodal federated learning",
            subtitle_style,
        )
    )

    # Include the provided assessment context
    story.append(Paragraph("Assessment Context", heading_style))

    modalities_text = (
        ", ".join(required_modalities)
        if required_modalities
        else "Not provided"
    )

    context_data = [
        [
            Paragraph("Project name", label_style),
            Paragraph(safe_text(project_name), body_style),
        ],
        [
            Paragraph("MMFL use case", label_style),
            Paragraph(safe_text(use_case), body_style),
        ],
        [
            Paragraph("Target outcome or label", label_style),
            Paragraph(safe_text(outcome_variable), body_style),
        ],
        [
            Paragraph("Participating sites", label_style),
            Paragraph(safe_text(sites), body_style),
        ],
        [
            Paragraph("Target population", label_style),
            Paragraph(safe_text(target_population), body_style),
        ],
        [
            Paragraph("Required modalities", label_style),
            Paragraph(safe_text(modalities_text), body_style),
        ],
    ]

    context_table = Table(
        context_data,
        colWidths=[1.55 * inch, 5.25 * inch],
        hAlign="LEFT",
    )

    context_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E5F1F3")),
                ("BACKGROUND", (1, 0), (1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#ABC9D1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C9DCE3")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    story.append(context_table)
    story.append(Spacer(1, 12))

    # Add the results from the assessment
    story.append(Paragraph("Assessment Summary", heading_style))

    summary_data = [
        [
            Paragraph("Total score", label_style),
            Paragraph("Readiness", label_style),
            Paragraph("Classification", label_style),
        ],
        [
            Paragraph(f"{total_score}/{maximum_score}", classification_style),
            Paragraph(
                f"{readiness_percentage:.1f}%",
                classification_style,
            ),
            Paragraph(safe_text(readiness_level), classification_style),
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[1.25 * inch, 1.35 * inch, 4.2 * inch],
        hAlign="LEFT",
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#176B78"),
                ),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#F5F8FA")),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#ABC9D1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C9DCE3")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(summary_table)
    story.append(Spacer(1, 12))

    # Add the detailed results for each pillar
    story.append(Paragraph("Pillar Results", heading_style))

    results_data = [
        [
            Paragraph("Category", label_style),
            Paragraph("MHDRM pillar", label_style),
            Paragraph("Response", label_style),
            Paragraph("Score", label_style),
            Paragraph("Flag", label_style),
        ]
    ]

    for response in responses:
        if response["response"] == "N/E — Insufficient evidence":
            flag = "Evidence gap"
            score_display = "N/E"
        elif response["score"] == 0:
            flag = "Critical gap"
            score_display = "0"
        else:
            flag = ""
            score_display = str(response["score"])

        results_data.append(
            [
                Paragraph(safe_text(response["category"]), small_style),
                Paragraph(safe_text(response["pillar"]), small_style),
                Paragraph(safe_text(response["response"]), small_style),
                Paragraph(score_display, small_style),
                Paragraph(flag, small_style),
            ]
        )

    results_table = Table(
        results_data,
        colWidths=[
            1.35 * inch,
            1.65 * inch,
            2.3 * inch,
            0.5 * inch,
            1.0 * inch,
        ],
        repeatRows=1,
        hAlign="LEFT",
    )

    results_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#123B5D"),
                ),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                    colors.white,
                    colors.HexColor("#F5F8FA"),
                ]),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#ABC9D1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C9DCE3")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (3, 1), (3, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    # Highlight flagged rows
    for row_number, response in enumerate(responses, start=1):
        if response["response"] == "N/E — Insufficient evidence":
            results_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (4, row_number),
                            (4, row_number),
                            colors.HexColor("#FFF2CC"),
                        )
                    ]
                )
            )
        elif response["score"] == 0:
            results_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (4, row_number),
                            (4, row_number),
                            colors.HexColor("#F4CCCC"),
                        )
                    ]
                )
            )

    story.append(results_table)
    story.append(Spacer(1, 12))

    # Gap summary
    if critical_gaps:
        story.append(
            Paragraph(
                "<b>Potential critical gaps:</b> "
                + safe_text(", ".join(critical_gaps)),
                body_style,
            )
        )
        story.append(Spacer(1, 4))

    if evidence_gaps:
        story.append(
            Paragraph(
                "<b>Evidence gaps:</b> "
                + safe_text(", ".join(evidence_gaps)),
                body_style,
            )
        )
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            "<b>Prototype limitation:</b> This report provides a preliminary "
            "preimplementation screening of cross-site data compatibility. "
            "The scores and thresholds have not been empirically validated and "
            "do not certify that an MMFL initiative will be successful.",
            small_style,
        )
    )

    document.build(story)

    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()