from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .models import ProposalSubmission
from .storage import OUTPUT_DIR, ensure_directories


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleCustom",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=colors.HexColor("#102A43"),
            leading=22,
            spaceAfter=14,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleCustom",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            textColor=colors.HexColor("#52606D"),
            leading=12,
            spaceAfter=10,
        ),
        "section": ParagraphStyle(
            "SectionCustom",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            textColor=colors.HexColor("#0B7285"),
            spaceBefore=8,
            spaceAfter=6,
        ),
        "normal": ParagraphStyle(
            "NormalCustom",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
        ),
    }


def _table(rows: list[tuple[str, str]]) -> Table:
    styles = _styles()
    data = [
        [
            Paragraph(f"<b>{escape(label)}</b>", styles["normal"]),
            Paragraph(escape(str(value)).replace("\n", "<br/>") if value else "Nao informado", styles["normal"]),
        ]
        for label, value in rows
    ]
    table = Table(data, colWidths=[5.2 * cm, 11.2 * cm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#D9E2EC")),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#D9E2EC")),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F0F4F8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def generate_pdf(submission: ProposalSubmission) -> Path:
    ensure_directories()
    styles = _styles()
    output_path = OUTPUT_DIR / f"{submission.protocol}.pdf"
    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        title="Pontual Propostas de Locacao",
    )

    property_data = submission.property_data
    applicant = submission.applicant_data
    delivery = submission.delivery_data
    doc_rows = [
        (doc.label, f"{doc.filename} ({doc.size_bytes / 1024:.1f} KB)")
        for doc in submission.documents
    ] or [("Documentos", "Nenhum arquivo anexado")]

    story = [
        Paragraph("Pontual Propostas de Locacao", styles["title"]),
        Paragraph(
            f"Protocolo: {submission.protocol}<br/>Gerado em: {submission.created_at.strftime('%d/%m/%Y %H:%M')}",
            styles["subtitle"],
        ),
        Paragraph("1. Dados do Imovel Pretendido", styles["section"]),
        _table(
            [
                ("Tipo de locacao", property_data.lease_type),
                ("Endereco do imovel", property_data.address),
                ("Valor do aluguel proposto", property_data.proposed_rent),
                ("Numero de futuros moradores", str(property_data.residents_count)),
                ("Observacoes sobre taxas", property_data.fees_notes),
            ]
        ),
        Spacer(1, 10),
        Paragraph("2. Dados do Proponente", styles["section"]),
        _table(
            [
                ("Nome completo", applicant.full_name),
                ("Data de nascimento", applicant.birth_date.strftime("%d/%m/%Y")),
                ("Profissao", applicant.profession),
                ("RG / Orgao emissor / Expedicao", applicant.rg_info),
                ("CPF", applicant.cpf),
                ("Telefone / WhatsApp", applicant.phone),
                ("E-mail", applicant.email),
                ("Estado civil", applicant.marital_status),
                ("Sexo", applicant.sex),
                ("Nacionalidade", applicant.nationality),
                ("Nome do pai", applicant.father_name),
                ("Nome da mae", applicant.mother_name),
                ("Nome do conjuge", applicant.spouse_name),
                ("CPF do conjuge", applicant.spouse_cpf),
                ("Carteira de trabalho / Serie", applicant.work_card),
            ]
        ),
        Spacer(1, 10),
        Paragraph("3. Endereco e Historico Residencial", styles["section"]),
        _table(
            [
                ("Endereco atual", applicant.current_address),
                ("Endereco anterior", applicant.previous_address),
                ("Tempo no endereco atual", applicant.years_current_address),
                ("Tempo no endereco anterior", applicant.years_previous_address),
                ("Situacao do imovel atual", applicant.residence_status),
                ("Proprietario ou administradora", applicant.landlord_contact),
            ]
        ),
        Spacer(1, 10),
        Paragraph("4. Dados Profissionais e Renda", styles["section"]),
        _table(
            [
                ("Cargo / Profissao", applicant.profession),
                ("Tipo da fonte de renda", applicant.occupation_type),
                ("Empresa ou atividade", applicant.company_name),
                ("Endereco profissional", applicant.company_address),
                ("Telefone / Ramal", applicant.company_phone),
                ("Departamento", applicant.department),
                ("Tempo na empresa", applicant.employment_time),
                ("Renda mensal", applicant.monthly_income),
                ("Renda extra mensal", applicant.extra_income),
                ("Participacao societaria", applicant.company_participation),
                ("Inscricao estadual", applicant.state_registration),
                ("Outros rendimentos", applicant.other_income),
            ]
        ),
        Spacer(1, 10),
        Paragraph("5. Moradores, Patrimonio e Referencias", styles["section"]),
        _table(
            [
                ("Demais moradores", applicant.other_residents),
                ("Animais de estimacao", applicant.pets),
                ("Imoveis proprios", applicant.properties),
                ("Veiculos", applicant.vehicles),
                ("Referencias pessoais", applicant.references),
            ]
        ),
    ]

    if submission.guarantor_data:
        guarantor = submission.guarantor_data
        story.extend(
            [
                Spacer(1, 10),
                Paragraph("6. Dados do Fiador", styles["section"]),
                _table(
                    [
                        ("Nome completo", guarantor.full_name),
                        ("Data de nascimento", guarantor.birth_date.strftime("%d/%m/%Y")),
                        ("RG / Orgao emissor", guarantor.rg_info),
                        ("CPF", guarantor.cpf),
                        ("Sexo", guarantor.sex),
                        ("Estado civil", guarantor.marital_status),
                        ("Nacionalidade", guarantor.nationality),
                        ("Nome do pai", guarantor.father_name),
                        ("Nome da mae", guarantor.mother_name),
                        ("Carteira de trabalho / Serie", guarantor.work_card),
                        ("Dados do conjuge", guarantor.spouse_details),
                        ("Endereco atual", guarantor.current_address),
                        ("Situacao do imovel atual", guarantor.residence_status),
                        ("Empresa e dados profissionais", guarantor.company_details),
                        ("Cargo / Profissao", guarantor.profession),
                        ("Tempo na empresa", guarantor.employment_time),
                        ("Renda mensal", guarantor.monthly_income),
                        ("Outros rendimentos", guarantor.other_income),
                        ("Tipo da fonte de renda", guarantor.occupation_type),
                        ("Imoveis", guarantor.properties),
                        ("Veiculos", guarantor.vehicles),
                        ("Referencias pessoais", guarantor.references),
                    ]
                ),
            ]
        )

    story.extend(
        [
            Spacer(1, 10),
            Paragraph("7. Documentos Anexados", styles["section"]),
            _table(doc_rows),
            Spacer(1, 10),
            Paragraph("8. Canal de Retorno", styles["section"]),
            _table(
                [
                    ("Canal preferencial", delivery.preferred_channel),
                    ("Contato informado", delivery.destination),
                ]
            ),
            Spacer(1, 14),
            Paragraph(
                "Declaracao: declaro serem verdadeiros os dados informados nesta proposta e autorizo a analise cadastral. "
                "O locador ou administradora podera solicitar documentos complementares e decidir pela aceitacao da proposta.",
                styles["normal"],
            ),
        ]
    )

    document.build(story)
    return output_path
