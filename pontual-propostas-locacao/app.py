from __future__ import annotations

from datetime import date
from urllib.parse import quote

import streamlit as st

from src.models import ApplicantData, DeliveryData, GuarantorData, PropertyData, ProposalSubmission
from src.pdf_generator import generate_pdf
from src.storage import (
    create_submission_package,
    ensure_directories,
    generate_protocol,
    save_submission,
    save_uploaded_file,
)
from src.validators import required, validate_birth_date, validate_cpf, validate_email, validate_phone


st.set_page_config(
    page_title="Pontual Propostas de Locacao",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)


CUSTOM_CSS = """
<style>
    .main .block-container { padding-top: 1.5rem; max-width: 1180px; }
    .hero {
        border: 1px solid #d9e2ec;
        border-radius: 8px;
        padding: 22px 24px;
        background: linear-gradient(135deg, #f8fafc 0%, #eef6f7 100%);
        margin-bottom: 18px;
    }
    .hero h1 { margin: 0 0 6px 0; color: #102a43; font-size: 2rem; }
    .hero p { margin: 0; color: #52606d; font-size: 1rem; }
    .metric-card {
        border: 1px solid #d9e2ec;
        border-radius: 8px;
        padding: 14px;
        background: #ffffff;
    }
    .small-muted { color: #627d98; font-size: .9rem; }
    div[data-testid="stForm"] {
        border: 1px solid #d9e2ec;
        border-radius: 8px;
        padding: 18px;
    }
</style>
"""


def init_state() -> None:
    ensure_directories()
    st.session_state.setdefault("last_pdf_path", None)
    st.session_state.setdefault("last_package_path", None)
    st.session_state.setdefault("last_protocol", None)
    st.session_state.setdefault("last_channel", None)
    st.session_state.setdefault("last_destination", None)


