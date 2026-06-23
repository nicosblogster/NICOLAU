# Entrega Comercial - Pontual Propostas de Locacao

## Objetivo

Substituir um formulario simples por uma aplicacao profissional para coleta, validacao e organizacao de propostas de locacao residencial.

## Problema resolvido

Administradoras, imobiliarias e proprietarios costumam receber dados incompletos, documentos dispersos e propostas sem padronizacao. Este sistema centraliza o processo e gera uma saida documental pronta para analise.

## Funcionalidades entregues

- Formulario digital com organizacao por secoes.
- Abertura da proposta por tipo de locacao: Residencial, Comercial ou Temporada.
- Campos baseados no questionario original.
- Endereco do imovel e aluguel inicialmente em branco.
- Dados familiares, historico residencial, vinculo profissional, renda, patrimonio e referencias.
- Cadastro condicional de fiador.
- Validacao de CPF, telefone, e-mail e data de nascimento.
- Upload de documentos obrigatorios.
- Geracao de protocolo unico.
- Armazenamento local dos dados preenchidos.
- Organizacao dos documentos por protocolo.
- Geracao automatica de PDF.
- Pacote ZIP com PDF, JSON e documentos anexados.
- Encaminhamento assistido por WhatsApp ou e-mail.
- Interface visual para demonstracao comercial.

## Diferenciais para venda

- Reduz retrabalho na coleta cadastral.
- Padroniza propostas recebidas.
- Facilita a analise documental.
- Evita perda de anexos em conversas de WhatsApp/e-mail.
- Permite evolucao para painel administrativo, CRM e automacoes.

## Limites da versao MVP

- Roda localmente no computador.
- Nao possui login.
- Nao possui banco de dados remoto.
- Nao envia e-mail automaticamente.
- WhatsApp e e-mail sao abertos com mensagem pronta; por seguranca do navegador, o usuario anexa o ZIP baixado.
- Nao realiza assinatura digital.

## Evolucao sugerida para versao profissional

1. Painel administrativo com lista de propostas.
2. Status da proposta: recebida, em analise, aprovada, recusada.
3. Banco SQLite para uso local ou PostgreSQL para nuvem.
4. Login por perfil: administrador, corretor e proprietario.
5. Envio automatico de PDF por e-mail.
6. Integracao com Google Drive ou OneDrive.
7. Assinatura digital.
8. Dashboard com indicadores.

## Arquivos principais

- `app.py`: interface principal.
- `src/validators.py`: validacoes.
- `src/storage.py`: salvamento local.
- `src/pdf_generator.py`: geracao do PDF.
- `requirements.txt`: dependencias.
- `run_windows.bat`: execucao simplificada no Windows.
