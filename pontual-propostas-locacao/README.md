# Pontual Propostas de Locacao - Streamlit

Aplicacao profissional em Streamlit para substituir um Google Forms de proposta de locacao residencial, com validacao de dados, upload de documentos, protocolo automatico, armazenamento local e geracao de PDF.

## Funcionalidades

- Formulario organizado por etapas.
- Selecao do tipo de locacao: Residencial, Comercial ou Temporada.
- Endereco do imovel e valor do aluguel preenchidos pelo usuario, sem valores predefinidos.
- Validacao de CPF, e-mail, telefone, data de nascimento e campos obrigatorios.
- Dados pessoais, familiares, residenciais, profissionais, renda, patrimonio e referencias.
- Cadastro estruturado de 2 referencias pessoais, com nome e telefone.
- Campo "Possui imovel?" com inclusao de um ou mais imoveis, contendo endereco e inscricao IPTU.
- Campo "Possui veiculo?" com inclusao de um ou mais veiculos, contendo tipo, modelo/ano e placa.
- Cadastro opcional de fiador com documentos proprios.
- Upload de documento de identidade/CPF, comprovante de residencia e comprovante de renda/IRPF.
- Geracao automatica de protocolo.
- Salvamento local dos dados em JSON.
- Geracao de PDF profissional para analise da administradora ou proprietario.
- Geracao de pacote ZIP com proposta e documentos.
- Atalhos para abrir WhatsApp ou e-mail com mensagem de encaminhamento.
- Interface pronta para demonstracao comercial.

## Estrutura

```text
locacao-streamlit-pro/
  app.py
  requirements.txt
  README.md
  run_windows.bat
  src/
    models.py
    pdf_generator.py
    storage.py
    validators.py
  data/
    submissions/
    uploads/
  output/
```

## Entrega para teste externo

Opcao recomendada para cliente leigo: publicar no Streamlit Cloud e enviar apenas o link publico.

Nome recomendado no Streamlit Cloud:

```text
https://pontualpropostasdelocacao.streamlit.app
```

Dominio proprio desejado:

```text
https://pontualpropostasdelocação.app
```

Recomendacao tecnica: usar tambem a versao sem acento `pontualpropostasdelocacao.app`, por ser mais simples para DNS, certificado e digitacao.

Veja o passo a passo em:

```text
DEPLOY_STREAMLIT_CLOUD.md
```

Depois de publicado, envie ao cliente a mensagem modelo em:

```text
MENSAGEM_PARA_CLIENTE.md
```

Tambem existe a opcao local por ZIP, mas ela exige Python instalado no computador do cliente.

Arquivos importantes para o solicitante:

- `LEIA-ME-TESTE.md`: instrucoes simples de teste.
- `COMO_TESTAR_RAPIDO.txt`: passo a passo minimo para cliente leigo.
- `ENTREGA_COMERCIAL.md`: resumo comercial do que foi entregue.
- `CLIQUE_AQUI_PARA_INICIAR.bat`: instala dependencias e inicia a aplicacao.
- `arquivos_teste/`: documentos ficticios para testar os anexos.

## Instalacao no Windows

```powershell
cd C:\projetos\locacao-streamlit-pro
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Execucao

```powershell
cd C:\projetos\locacao-streamlit-pro
.\.venv\Scripts\activate
streamlit run app.py
```

Ou execute:

```powershell
.\run_windows.bat
```

## Como testar

1. Abra a aplicacao no navegador.
2. Preencha todos os campos obrigatorios.
3. Use um CPF valido para passar na validacao.
4. Informe as 2 referencias pessoais obrigatorias.
5. Se possuir imovel, marque `Sim` e use `Adicionar imóvel` para cadastrar mais de um.
6. Se possuir veiculo, marque `Sim` e use `Adicionar veículo` para cadastrar mais de um.
7. Anexe tres arquivos em PDF, PNG, JPG ou JPEG com ate 10 MB cada.
8. Marque a declaracao final.
9. Clique em `Gerar proposta em PDF`.
10. Baixe o PDF gerado e confira os arquivos salvos em:
   - `data/submissions/`
   - `data/uploads/`
   - `output/`

## Evolucoes comerciais recomendadas

- Painel administrativo com filtros e status da proposta.
- Login para imobiliarias, corretores e proprietarios.
- Banco SQLite ou PostgreSQL.
- Assinatura digital.
- Envio automatico por e-mail.
- Integracao com Google Drive, OneDrive ou CRM.
- Analise documental com IA.

## Observacao de seguranca

Esta versao salva dados e documentos localmente nas pastas `data/` e `output/`. Para producao, adicione controle de acesso, politica de retencao de dados, backup e criptografia quando necessario.

No Streamlit Cloud, o armazenamento local e temporario. O usuario deve baixar o ZIP gerado na mesma sessao. Para producao, conecte armazenamento externo e banco de dados.