def render_header() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(
        """
        <div class="hero">
            <h1>Pontual Propostas de Locacao</h1>
            <p>Propostas residenciais, comerciais e de temporada com analise cadastral, fiador e documentos organizados.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    with st.sidebar:
        st.subheader("Pontual Propostas")
        st.caption("Use esta area para demonstrar valor ao cliente.")
        st.markdown(
            """
            - Formulario digital padronizado
            - Validacao de dados essenciais
            - Upload organizado de documentos
            - Cadastro opcional de fiador
            - Protocolo automatico
            - PDF e pacote ZIP para envio
            - Historico local em JSON
            """
        )
        st.divider()
        st.info("Este MVP pode evoluir para login, banco de dados, assinatura digital e dashboard administrativo.")


def validate_form(fields: dict[str, object], uploaded_files: dict[str, object]) -> list[str]:
    errors: list[str] = []

    required_fields = {
        "Tipo de locação": fields["lease_type"],
        "Endereço do imóvel": fields["property_address"],
        "Valor do aluguel": fields["proposed_rent"],
        "Nome completo": fields["full_name"],
        "Profissão": fields["profession"],
        "RG": fields["rg_info"],
        "CPF": fields["cpf"],
        "Telefone": fields["phone"],
        "E-mail": fields["email"],
        "Participação societária": fields["company_participation"],
        "Endereço atual": fields["current_address"],
        "Empresa ou atividade profissional": fields["company_name"],
        "Renda mensal": fields["monthly_income"],
        "Canal de retorno": fields["delivery_channel"],
        "Contato para retorno": fields["delivery_destination"],
    }
    for label, value in required_fields.items():
        if not required(str(value)):
            errors.append(f"Preencha o campo obrigatório: {label}.")

    birth_date = fields["birth_date"]
    if not isinstance(birth_date, date) or not validate_birth_date(birth_date):
        errors.append("Informe uma data de nascimento valida.")

    if not validate_cpf(str(fields["cpf"])):
        errors.append("CPF invalido. Confira os numeros informados.")

    if not validate_phone(str(fields["phone"])):
        errors.append("Telefone/WhatsApp invalido. Use DDD e numero.")

    if not validate_email(str(fields["email"])):
        errors.append("E-mail invalido.")

    if int(fields["residents_count"]) < 1:
        errors.append("O numero de moradores deve ser pelo menos 1.")

    if fields["delivery_channel"] == "E-mail" and not validate_email(str(fields["delivery_destination"])):
        errors.append("Informe um e-mail valido para retorno.")
    if fields["delivery_channel"] == "WhatsApp" and not validate_phone(str(fields["delivery_destination"])):
        errors.append("Informe um WhatsApp valido para retorno.")

    if fields["has_guarantor"]:
        guarantor_required = {
            "Nome do fiador": fields["guarantor_full_name"],
            "CPF do fiador": fields["guarantor_cpf"],
            "RG do fiador": fields["guarantor_rg"],
            "Endereço do fiador": fields["guarantor_address"],
            "Profissão do fiador": fields["guarantor_profession"],
            "Renda mensal do fiador": fields["guarantor_income"],
        }
        for label, value in guarantor_required.items():
            if not required(str(value)):
                errors.append(f"Preencha o campo obrigatorio: {label}.")
        if fields["guarantor_cpf"] and not validate_cpf(str(fields["guarantor_cpf"])):
            errors.append("CPF do fiador invalido.")

    for label, file in uploaded_files.items():
        if file is None:
            errors.append(f"Anexe o documento obrigatorio: {label}.")
        elif file.size > 10 * 1024 * 1024:
            errors.append(f"O arquivo '{file.name}' excede 10 MB.")

    return errors


def render_form() -> None:
    guarantee_mode = st.radio(
        "Garantia da proposta",
        ["Sem fiador", "Com fiador"],
        horizontal=True,
        help="Selecione 'Com fiador' para abrir o cadastro e os documentos do fiador.",
    )
    has_guarantor = guarantee_mode == "Com fiador"

    with st.form("proposal_form", clear_on_submit=False):
        st.subheader("1. Tipo e dados do imovel pretendido")
        lease_type = st.radio(
            "Tipo de locação *",
            ["Residencial", "Comercial", "Temporada"],
            horizontal=True,
        )
        col1, col2 = st.columns([2, 1])
        with col1:
            property_address = st.text_input("Endereço do imóvel *")
        with col2:
            proposed_rent = st.text_input("Valor do aluguel com encargos *", placeholder="R$ 0,00")
        residents_count = st.number_input("Número de futuros moradores *", min_value=1, max_value=20, value=1)
        fees_notes = st.text_area("Observações sobre condomínio, IPTU ou demais taxas", height=80)

        st.subheader("2. Dados do proponente")
        with st.expander("Dados pessoais", expanded=True):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                full_name = st.text_input("Nome completo *")
            with col2:
                birth_date = st.date_input(
                    "Data de nascimento *",
                    value=date(1990, 1, 1),
                    min_value=date(1916, 1, 1),
                    max_value=date.today(),
                    format="DD/MM/YYYY",
                )
            with col3:
                nationality = st.text_input("Nacionalidade", value="Brasileira")

            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                rg_info = st.text_input("RG / Órgão emissor / Data da expedição *")
            with col2:
                cpf = st.text_input("CPF *", placeholder="000.000.000-00")
            with col3:
                sex = st.selectbox("Sexo", ["Não informado", "Masculino", "Feminino", "Outro"])

            col1, col2 = st.columns(2)
            with col1:
                phone = st.text_input("Telefone / WhatsApp *", placeholder="(21) 99999-9999")
            with col2:
                email = st.text_input("E-mail *", placeholder="nome@email.com")

            col1, col2 = st.columns(2)
            with col1:
                marital_status = st.selectbox(
                    "Estado civil *",
                    ["Solteiro", "Casado", "Viuvo", "Divorciado", "Separado judicialmente", "Outros"],
                )
            with col2:
                work_card = st.text_input("Carteira de trabalho / Série")

            col1, col2 = st.columns(2)
            with col1:
                father_name = st.text_input("Nome do pai")
            with col2:
                mother_name = st.text_input("Nome da mãe")

            col1, col2 = st.columns(2)
            with col1:
                spouse_name = st.text_input("Nome do cônjuge")
            with col2:
                spouse_cpf = st.text_input("CPF do cônjuge")

        with st.expander("Endereço e histórico residencial", expanded=True):
            current_address = st.text_area(
                "Endereço atual completo *",
                placeholder="Logradouro, número, complemento, bairro, cidade, UF e CEP",
                height=80,
            )
            previous_address = st.text_area("Endereço da residência anterior", height=70)
            col1, col2, col3 = st.columns(3)
            with col1:
                years_current_address = st.text_input("Tempo no endereço atual")
            with col2:
                years_previous_address = st.text_input("Tempo no endereço anterior")
            with col3:
                residence_status = st.selectbox("Situação do imóvel atual", ["Próprio", "Alugado", "Outros"])
            landlord_contact = st.text_area(
                "Se alugado: nome, telefone e endereço do proprietário ou administradora",
                height=70,
            )

        with st.expander("Dados profissionais e renda", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                profession = st.text_input("Cargo / Profissão *")
            with col2:
                occupation_type = st.selectbox(
                    "Tipo da principal fonte de renda",
                    ["Assalariado", "Autônomo", "Profissional liberal", "Militar", "Empresário", "Outros"],
                )
            company_name = st.text_input("Empresa ou atividade profissional *")
            company_address = st.text_area("Endereço profissional", height=70)
            col1, col2, col3 = st.columns(3)
            with col1:
                company_phone = st.text_input("Telefone / Ramal profissional")
            with col2:
                department = st.text_input("Departamento")
            with col3:
                employment_time = st.text_input("Tempo na empresa/atividade")
            col1, col2 = st.columns(2)
            with col1:
                monthly_income = st.text_input("Renda mensal *", placeholder="R$ 0,00")
            with col2:
                extra_income = st.text_input("Renda extra mensal", placeholder="R$ 0,00")
            company_participation = st.text_input(
                "CNPJ, se sócio ou diretor *",
                placeholder="Não possui / 00.000.000/0001-00",
            )
            state_registration = st.text_input("Inscrição estadual")
            other_income = st.text_area("Outros rendimentos e respectivas fontes", height=70)

        with st.expander("Moradores, patrimônio e referências"):
            other_residents = st.text_area("Nome e idade dos demais moradores", height=80)
            pets = st.text_area("Possui animais de estimação? Informe tipo e porte", height=70)
            properties = st.text_area(
                "Imóveis próprios: endereço e informação sobre escritura definitiva",
                height=80,
            )
            vehicles = st.text_area(
                "Veículos: tipo, marca/modelo, ano, Renavam e placa",
                height=80,
            )
            references = st.text_area(
                "Referências pessoais: nome, telefone e ramal (até 3 pessoas)",
                height=90,
            )

        if has_guarantor:
            st.subheader("3. Dados do fiador")
            with st.expander("Dados pessoais e endereço do fiador", expanded=True):
                col1, col2 = st.columns([2, 1])
                with col1:
                    guarantor_full_name = st.text_input("Nome completo do fiador *")
                with col2:
                    guarantor_birth_date = st.date_input(
                        "Data de nascimento do fiador *",
                        value=date(1980, 1, 1),
                        min_value=date(1916, 1, 1),
                        max_value=date.today(),
                        format="DD/MM/YYYY",
                    )
                col1, col2, col3 = st.columns(3)
                with col1:
                    guarantor_rg = st.text_input("RG / Órgão emissor do fiador *")
                with col2:
                    guarantor_cpf = st.text_input("CPF do fiador *")
                with col3:
                    guarantor_sex = st.selectbox(
                        "Sexo do fiador",
                        ["Não informado", "Masculino", "Feminino", "Outro"],
                    )
                col1, col2 = st.columns(2)
                with col1:
                    guarantor_marital_status = st.selectbox(
                        "Estado civil do fiador",
                        ["Solteiro", "Casado", "Viuvo", "Divorciado", "Separado judicialmente", "Outros"],
                    )
                with col2:
                    guarantor_nationality = st.text_input("Nacionalidade do fiador", value="Brasileira")
                col1, col2 = st.columns(2)
                with col1:
                    guarantor_father = st.text_input("Nome do pai do fiador")
                with col2:
                    guarantor_mother = st.text_input("Nome da mãe do fiador")
                guarantor_work_card = st.text_input("Carteira de trabalho / Série do fiador")
                guarantor_spouse = st.text_area(
                    "Cônjuge do fiador: nome, CPF, nascimento, empresa, cargo, renda, telefone e endereço comercial",
                    height=90,
                )
                guarantor_address = st.text_area(
                    "Endereço completo do fiador *",
                    placeholder="Logradouro, número, complemento, bairro, cidade, UF, CEP e telefone",
                    height=80,
                )
                guarantor_residence_status = st.selectbox(
                    "Situação do imóvel onde reside o fiador",
                    ["Próprio", "Alugado", "Outros"],
                )

            with st.expander("Profissão, renda e patrimônio do fiador", expanded=True):
                guarantor_company = st.text_area(
                    "Empresa do fiador: razão social, endereço, telefone, CNPJ, IE e departamento",
                    height=90,
                )
                col1, col2, col3 = st.columns(3)
                with col1:
                    guarantor_profession = st.text_input("Cargo / Profissão do fiador *")
                with col2:
                    guarantor_employment_time = st.text_input("Tempo na empresa")
                with col3:
                    guarantor_income = st.text_input("Renda mensal do fiador *")
                guarantor_occupation_type = st.selectbox(
                    "Tipo da principal fonte de renda do fiador",
                    ["Assalariado", "Autônomo", "Profissional liberal", "Militar", "Empresário", "Outros"],
                )
                guarantor_other_income = st.text_area("Outros rendimentos do fiador", height=70)
                guarantor_properties = st.text_area(
                    "Imóveis do fiador: endereços e informação sobre escritura definitiva",
                    height=80,
                )
                guarantor_vehicles = st.text_area(
                    "Veículos do fiador: tipo, marca/modelo, ano, Renavam e placa",
                    height=80,
                )
                guarantor_references = st.text_area(
                    "Referências pessoais do fiador: nome e telefone (até 3 pessoas)",
                    height=80,
                )
        else:
            guarantor_full_name = guarantor_rg = guarantor_cpf = ""
            guarantor_sex = guarantor_marital_status = guarantor_nationality = ""
            guarantor_father = guarantor_mother = guarantor_work_card = guarantor_spouse = ""
            guarantor_address = guarantor_residence_status = guarantor_company = ""
            guarantor_profession = guarantor_employment_time = guarantor_income = ""
            guarantor_occupation_type = guarantor_other_income = ""
            guarantor_properties = guarantor_vehicles = guarantor_references = ""
            guarantor_birth_date = date(1980, 1, 1)

        st.subheader("4. Documentos")
        st.caption("Arquivos aceitos: PDF, PNG, JPG ou JPEG. Tamanho maximo: 10 MB por arquivo.")
        accepted_types = ["pdf", "png", "jpg", "jpeg"]
        identity_file = st.file_uploader("Documento de identidade / CPF do proponente *", type=accepted_types)
        residence_file = st.file_uploader("Comprovante de residência do proponente *", type=accepted_types)
        income_file = st.file_uploader(
            "Comprovante de rendimento ou IRPF do proponente *",
            type=accepted_types,
        )
        property_file = st.file_uploader(
            "IPTU, escritura ou registro de imóvel do proponente (se proprietário)",
            type=accepted_types,
        )
        if has_guarantor:
            guarantor_identity_file = st.file_uploader(
                "Documento de identidade / CPF do fiador *",
                type=accepted_types,
            )
            guarantor_residence_file = st.file_uploader(
                "Comprovante de residência do fiador *",
                type=accepted_types,
            )
            guarantor_income_file = st.file_uploader(
                "Comprovante de renda do fiador *",
                type=accepted_types,
            )
            guarantor_property_file = st.file_uploader(
                "IPTU, escritura ou registro de imóvel do fiador (se proprietário)",
                type=accepted_types,
            )
        else:
            guarantor_identity_file = guarantor_residence_file = guarantor_income_file = None
            guarantor_property_file = None

        st.subheader("5. Retorno da proposta")
        col1, col2 = st.columns(2)
        with col1:
            delivery_channel = st.radio("Canal preferencial para retorno *", ["WhatsApp", "E-mail"], horizontal=True)
        with col2:
            delivery_destination = st.text_input(
                "WhatsApp ou e-mail para retorno *",
                placeholder="(21) 99999-9999 ou contato@email.com",
            )

        accepted_terms = st.checkbox(
            "Declaro que as informações prestadas são verdadeiras e autorizo a análise cadastral."
        )
        submitted = st.form_submit_button("Gerar proposta em PDF", use_container_width=True)

    if not submitted:
        return

    fields = {
        "lease_type": lease_type,
        "property_address": property_address,
        "proposed_rent": proposed_rent,
        "residents_count": residents_count,
        "fees_notes": fees_notes,
        "full_name": full_name,
        "birth_date": birth_date,
        "profession": profession,
        "rg_info": rg_info,
        "cpf": cpf,
        "phone": phone,
        "email": email,
        "marital_status": marital_status,
        "sex": sex,
        "nationality": nationality,
        "father_name": father_name,
        "mother_name": mother_name,
        "spouse_name": spouse_name,
        "spouse_cpf": spouse_cpf,
        "work_card": work_card,
        "company_participation": company_participation,
        "current_address": current_address,
        "previous_address": previous_address,
        "years_current_address": years_current_address,
        "years_previous_address": years_previous_address,
        "residence_status": residence_status,
        "landlord_contact": landlord_contact,
        "company_name": company_name,
        "company_address": company_address,
        "company_phone": company_phone,
        "department": department,
        "employment_time": employment_time,
        "monthly_income": monthly_income,
        "occupation_type": occupation_type,
        "state_registration": state_registration,
        "other_income": other_income,
        "extra_income": extra_income,
        "other_residents": other_residents,
        "pets": pets,
        "properties": properties,
        "vehicles": vehicles,
        "references": references,
        "has_guarantor": has_guarantor,
        "guarantor_full_name": guarantor_full_name,
        "guarantor_birth_date": guarantor_birth_date,
        "guarantor_rg": guarantor_rg,
        "guarantor_cpf": guarantor_cpf,
        "guarantor_address": guarantor_address,
        "guarantor_profession": guarantor_profession,
        "guarantor_income": guarantor_income,
        "delivery_channel": delivery_channel,
        "delivery_destination": delivery_destination,
    }
    uploaded_files = {
        "Proponente - Documento de identidade e CPF": identity_file,
        "Proponente - Comprovante de residencia": residence_file,
        "Proponente - Comprovante de rendimento ou IRPF": income_file,
    }
    optional_files = {
        "Proponente - Documento do imovel": property_file,
    }
    if has_guarantor:
        uploaded_files.update(
            {
                "Fiador - Documento de identidade e CPF": guarantor_identity_file,
                "Fiador - Comprovante de residencia": guarantor_residence_file,
                "Fiador - Comprovante de renda": guarantor_income_file,
            }
        )
        optional_files["Fiador - Documento do imovel"] = guarantor_property_file

    errors = validate_form(fields, uploaded_files)
    if not accepted_terms:
        errors.append("Confirme a declaração de veracidade e autorização de análise.")

    if errors:
        for error in errors:
            st.error(error)
        return

    protocol = generate_protocol(full_name)
    documents = [
        saved
        for label, uploaded in {**uploaded_files, **optional_files}.items()
        if (saved := save_uploaded_file(protocol, label, uploaded)) is not None
    ]
    guarantor_data = None
    if has_guarantor:
        guarantor_data = GuarantorData(
            full_name=guarantor_full_name,
            birth_date=guarantor_birth_date,
            rg_info=guarantor_rg,
            cpf=guarantor_cpf,
            sex=guarantor_sex,
            marital_status=guarantor_marital_status,
            nationality=guarantor_nationality,
            father_name=guarantor_father,
            mother_name=guarantor_mother,
            work_card=guarantor_work_card,
            spouse_details=guarantor_spouse,
            current_address=guarantor_address,
            residence_status=guarantor_residence_status,
            company_details=guarantor_company,
            profession=guarantor_profession,
            employment_time=guarantor_employment_time,
            monthly_income=guarantor_income,
            other_income=guarantor_other_income,
            occupation_type=guarantor_occupation_type,
            properties=guarantor_properties,
            vehicles=guarantor_vehicles,
            references=guarantor_references,
        )
    submission = ProposalSubmission(
        protocol=protocol,
        property_data=PropertyData(lease_type, property_address, proposed_rent, int(residents_count), fees_notes),
        applicant_data=ApplicantData(
            full_name=full_name,
            birth_date=birth_date,
            profession=profession,
            rg_info=rg_info,
            cpf=cpf,
            phone=phone,
            email=email,
            marital_status=marital_status,
            sex=sex,
            nationality=nationality,
            father_name=father_name,
            mother_name=mother_name,
            spouse_name=spouse_name,
            spouse_cpf=spouse_cpf,
            work_card=work_card,
            current_address=current_address,
            previous_address=previous_address,
            years_current_address=years_current_address,
            years_previous_address=years_previous_address,
            residence_status=residence_status,
            landlord_contact=landlord_contact,
            company_name=company_name,
            company_address=company_address,
            company_phone=company_phone,
            department=department,
            employment_time=employment_time,
            monthly_income=monthly_income,
            occupation_type=occupation_type,
            company_participation=company_participation,
            state_registration=state_registration,
            other_income=other_income,
            extra_income=extra_income,
            other_residents=other_residents,
            pets=pets,
            properties=properties,
            vehicles=vehicles,
            references=references,
        ),
        guarantor_data=guarantor_data,
        delivery_data=DeliveryData(delivery_channel, delivery_destination),
        documents=documents,
    )
    pdf_path = generate_pdf(submission)
    submission.pdf_path = str(pdf_path)
    json_path = save_submission(submission)
    package_path = create_submission_package(submission, json_path)
    submission.package_path = str(package_path)
    save_submission(submission)

    st.session_state["last_pdf_path"] = str(pdf_path)
    st.session_state["last_package_path"] = str(package_path)
    st.session_state["last_protocol"] = protocol
    st.session_state["last_channel"] = delivery_channel
    st.session_state["last_destination"] = delivery_destination
    st.success(f"Proposta gerada com sucesso. Protocolo: {protocol}")


def render_download() -> None:
    pdf_path = st.session_state.get("last_pdf_path")
    if not pdf_path:
        return

    st.divider()
    st.subheader("Proposta gerada")
    st.write(f"Protocolo: `{st.session_state.get('last_protocol')}`")
    with open(pdf_path, "rb") as file:
        st.download_button(
            "Baixar proposta em PDF",
            data=file,
            file_name=f"{st.session_state.get('last_protocol')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    package_path = st.session_state.get("last_package_path")
    if package_path:
        with open(package_path, "rb") as file:
            st.download_button(
                "Baixar proposta e documentos em ZIP",
                data=file,
                file_name=f"{st.session_state.get('last_protocol')}-documentos.zip",
                mime="application/zip",
                use_container_width=True,
            )

    protocol = st.session_state.get("last_protocol")
    channel = st.session_state.get("last_channel")
    destination = st.session_state.get("last_destination", "")
    message = (
        f"Olá. Segue a proposta de locação preenchida. Protocolo: {protocol}. "
        "Baixe o pacote ZIP nesta página e anexe-o a esta conversa."
    )
    st.caption(
        "Por segurança, WhatsApp e e-mail não permitem que o navegador anexe arquivos automaticamente. "
        "Baixe o ZIP acima e anexe-o na mensagem aberta pelo botão."
    )
    if channel == "WhatsApp":
        phone = "".join(character for character in destination if character.isdigit())
        st.link_button(
            "Abrir conversa no WhatsApp",
            f"https://wa.me/{phone}?text={quote(message)}",
            use_container_width=True,
        )
    elif channel == "E-mail":
        subject = quote(f"Proposta de locação - {protocol}")
        body = quote(message)
        st.link_button(
            "Abrir e-mail para envio",
            f"mailto:{destination}?subject={subject}&body={body}",
            use_container_width=True,
        )


def main() -> None:
    init_state()
    render_header()
    render_sidebar()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card"><b>Entrada</b><br><span class="small-muted">Dados e anexos padronizados</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><b>Processo</b><br><span class="small-muted">Validação e protocolo automático</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><b>Saída</b><br><span class="small-muted">PDF profissional para análise</span></div>', unsafe_allow_html=True)

    st.divider()
    render_form()
    render_download()


if __name__ == "__main__":
    main()
