# Eval Replay Report

Casos: 3  
Accuracy geral: 0.00%

## Accuracy por campo

| campo | accuracy |
|---|---|
| emissor | 0.00% |
| endereco | 0.00% |
| valor | 66.67% |
| vencimento | 0.00% |

## Mismatches

### inv-01

| campo | esperado | previsto |
|---|---|---|
| emissor | Tech Solutions Ltda. | DE SERVIÇOS **Emissor:** Tech Solutions Ltda. **CNPJ / Endereço:** 12.345.678/0001-90 - Av. Paulista, 1000, Bela Vista, São Paulo - SP **Cliente:** Exemplo Serviços S.A. --- ### Descrição dos Serviços - Consultoria Técnica em TI: R$ 1.500,00 --- **Valor |
| endereco | 12.345.678/0001-90 - Av. Paulista, 1000, Bela Vista, São Paulo - SP | 12.345.678/0001-90 |
| vencimento | 2026-09-15 |  |

### inv-02

| campo | esperado | previsto |
|---|---|---|
| emissor | Logística Expressa do Brasil S.A. | # NOTA FISCAL DE PRESTAÇÃO DE SERVIÇOS **Emissor:** Logístic |
| endereco | 98.765.432/0001-10 - Rua das Flores, 500, Curitiba - PR | 98.765.432/0001-10 |
| vencimento | 2026-09-10 |  |

### inv-03

| campo | esperado | previsto |
|---|---|---|
| emissor | Cloud Hosting Services LLC | # INVOICE **Issuer:** Cloud Hosting Services LLC **Address / |
| endereco | 100 Main St, Suite 400, Austin, TX 78701 |  |
| valor | 320.0 | 0.0 |
| vencimento | 2026-10-01 |  |
