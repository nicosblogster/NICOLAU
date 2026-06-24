# Como testar o sistema de Proposta de Locacao Residencial

Este pacote contem uma aplicacao local para coleta de proposta de locacao residencial, com formulario profissional, validacao de dados, anexos e geracao de PDF.

## Requisitos

- Windows 10 ou superior.
- Python 3.11 ou superior instalado.
- Internet apenas na primeira execucao, para baixar as dependencias.

Se o Python nao estiver instalado, baixe em:

https://www.python.org/downloads/

Durante a instalacao, marque a opcao:

```text
Add python.exe to PATH
```

## Como executar

1. Extraia o arquivo ZIP para uma pasta do computador.
2. Abra a pasta extraida.
3. Clique duas vezes em:

```text
CLIQUE_AQUI_PARA_INICIAR.bat
```

Na primeira execucao, o sistema cria o ambiente virtual e instala as dependencias. Isso pode levar alguns minutos.

Depois, o navegador deve abrir em:

```text
http://localhost:8501
```

Se o navegador nao abrir automaticamente, copie esse endereco e cole no navegador.

## Como testar o fluxo

1. Preencha os dados do imovel.
2. Escolha o tipo de locacao: Residencial, Comercial ou Temporada.
3. Preencha os dados do proponente.
4. Informe um CPF valido.
5. Informe as duas referencias pessoais: nome e telefone.
6. Em `Possui imóvel?`, marque `Sim` apenas se houver imovel proprio. Para mais de um imovel, clique em `Adicionar imóvel`.
7. Em `Possui veículo?`, marque `Sim` apenas se houver veiculo. Para mais de um veiculo, clique em `Adicionar veículo`.
8. Anexe os tres documentos solicitados. Se quiser apenas testar, use os arquivos da pasta `arquivos_teste`.
9. Se escolher `Com fiador`, preencha os dados e anexe os documentos adicionais.
10. Informe se prefere retorno por WhatsApp ou e-mail.
11. Marque a declaracao final.
12. Clique em `Gerar proposta em PDF`.
13. Baixe o PDF, o contrato modelo em Word ou o pacote ZIP completo.
14. Use o botao de WhatsApp/e-mail e anexe o ZIP baixado.

## Modelo Superlogica

O pacote tambem contem:

```text
templates/contrato_locacao_superlogica.docx
```

Esse arquivo usa variaveis no formato `%variavel%`, conforme o material enviado sobre o sistema Superlogica. Antes de uso oficial, revise campos sem variavel direta, como garantia, prazo por extenso e representante do proprietario.

## Onde os arquivos ficam salvos

- PDFs gerados: `output/`
- Dados em JSON: `data/submissions/`
- Documentos anexados: `data/uploads/`

## Observacoes importantes

- Este e um MVP local para demonstracao e validacao do fluxo.
- Nao envie dados reais sensiveis durante testes sem definir uma politica de armazenamento.
- Para uso em producao, recomenda-se adicionar login, banco de dados, controle de acesso e backup.

## Contato para ajustes

Solicite melhorias como painel administrativo, assinatura digital, envio automatico por e-mail, banco de dados e dashboard de acompanhamento.
