# Variaveis Superlogica para contratos

Fonte analisada: `Variaveis para preenchimento - sistema Superlogica.pdf`.

## Imobiliaria

- `%imobiliariaNome%`: nome da imobiliaria.
- `%imobiliariaNomeFantasia%`: nome fantasia da imobiliaria.
- `%imobiliariaCidade%`: cidade da imobiliaria.
- `%imobiliariaEstado%`: estado da imobiliaria.
- `%imobiliariaEndereco%`: endereco completo da imobiliaria.
- `%imobiliariaCNPJ%`: CNPJ da imobiliaria.
- `%imobiliariaTelefone%`: telefone de contato da imobiliaria.

## Datas

- `%hoje%`: data atual.
- `%dia_atual%`: dia atual em numero.
- `%dia_atual_extenso%`: dia atual por extenso.
- `%amanha%`: data de amanha.
- `%mes_atual%`: mes atual.
- `%mes_atual_extenso%`: mes atual por extenso.
- `%mes_anterior%`: mes anterior.
- `%mes_anterior_extenso%`: mes anterior por extenso.
- `%mes_subsequente%`: proximo mes.
- `%mes_subsequente_extenso%`: proximo mes por extenso.
- `%ano_atual%`: ano atual.
- `%ano_anterior%`: ano anterior.

## Proprietario

- `%proprietarioNome%`: nome completo do proprietario.
- `%proprietarioTelefone%`: telefone do proprietario.
- `%proprietarioCelular%`: celular do proprietario.
- `%proprietarioEmail%`: e-mail do proprietario.
- `%proprietarioRg%`: RG do proprietario.
- `%proprietarioCpf%`: CPF do proprietario.
- `%proprietarioEndereco%`: endereco completo do proprietario.
- `%proprietarioBairro%`: bairro onde reside o proprietario.
- `%proprietarioCidade%`: cidade do proprietario.
- `%proprietarioEstado%`: estado do proprietario.
- `%dadosProprietarios%`: todos os dados do proprietario.
- `%dadosRecebimentoDoRepasse%`: dados bancarios para repasse ao proprietario.

## Inquilino

- `%inquilinoNome%`: nome completo do inquilino.
- `%inquilinoTelefone%`: telefone do inquilino.
- `%inquilinoCelular%`: celular do inquilino.
- `%inquilinoEmail%`: e-mail do inquilino.
- `%inquilinoRg%`: RG do inquilino.
- `%inquilinoCpf%`: CPF do inquilino.
- `%inquilinoEndereco%`: endereco completo do inquilino.
- `%dadosInquilinos%`: todos os dados do inquilino.

## Imovel

- `%imovelCep%`: CEP do imovel.
- `%imovelRua%`: rua do imovel.
- `%imovelNumero%`: numero do imovel.
- `%imovelBairro%`: bairro do imovel.
- `%imovelCidade%`: cidade onde o imovel esta localizado.
- `%imovelEstado%`: estado do imovel.
- `%imovelValorAluguel%`: valor de aluguel do imovel.
- `%imovelTipo%`: tipo do imovel, como casa ou apartamento.
- `%imovelEnderecoCompleto%`: endereco completo do imovel com CEP.

## Contrato

- `%contratoCodigo%`: codigo do contrato.
- `%contratoDataInicio%`: data de inicio do contrato.
- `%contratoDataTermino%`: data de rescisao/termino do contrato.
- `%contratoValorAluguel%`: valor do aluguel previsto no contrato.
- `%contratoDiaVencimento%`: dia de vencimento do aluguel.
- `%contratoJuros%`: juros aplicados ao contrato.
- `%contratoMulta%`: multa do contrato.
- `%contratoAssinaturas%`: informacoes de assinatura do contrato.

## Mapeamento aplicado no modelo

- Locadora/proprietario: `%dadosProprietarios%`.
- Administradora: `%imobiliariaNome%`, `%imobiliariaCNPJ%`, `%imobiliariaEndereco%`, `%imobiliariaTelefone%`.
- Locatario/inquilino: `%dadosInquilinos%`.
- Imovel: `%imovelEnderecoCompleto%`.
- Valor do aluguel: `%contratoValorAluguel%`.
- Inicio e termino: `%contratoDataInicio%` e `%contratoDataTermino%`.
- Assinaturas: `%contratoAssinaturas%`, `%proprietarioNome%` e `%inquilinoNome%`.

## Observacao tecnica

Alguns campos do contrato original nao apareceram na lista do PDF, como prazo total da locacao por extenso, clausula de garantia detalhada e representante/curador do proprietario. Esses pontos devem ser mantidos como texto fixo, revisados manualmente ou configurados no Superlogica se houver variaveis adicionais disponiveis no ambiente do cliente.
