# Publicar no Streamlit Cloud

Este projeto esta pronto para gerar um link publico pelo Streamlit Community Cloud.

## Resultado esperado

Depois da publicacao, o cliente acessa o sistema por um link parecido com:

```text
https://pontualpropostasdelocacao.streamlit.app
```

O cliente nao precisa instalar Python, baixar ZIP ou executar arquivo `.bat`.

## Sobre o dominio desejado

Dominio solicitado:

```text
https://pontualpropostasdelocação.app
```

Ponto tecnico importante: dominios com acento/cedilha usam IDN/Punycode na configuracao DNS. A forma tecnica desse dominio e:

```text
xn--pontualpropostasdelocao-s7b3h.app
```

Para evitar problemas de digitacao, certificado e configuracao, a recomendacao comercial e registrar tambem a versao sem acento:

```text
https://pontualpropostasdelocacao.app
```

O Streamlit Community Cloud publica apps em subdominios `streamlit.app`. Para usar um dominio proprio `.app`, ha duas alternativas:

1. Usar `pontualpropostasdelocacao.streamlit.app` como link principal imediato.
2. Registrar `pontualpropostasdelocacao.app` e configurar redirecionamento para o link Streamlit, ou hospedar em uma plataforma que aceite dominio customizado diretamente.

## Passo a passo

### 1. Criar um repositorio no GitHub

Crie um repositorio, por exemplo:

```text
locacao-streamlit-pro
```

Envie estes arquivos para o repositorio:

```text
app.py
requirements.txt
runtime.txt
.streamlit/config.toml
src/
README.md
LEIA-ME-TESTE.md
ENTREGA_COMERCIAL.md
```

Nao envie:

```text
.venv/
data/submissions/
data/uploads/
output/
dist/
```

Esses caminhos ja estao protegidos no `.gitignore`.

### 2. Acessar o Streamlit Cloud

Entre em:

```text
https://share.streamlit.io/
```

Faca login com a conta GitHub.

### 3. Criar o app

Clique em:

```text
New app
```

Selecione:

```text
Repository: locacao-streamlit-pro
Branch: main
Main file path: app.py
```

No campo de URL, use:

```text
pontualpropostasdelocacao
```

Depois clique em:

```text
Deploy
```

### 4. Copiar o link

Ao final do deploy, o Streamlit Cloud gera um link publico.

Envie esse link para o cliente testar.

## Observacao importante sobre esta versao

Esta versao e ideal para demonstracao e validacao comercial.

No Streamlit Cloud, arquivos enviados e PDFs gerados podem nao ser persistentes de forma definitiva. Para uso profissional em producao, o proximo passo recomendado e adicionar:

- Banco de dados.
- Login.
- Armazenamento em nuvem para anexos.
- Painel administrativo.
- Envio automatico por e-mail.
