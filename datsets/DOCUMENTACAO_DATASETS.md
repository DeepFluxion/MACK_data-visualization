
# DOCUMENTAÇÃO DOS DATASETS GERADOS
=====================================

## 1. DATASET DE VENDAS E FATURAMENTO (dataset_vendas_completo.csv)

### Descrição:
Dataset com 24 meses de dados de vendas de uma empresa de tecnologia, 
incluindo 5 produtos em 5 regiões do Brasil.

### Colunas:
- data: Data (primeiro dia do mês)
- ano: Ano
- mes: Número do mês
- mes_nome: Nome do mês
- trimestre: Trimestre (Q1-Q4)
- produto: Nome do produto
- categoria: Categoria do produto (Eletrônicos/Acessórios)
- regiao: Região do Brasil
- quantidade_vendida: Unidades vendidas
- preco_unitario: Preço unitário em R$
- faturamento: Faturamento total em R$
- custo_unitario: Custo unitário em R$
- lucro_bruto: Lucro bruto em R$
- margem_lucro: Margem de lucro em %
- ticket_medio: Ticket médio em R$

### Características dos dados:
- Sazonalidade: Black Friday/Natal (alta), Janeiro/Fevereiro (baixa)
- Tendência: Crescimento médio de 0.8% ao mês
- Produtos com diferentes padrões sazonais
- Distribuição regional baseada em população/poder de compra

### Perguntas sugeridas para análise:
1. Qual foi o faturamento total por trimestre?
2. Qual produto teve maior crescimento percentual?
3. Como as vendas variam por região?
4. Qual o impacto da sazonalidade nas vendas?
5. Qual categoria é mais lucrativa?

---

## 2. DATASET DE ATENDIMENTO AO CLIENTE (dataset_atendimento_completo.csv)

### Descrição:
Dataset com 24 meses de dados de atendimento ao cliente através de 
múltiplos canais, incluindo métricas de desempenho e satisfação.

### Colunas:
- data: Data (primeiro dia do mês)
- ano: Ano
- mes: Número do mês
- mes_nome: Nome do mês
- trimestre: Trimestre
- canal: Canal de atendimento
- tipo_problema: Classificação do problema
- prioridade: Nível de prioridade
- quantidade_tickets: Volume de tickets
- tempo_medio_resolucao_horas: Tempo médio de resolução
- satisfacao_media: Nota de satisfação (1-5)
- taxa_resolucao_primeiro_contato: Taxa de FCR
- tickets_reabertos: Quantidade de reaberturas
- custo_medio_por_ticket: Custo médio em R$
- eficiencia_canal: Índice de eficiência (0-100)

### Características dos dados:
- Crescimento no volume: 30 tickets/mês
- Picos em Janeiro, Julho, Novembro e Dezembro
- Canais com diferentes perfis de eficiência
- Correlação entre tempo de resolução e satisfação

### Perguntas sugeridas para análise:
1. Qual canal é mais eficiente?
2. Como o volume de tickets evolui ao longo do tempo?
3. Existe correlação entre prioridade e tempo de resolução?
4. Qual tipo de problema é mais frequente?
5. Como reduzir o custo total de atendimento?

---

## 3. DATASET DE PESQUISA DE MERCADO (dataset_pesquisa_mercado.csv)

### Descrição:
Dataset trimestral com dados de penetração e uso de serviços digitais,
segmentado por demografia (idade, região, classe social).

### Colunas:
- data: Data (primeiro dia do trimestre)
- ano: Ano
- trimestre: Trimestre
- servico: Tipo de serviço digital
- faixa_etaria: Faixa de idade
- regiao: Região do Brasil
- classe_social: Classe socioeconômica
- tamanho_amostra: Tamanho da amostra pesquisada
- usuarios_ativos: Número de usuários ativos
- penetracao_percentual: Taxa de penetração em %
- frequencia_uso_semanal: Frequência de uso (vezes/semana)
- satisfacao_media: Satisfação (1-10)
- intencao_continuar_pct: Intenção de continuar usando em %
- nao_usuarios: Número de não usuários
- potencial_crescimento_pct: Potencial de crescimento em %
- nps_estimado: Net Promoter Score estimado

### Características dos dados:
- 8 serviços digitais diferentes
- 6 faixas etárias
- 5 regiões
- 4 classes sociais
- Tendências de crescimento variadas por serviço

### Perguntas sugeridas para análise:
1. Qual serviço tem maior penetração?
2. Como a adoção varia por faixa etária?
3. Quais regiões têm maior potencial de crescimento?
4. Existe correlação entre classe social e uso de serviços?
5. Quais serviços estão crescendo mais rápido?

---

## 4. DATASETS SIMPLIFICADOS (Para exercícios iniciais)

### 4.1 Vendas Mensais (dataset_vendas_mensais.csv)
- Dados agregados mensais de faturamento
- Ideal para gráficos de linha simples
- 12 meses de dados

### 4.2 Comparação de Produtos (dataset_produtos_comparacao.csv)
- Snapshot comparativo de 5 produtos
- Ideal para gráficos de barras
- Inclui crescimento ano a ano

### 4.3 Categorias (dataset_categorias.csv)
- Distribuição de faturamento por categoria
- Ideal para gráficos de pizza/donut
- Inclui percentuais calculados

### 4.4 Canais de Satisfação (dataset_canais_satisfacao.csv)
- Métricas de desempenho por canal
- Ideal para análises de correlação
- Combina volume, satisfação e custo

---

## EXEMPLOS DE USO DOS DATASETS

### Exemplo 1: Análise de Tendência Temporal
```python
import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
df = pd.read_csv('dataset_vendas_completo.csv')
df['data'] = pd.to_datetime(df['data'])

# Agregar por mês
vendas_mensais = df.groupby('data')['faturamento'].sum()

# Plotar
plt.figure(figsize=(12, 6))
plt.plot(vendas_mensais.index, vendas_mensais.values)
plt.title('Evolução do Faturamento Mensal')
plt.xlabel('Mês')
plt.ylabel('Faturamento (R$)')
plt.grid(True, alpha=0.3)
plt.show()
```

### Exemplo 2: Comparação entre Categorias
```python
# Carregar dados simplificados
df_cat = pd.read_csv('dataset_categorias.csv')

# Criar gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(df_cat['categoria'], df_cat['faturamento_anual'])
plt.title('Faturamento por Categoria')
plt.xlabel('Categoria')
plt.ylabel('Faturamento Anual (R$)')
plt.xticks(rotation=45)
plt.show()
```

### Exemplo 3: Análise de Correlação
```python
# Carregar dados de atendimento
df_at = pd.read_csv('dataset_atendimento_completo.csv')

# Calcular correlação
correlacao = df_at[['tempo_medio_resolucao_horas', 
                     'satisfacao_media']].corr()

# Visualizar
plt.figure(figsize=(8, 6))
plt.scatter(df_at['tempo_medio_resolucao_horas'], 
           df_at['satisfacao_media'], alpha=0.5)
plt.xlabel('Tempo de Resolução (horas)')
plt.ylabel('Satisfação Média')
plt.title('Relação entre Tempo de Resolução e Satisfação')
plt.show()
```

---

## NOTAS IMPORTANTES

1. **Reprodutibilidade**: Os datasets usam seed fixo (42) para permitir reprodução
2. **Realismo**: Incluem variações, sazonalidades e ruído similares a dados reais
3. **Complexidade Gradual**: Desde datasets simples até complexos
4. **Flexibilidade**: Podem ser filtrados/agregados para diferentes exercícios
5. **Encoding**: Todos salvos em UTF-8 para compatibilidade

