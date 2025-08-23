"""
Dashboard Interativo - Análise de Vendas com CRISP-DM
Aplicação Streamlit para visualização de dados e conceitos de percepção visual
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Dashboard CRISP-DM - Análise de Vendas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar o visual
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        border: 1px solid #cccccc;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .css-1d391kg {
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Definir cores corporativas
CORES = {
    'principal': '#2E86AB',
    'secundaria': '#A23B72',
    'sucesso': '#73AB84',
    'alerta': '#F18F01',
    'neutro': '#C4C4C4',
    'destaque': '#C73E1D'
}

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

@st.cache_data
def carregar_dados():
    """Carrega e prepara o dataset de vendas"""
    try:
        df = pd.read_csv('dataset_vendas_completo.csv')
        df['data'] = pd.to_datetime(df['data'])
        
        # Criar features adicionais
        df['ano_mes'] = df['data'].dt.to_period('M').astype(str)
        df['semestre'] = df['data'].dt.month.apply(lambda x: 'S1' if x <= 6 else 'S2')
        df['ano_semestre'] = df['ano'].astype(str) + '-' + df['semestre']
        df['roi'] = ((df['lucro_bruto'] / (df['custo_unitario'] * df['quantidade_vendida'])) * 100).round(2)
        
        return df
    except FileNotFoundError:
        st.error("⚠️ Arquivo 'dataset_vendas_completo.csv' não encontrado. Por favor, gere o dataset primeiro.")
        return None

def calcular_metricas_principais(df):
    """Calcula as métricas principais do dashboard"""
    faturamento_total = df['faturamento'].sum()
    
    # Crescimento YoY
    faturamento_2023 = df[df['ano'] == 2023]['faturamento'].sum()
    faturamento_2024 = df[df['ano'] == 2024]['faturamento'].sum()
    crescimento_yoy = ((faturamento_2024 - faturamento_2023) / faturamento_2023) * 100
    
    # Outras métricas
    margem_media = df['margem_lucro'].mean()
    ticket_medio = df['ticket_medio'].mean()
    volume_total = df['quantidade_vendida'].sum()
    
    return {
        'faturamento_total': faturamento_total,
        'crescimento_yoy': crescimento_yoy,
        'margem_media': margem_media,
        'ticket_medio': ticket_medio,
        'volume_total': volume_total,
        'faturamento_2023': faturamento_2023,
        'faturamento_2024': faturamento_2024
    }

# =============================================================================
# SIDEBAR - NAVEGAÇÃO E FILTROS
# =============================================================================

st.sidebar.image("https://via.placeholder.com/300x100/2E86AB/FFFFFF?text=CRISP-DM+Dashboard", use_column_width=True)
st.sidebar.title("🔄 Metodologia CRISP-DM")
st.sidebar.markdown("---")

# Menu de navegação
pagina = st.sidebar.selectbox(
    "Selecione a Fase:",
    [
        "📚 Visão Geral",
        "1️⃣ Business Understanding",
        "2️⃣ Data Understanding",
        "3️⃣ Data Preparation",
        "4️⃣ Modeling & Analysis",
        "5️⃣ Evaluation",
        "6️⃣ Deployment",
        "🎓 Conceitos de Visualização"
    ]
)

st.sidebar.markdown("---")

# Carregar dados
df = carregar_dados()

if df is not None:
    # Filtros globais
    st.sidebar.subheader("🔍 Filtros Globais")
    
    # Filtro de período
    anos_disponiveis = sorted(df['ano'].unique())
    anos_selecionados = st.sidebar.multiselect(
        "Anos:",
        anos_disponiveis,
        default=anos_disponiveis
    )
    
    # Filtro de região
    regioes_disponiveis = sorted(df['regiao'].unique())
    regioes_selecionadas = st.sidebar.multiselect(
        "Regiões:",
        regioes_disponiveis,
        default=regioes_disponiveis
    )
    
    # Filtro de produto
    produtos_disponiveis = sorted(df['produto'].unique())
    produtos_selecionados = st.sidebar.multiselect(
        "Produtos:",
        produtos_disponiveis,
        default=produtos_disponiveis
    )
    
    # Aplicar filtros
    df_filtrado = df[
        (df['ano'].isin(anos_selecionados)) &
        (df['regiao'].isin(regioes_selecionadas)) &
        (df['produto'].isin(produtos_selecionados))
    ]
    
    # Calcular métricas
    metricas = calcular_metricas_principais(df_filtrado)

# =============================================================================
# CONTEÚDO PRINCIPAL - BASEADO NA PÁGINA SELECIONADA
# =============================================================================

if df is None:
    st.error("Não foi possível carregar os dados. Verifique se o arquivo existe.")
else:
    # PÁGINA: VISÃO GERAL
    if pagina == "📚 Visão Geral":
        st.title("📊 Dashboard de Análise de Vendas - Metodologia CRISP-DM")
        st.markdown("### Aplicando Conceitos de Visualização e Percepção Visual")
        
        # Métricas principais em cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="💰 Faturamento Total",
                value=f"R$ {metricas['faturamento_total']/1e6:.1f}M",
                delta=f"{metricas['crescimento_yoy']:.1f}% YoY"
            )
        
        with col2:
            st.metric(
                label="📈 Crescimento YoY",
                value=f"{metricas['crescimento_yoy']:.1f}%",
                delta="Meta: 15%"
            )
        
        with col3:
            st.metric(
                label="💹 Margem Média",
                value=f"{metricas['margem_media']:.1f}%",
                delta="Meta: 35%"
            )
        
        with col4:
            st.metric(
                label="🎯 Ticket Médio",
                value=f"R$ {metricas['ticket_medio']:.0f}",
                delta=f"{metricas['volume_total']:,} vendas"
            )
        
        st.markdown("---")
        
        # Gráficos principais
        col1, col2 = st.columns(2)
        
        with col1:
            # Evolução temporal
            vendas_mensais = df_filtrado.groupby('data')['faturamento'].sum().reset_index()
            
            fig_temporal = go.Figure()
            fig_temporal.add_trace(go.Scatter(
                x=vendas_mensais['data'],
                y=vendas_mensais['faturamento'],
                mode='lines+markers',
                name='Faturamento',
                line=dict(color=CORES['principal'], width=3),
                fill='tozeroy',
                fillcolor='rgba(46, 134, 171, 0.2)'
            ))
            
            fig_temporal.update_layout(
                title="📈 Evolução do Faturamento Mensal",
                xaxis_title="Período",
                yaxis_title="Faturamento (R$)",
                hovermode='x unified',
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig_temporal, use_container_width=True)
        
        with col2:
            # Top produtos
            top_produtos = df_filtrado.groupby('produto')['faturamento'].sum().nlargest(5)
            
            fig_produtos = go.Figure(data=[
                go.Bar(
                    x=top_produtos.values,
                    y=top_produtos.index,
                    orientation='h',
                    marker_color=[CORES['sucesso'], CORES['principal'], CORES['secundaria'], 
                                 CORES['alerta'], CORES['neutro']][:len(top_produtos)]
                )
            ])
            
            fig_produtos.update_layout(
                title="🏆 Top 5 Produtos por Faturamento",
                xaxis_title="Faturamento (R$)",
                yaxis_title="",
                height=400
            )
            
            st.plotly_chart(fig_produtos, use_container_width=True)
        
        # Tabela resumo
        st.markdown("### 📊 Resumo por Categoria")
        resumo_categoria = df_filtrado.groupby('categoria').agg({
            'faturamento': 'sum',
            'quantidade_vendida': 'sum',
            'margem_lucro': 'mean'
        }).round(2)
        resumo_categoria['faturamento'] = resumo_categoria['faturamento'].apply(lambda x: f"R$ {x/1e6:.2f}M")
        st.dataframe(resumo_categoria, use_container_width=True)
    
    # PÁGINA: BUSINESS UNDERSTANDING
    elif pagina == "1️⃣ Business Understanding":
        st.title("1️⃣ FASE 1: Business Understanding")
        st.markdown("### Entendimento do Negócio e Definição de Objetivos")
        
        # Contexto
        with st.expander("🏢 Contexto do Negócio", expanded=True):
            st.markdown("""
            **Empresa de Tecnologia em Expansão**
            
            A empresa comercializa produtos eletrônicos e acessórios em todo o Brasil, 
            operando em 5 regiões com 5 produtos principais. Busca otimizar suas 
            estratégias comerciais baseadas em dados.
            
            **Desafios Atuais:**
            - Maximizar receita em um mercado competitivo
            - Otimizar o mix de produtos
            - Expandir presença regional
            - Antecipar e aproveitar sazonalidades
            """)
        
        # Objetivos e KPIs
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Objetivos Estratégicos")
            objetivos = [
                "Maximizar Receita",
                "Otimizar Mix de Produtos", 
                "Expansão Regional",
                "Planejamento Sazonal"
            ]
            for obj in objetivos:
                st.success(f"✅ {obj}")
        
        with col2:
            st.markdown("### 📊 KPIs de Sucesso")
            kpis = {
                "Crescimento de Receita": "15% YoY",
                "Margem de Lucro": "> 35%",
                "Penetração Regional": "+20% regiões baixas",
                "ROI de Produtos": "> 25%"
            }
            for kpi, meta in kpis.items():
                st.info(f"📈 {kpi}: {meta}")
        
        # Perguntas de negócio
        st.markdown("### ❓ Perguntas-Chave do Negócio")
        
        perguntas = [
            "Qual é a tendência geral de faturamento da empresa?",
            "Quais produtos/categorias geram maior receita e lucro?",
            "Como o desempenho varia entre as regiões?",
            "Existem padrões sazonais que devemos considerar?",
            "Qual é a evolução da margem de lucro?",
            "Quais combinações produto-região são mais promissoras?"
        ]
        
        for i, pergunta in enumerate(perguntas, 1):
            st.markdown(f"{i}. {pergunta}")
    
    # PÁGINA: DATA UNDERSTANDING
    elif pagina == "2️⃣ Data Understanding":
        st.title("2️⃣ FASE 2: Data Understanding")
        st.markdown("### Exploração e Entendimento dos Dados")
        
        # Informações gerais
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Total de Registros", f"{len(df_filtrado):,}")
        with col2:
            st.metric("📅 Período", f"{df_filtrado['data'].min().strftime('%m/%Y')} - {df_filtrado['data'].max().strftime('%m/%Y')}")
        with col3:
            st.metric("🔢 Variáveis", len(df_filtrado.columns))
        
        # Tabs para diferentes visualizações
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Estatísticas", "🔍 Qualidade", "📊 Distribuições", "💡 Demo Visual"])
        
        with tab1:
            st.markdown("### Estatísticas Descritivas")
            stats_df = df_filtrado[['quantidade_vendida', 'preco_unitario', 'faturamento', 'margem_lucro']].describe()
            st.dataframe(stats_df.style.format("{:.2f}"), use_container_width=True)
        
        with tab2:
            st.markdown("### Verificação de Qualidade dos Dados")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Valores Nulos", df_filtrado.isnull().sum().sum())
                st.metric("Linhas Duplicadas", df_filtrado.duplicated().sum())
            
            with col2:
                completude = (1 - df_filtrado.isnull().sum().sum() / (len(df_filtrado) * len(df_filtrado.columns))) * 100
                st.metric("Completude dos Dados", f"{completude:.1f}%")
                st.metric("Produtos Únicos", df_filtrado['produto'].nunique())
        
        with tab3:
            st.markdown("### Distribuição dos Dados")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribuição por categoria
                fig_cat = px.pie(
                    df_filtrado.groupby('categoria')['faturamento'].sum().reset_index(),
                    values='faturamento',
                    names='categoria',
                    title="Distribuição por Categoria"
                )
                st.plotly_chart(fig_cat, use_container_width=True)
            
            with col2:
                # Distribuição por região
                fig_reg = px.bar(
                    df_filtrado.groupby('regiao')['faturamento'].sum().reset_index(),
                    x='regiao',
                    y='faturamento',
                    title="Faturamento por Região",
                    color='faturamento',
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig_reg, use_container_width=True)
        
        with tab4:
            st.markdown("### 💡 Demonstração: O Poder da Visualização")
            st.info("🧠 **Fato:** O cérebro processa imagens 60.000x mais rápido que texto!")
            
            # Comparação tabela vs gráfico
            col1, col2 = st.columns(2)
            
            vendas_demo = df_filtrado.groupby('mes')['faturamento'].sum().head(12)
            
            with col1:
                st.markdown("#### 📋 Dados em Tabela")
                tabela_demo = pd.DataFrame({
                    'Mês': range(1, len(vendas_demo)+1),
                    'Faturamento': [f"R$ {v/1e6:.2f}M" for v in vendas_demo.values]
                })
                st.dataframe(tabela_demo, use_container_width=True, height=400)
            
            with col2:
                st.markdown("#### 📈 Mesmos Dados em Gráfico")
                fig_demo = go.Figure()
                fig_demo.add_trace(go.Scatter(
                    x=list(range(1, len(vendas_demo)+1)),
                    y=vendas_demo.values,
                    mode='lines+markers',
                    line=dict(color=CORES['principal'], width=3),
                    marker=dict(size=10)
                ))
                fig_demo.update_layout(
                    xaxis_title="Mês",
                    yaxis_title="Faturamento (R$)",
                    height=400,
                    showlegend=False
                )
                st.plotly_chart(fig_demo, use_container_width=True)
            
            st.success("✅ Note como o gráfico revela instantaneamente: tendências, padrões e magnitude das variações!")
    
    # PÁGINA: DATA PREPARATION
    elif pagina == "3️⃣ Data Preparation":
        st.title("3️⃣ FASE 3: Data Preparation")
        st.markdown("### Preparação e Transformação dos Dados")
        
        # Features criadas
        st.markdown("### 🔧 Engenharia de Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Features Temporais Criadas:")
            features_temporais = [
                "ano_mes - Período mensal",
                "trimestre - Trimestre do ano",
                "semestre - Semestre (S1/S2)",
                "ano_semestre - Combinação ano-semestre"
            ]
            for feat in features_temporais:
                st.write(f"• {feat}")
        
        with col2:
            st.markdown("#### Features de Negócio Criadas:")
            features_negocio = [
                "roi - Retorno sobre investimento (%)",
                "receita_por_unidade - Ticket médio",
                "classe_faturamento - Classificação por quartis",
                "eficiência_regional - Índice composto"
            ]
            for feat in features_negocio:
                st.write(f"• {feat}")
        
        # Agregações
        st.markdown("### 📊 Níveis de Agregação Disponíveis")
        
        tabs = st.tabs(["Mensal", "Por Produto", "Por Região", "Produto-Região"])
        
        with tabs[0]:
            df_mensal = df_filtrado.groupby(['ano', 'mes']).agg({
                'faturamento': 'sum',
                'quantidade_vendida': 'sum',
                'margem_lucro': 'mean'
            }).round(2).head(10)
            st.dataframe(df_mensal, use_container_width=True)
        
        with tabs[1]:
            df_produto = df_filtrado.groupby('produto').agg({
                'faturamento': 'sum',
                'quantidade_vendida': 'sum',
                'margem_lucro': 'mean'
            }).round(2)
            st.dataframe(df_produto, use_container_width=True)
        
        with tabs[2]:
            df_regiao = df_filtrado.groupby('regiao').agg({
                'faturamento': 'sum',
                'quantidade_vendida': 'sum',
                'margem_lucro': 'mean'
            }).round(2)
            st.dataframe(df_regiao, use_container_width=True)
        
        with tabs[3]:
            df_prod_reg = df_filtrado.pivot_table(
                values='faturamento',
                index='produto',
                columns='regiao',
                aggfunc='sum'
            ).round(0)
            st.dataframe(df_prod_reg.style.background_gradient(cmap='YlOrRd'), use_container_width=True)
    
    # PÁGINA: MODELING & ANALYSIS
    elif pagina == "4️⃣ Modeling & Analysis":
        st.title("4️⃣ FASE 4: Modeling & Analysis")
        st.markdown("### Análises Avançadas e Visualizações")
        
        # Seletor de análise
        analise = st.selectbox(
            "Selecione o tipo de análise:",
            ["Análise Temporal", "Análise de Produtos", "Análise Regional", "Análise de Sazonalidade"]
        )
        
        if analise == "Análise Temporal":
            st.markdown("### 📈 Análise de Tendência Temporal")
            
            # Preparar dados
            vendas_mensais = df_filtrado.groupby('data').agg({
                'faturamento': 'sum',
                'quantidade_vendida': 'sum',
                'margem_lucro': 'mean'
            }).reset_index()
            
            # Calcular média móvel
            vendas_mensais['media_movel_3'] = vendas_mensais['faturamento'].rolling(window=3, center=True).mean()
            
            # Criar gráfico
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Faturamento Mensal com Tendência', 'Volume de Vendas'),
                vertical_spacing=0.1,
                row_heights=[0.6, 0.4]
            )
            
            # Gráfico principal
            fig.add_trace(
                go.Scatter(
                    x=vendas_mensais['data'],
                    y=vendas_mensais['faturamento'],
                    mode='lines+markers',
                    name='Faturamento Real',
                    line=dict(color=CORES['principal'], width=2),
                    marker=dict(size=6)
                ),
                row=1, col=1
            )
            
            # Média móvel
            fig.add_trace(
                go.Scatter(
                    x=vendas_mensais['data'],
                    y=vendas_mensais['media_movel_3'],
                    mode='lines',
                    name='Média Móvel (3 meses)',
                    line=dict(color=CORES['destaque'], width=2, dash='dash')
                ),
                row=1, col=1
            )
            
            # Volume
            fig.add_trace(
                go.Bar(
                    x=vendas_mensais['data'],
                    y=vendas_mensais['quantidade_vendida'],
                    name='Volume',
                    marker_color=CORES['secundaria'],
                    opacity=0.6
                ),
                row=2, col=1
            )
            
            fig.update_layout(height=600, showlegend=True, hovermode='x unified')
            fig.update_xaxes(title_text="Período", row=2, col=1)
            fig.update_yaxes(title_text="Faturamento (R$)", row=1, col=1)
            fig.update_yaxes(title_text="Unidades", row=2, col=1)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Insights
            col1, col2, col3 = st.columns(3)
            with col1:
                crescimento = ((vendas_mensais['faturamento'].iloc[-1] / vendas_mensais['faturamento'].iloc[0]) - 1) * 100
                st.metric("Crescimento Total", f"{crescimento:.1f}%")
            with col2:
                melhor_mes = vendas_mensais.loc[vendas_mensais['faturamento'].idxmax(), 'data'].strftime('%B/%Y')
                st.metric("Melhor Mês", melhor_mes)
            with col3:
                media_mensal = vendas_mensais['faturamento'].mean()
                st.metric("Média Mensal", f"R$ {media_mensal/1e6:.2f}M")
        
        elif analise == "Análise de Produtos":
            st.markdown("### 💎 Análise Multidimensional de Produtos")
            
            # Preparar dados
            df_produtos = df_filtrado.groupby('produto').agg({
                'faturamento': 'sum',
                'quantidade_vendida': 'sum',
                'margem_lucro': 'mean',
                'preco_unitario': 'mean'
            }).round(2)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Matriz preço vs volume
                fig_scatter = go.Figure()
                
                for produto in df_produtos.index:
                    dados_prod = df_filtrado[df_filtrado['produto'] == produto]
                    categoria = dados_prod['categoria'].iloc[0]
                    cor = CORES['principal'] if categoria == 'Eletrônicos' else CORES['secundaria']
                    
                    fig_scatter.add_trace(go.Scatter(
                        x=[df_produtos.loc[produto, 'preco_unitario']],
                        y=[df_produtos.loc[produto, 'quantidade_vendida']],
                        mode='markers+text',
                        name=produto,
                        text=[produto],
                        textposition='top center',
                        marker=dict(
                            size=df_produtos.loc[produto, 'faturamento']/50000,
                            color=cor,
                            opacity=0.6,
                            line=dict(color='white', width=2)
                        )
                    ))
                
                fig_scatter.update_layout(
                    title="Matriz Preço vs Volume (tamanho = faturamento)",
                    xaxis_title="Preço Médio (R$)",
                    yaxis_title="Volume Total",
                    xaxis_type="log",
                    yaxis_type="log",
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            with col2:
                # Margem por produto
                fig_margem = go.Figure(data=[
                    go.Bar(
                        x=df_produtos.index,
                        y=df_produtos['margem_lucro'],
                        marker_color=[CORES['sucesso'] if m >= 40 else CORES['alerta'] if m >= 35 else CORES['destaque'] 
                                     for m in df_produtos['margem_lucro']],
                        text=df_produtos['margem_lucro'].apply(lambda x: f'{x:.1f}%'),
                        textposition='outside'
                    )
                ])
                
                fig_margem.add_hline(y=40, line_dash="dash", line_color="black", 
                                    annotation_text="Meta: 40%")
                
                fig_margem.update_layout(
                    title="Margem de Lucro por Produto",
                    xaxis_title="",
                    yaxis_title="Margem (%)",
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig_margem, use_container_width=True)
            
            # Heatmap de performance
            st.markdown("#### 🎯 Heatmap de Performance Produto-Região")
            
            matriz_margem = df_filtrado.pivot_table(
                values='margem_lucro',
                index='produto',
                columns='regiao',
                aggfunc='mean'
            )
            
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=matriz_margem.values,
                x=matriz_margem.columns,
                y=matriz_margem.index,
                colorscale='RdYlGn',
                text=matriz_margem.values.round(1),
                texttemplate='%{text}%',
                textfont={"size": 12},
                colorbar=dict(title="Margem (%)")
            ))
            
            fig_heatmap.update_layout(
                title="Margem de Lucro Média (%) por Produto e Região",
                height=400
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        elif analise == "Análise Regional":
            st.markdown("### 🌍 Análise de Performance Regional")
            
            # Preparar dados
            df_regional = df_filtrado.groupby('regiao').agg({
                'faturamento': 'sum',
                'quantidade_vendida': 'sum',
                'margem_lucro': 'mean'
            }).round(2)
            
            # Calcular crescimento YoY
            df_2023 = df_filtrado[df_filtrado['ano'] == 2023].groupby('regiao')['faturamento'].sum()
            df_2024 = df_filtrado[df_filtrado['ano'] == 2024].groupby('regiao')['faturamento'].sum()
            crescimento_regional = ((df_2024 - df_2023) / df_2023 * 100).fillna(0)
            
            # Criar visualizações
            col1, col2 = st.columns(2)
            
            with col1:
                # Mapa de intensidade
                fig_intensidade = go.Figure(data=[
                    go.Bar(
                        y=df_regional.index,
                        x=df_regional['faturamento'],
                        orientation='h',
                        marker=dict(
                            color=df_regional['faturamento'],
                            colorscale='YlOrRd',
                            showscale=True,
                            colorbar=dict(title="Faturamento")
                        ),
                        text=df_regional['faturamento'].apply(lambda x: f'R$ {x/1e6:.1f}M'),
                        textposition='outside'
                    )
                ])
                
                fig_intensidade.update_layout(
                    title="🗺️ Desempenho por Região",
                    xaxis_title="Faturamento (R$)",
                    yaxis_title="",
                    height=400
                )
                
                st.plotly_chart(fig_intensidade, use_container_width=True)
            
            with col2:
                # Crescimento YoY
                fig_crescimento = go.Figure(data=[
                    go.Bar(
                        y=crescimento_regional.index,
                        x=crescimento_regional.values,
                        orientation='h',
                        marker_color=[CORES['sucesso'] if x > 0 else CORES['destaque'] 
                                     for x in crescimento_regional.values],
                        text=crescimento_regional.apply(lambda x: f'{x:.1f}%'),
                        textposition='outside'
                    )
                ])
                
                fig_crescimento.add_vline(x=0, line_width=2, line_color="black")
                
                fig_crescimento.update_layout(
                    title="📈 Crescimento YoY por Região",
                    xaxis_title="Crescimento (%)",
                    yaxis_title="",
                    height=400
                )
                
                st.plotly_chart(fig_crescimento, use_container_width=True)
            
            # Evolução temporal por região
            st.markdown("#### 📊 Evolução Temporal por Região")
            
            fig_evolucao = go.Figure()
            
            for regiao in df_regional.index:
                dados_regiao = df_filtrado[df_filtrado['regiao'] == regiao].groupby('data')['faturamento'].sum()
                
                fig_evolucao.add_trace(go.Scatter(
                    x=dados_regiao.index,
                    y=dados_regiao.values,
                    mode='lines',
                    name=regiao,
                    line=dict(width=3 if regiao == 'Sudeste' else 2)
                ))
            
            fig_evolucao.update_layout(
                title="Evolução do Faturamento por Região",
                xaxis_title="Período",
                yaxis_title="Faturamento (R$)",
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig_evolucao, use_container_width=True)
            
            # Métricas regionais
            st.markdown("#### 📊 Métricas Regionais")
            df_regional['participacao'] = (df_regional['faturamento'] / df_regional['faturamento'].sum() * 100).round(1)
            df_regional['crescimento_yoy'] = crescimento_regional.round(1)
            
            df_display = df_regional[['faturamento', 'participacao', 'margem_lucro', 'crescimento_yoy']].copy()
            df_display.columns = ['Faturamento', 'Participação (%)', 'Margem (%)', 'Crescimento YoY (%)']
            df_display['Faturamento'] = df_display['Faturamento'].apply(lambda x: f'R$ {x/1e6:.2f}M')
            
            st.dataframe(
                df_display.style.background_gradient(subset=['Participação (%)'], cmap='YlOrRd'),
                use_container_width=True
            )
        
        else:  # Análise de Sazonalidade
            st.markdown("### 📅 Análise de Padrões Sazonais")
            
            # Análise por mês
            vendas_por_mes = df_filtrado.groupby('mes')['faturamento'].mean().reset_index()
            meses_nome = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            
            # Criar gráfico de sazonalidade
            fig_sazonal = go.Figure()
            
            # Barras com cores condicionais
            cores_mes = []
            for mes in vendas_por_mes['mes']:
                if mes in [11, 12]:  # Black Friday e Natal
                    cores_mes.append(CORES['destaque'])
                elif mes in [6, 7]:  # Meio do ano
                    cores_mes.append(CORES['alerta'])
                else:
                    cores_mes.append(CORES['neutro'])
            
            fig_sazonal.add_trace(go.Bar(
                x=meses_nome,
                y=vendas_por_mes['faturamento'],
                marker_color=cores_mes,
                text=vendas_por_mes['faturamento'].apply(lambda x: f'R$ {x/1e6:.1f}M'),
                textposition='outside'
            ))
            
            # Linha de média
            media_anual = vendas_por_mes['faturamento'].mean()
            fig_sazonal.add_hline(
                y=media_anual,
                line_dash="dash",
                line_color=CORES['secundaria'],
                annotation_text=f"Média: R$ {media_anual/1e6:.1f}M"
            )
            
            fig_sazonal.update_layout(
                title="📊 Padrão Sazonal - Média de Faturamento por Mês",
                xaxis_title="Mês",
                yaxis_title="Faturamento Médio (R$)",
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig_sazonal, use_container_width=True)
            
            # Análise por trimestre
            col1, col2 = st.columns(2)
            
            with col1:
                vendas_trimestre = df_filtrado.groupby('trimestre')['faturamento'].sum().reset_index()
                
                fig_trimestre = go.Figure(data=[
                    go.Pie(
                        labels=vendas_trimestre['trimestre'],
                        values=vendas_trimestre['faturamento'],
                        hole=0.3,
                        marker=dict(colors=[CORES['principal'], CORES['secundaria'], 
                                          CORES['alerta'], CORES['destaque']])
                    )
                ])
                
                fig_trimestre.update_layout(
                    title="Distribuição por Trimestre",
                    height=350
                )
                
                st.plotly_chart(fig_trimestre, use_container_width=True)
            
            with col2:
                # Insights de sazonalidade
                st.markdown("#### 💡 Insights de Sazonalidade")
                
                # Calcular impacto da sazonalidade
                nov_dez = vendas_por_mes[vendas_por_mes['mes'].isin([11, 12])]['faturamento'].sum()
                total_ano = vendas_por_mes['faturamento'].sum()
                impacto_fim_ano = (nov_dez / total_ano) * 100
                
                st.info(f"""
                **Principais Descobertas:**
                
                • **Black Friday/Natal**: Nov-Dez representam {impacto_fim_ano:.1f}% do faturamento anual
                
                • **Melhor Trimestre**: Q4 com pico de vendas
                
                • **Período de Baixa**: Janeiro e Fevereiro com vendas reduzidas
                
                • **Oportunidade**: Campanhas no meio do ano para equilibrar sazonalidade
                """)
    
    # PÁGINA: EVALUATION
    elif pagina == "5️⃣ Evaluation":
        st.title("5️⃣ FASE 5: Evaluation")
        st.markdown("### Avaliação dos Resultados e KPIs")
        
        # Calcular métricas de avaliação
        faturamento_2023 = df[df['ano'] == 2023]['faturamento'].sum()
        faturamento_2024 = df[df['ano'] == 2024]['faturamento'].sum()
        crescimento_yoy = ((faturamento_2024 - faturamento_2023) / faturamento_2023) * 100
        margem_media = df['margem_lucro'].mean()
        
        # KPIs vs Metas
        st.markdown("### 🎯 Avaliação de KPIs vs Metas")
        
        kpis_avaliacao = [
            {
                'nome': 'Crescimento de Receita',
                'meta': 15,
                'realizado': crescimento_yoy,
                'unidade': '%',
                'tipo': 'percentual'
            },
            {
                'nome': 'Margem de Lucro',
                'meta': 35,
                'realizado': margem_media,
                'unidade': '%',
                'tipo': 'percentual'
            },
            {
                'nome': 'ROI Médio dos Produtos',
                'meta': 25,
                'realizado': df['roi'].mean(),
                'unidade': '%',
                'tipo': 'percentual'
            }
        ]
        
        cols = st.columns(len(kpis_avaliacao))
        
        for i, kpi in enumerate(kpis_avaliacao):
            with cols[i]:
                atingido = kpi['realizado'] >= kpi['meta']
                delta = kpi['realizado'] - kpi['meta']
                
                st.metric(
                    label=kpi['nome'],
                    value=f"{kpi['realizado']:.1f}{kpi['unidade']}",
                    delta=f"{delta:+.1f}{kpi['unidade']} vs meta",
                    delta_color="normal" if atingido else "inverse"
                )
                
                if atingido:
                    st.success("✅ Meta Atingida")
                else:
                    st.error("❌ Meta Não Atingida")
        
        st.markdown("---")
        
        # Análise SWOT
        st.markdown("### 📊 Análise SWOT Baseada em Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💪 FORÇAS")
            forcas = [
                f"Crescimento de {crescimento_yoy:.1f}% YoY",
                f"Margem saudável de {margem_media:.1f}%",
                "Domínio no Sudeste (40% do mercado)",
                "Portfólio diversificado"
            ]
            for f in forcas:
                st.success(f"• {f}")
            
            st.markdown("#### 🎯 OPORTUNIDADES")
            oportunidades = [
                "Potencial de 45% no Norte/Nordeste",
                "Demanda crescente por Notebooks",
                "Expansão em acessórios",
                "Novos canais de venda"
            ]
            for o in oportunidades:
                st.info(f"• {o}")
        
        with col2:
            st.markdown("#### ⚠️ FRAQUEZAS")
            fraquezas = [
                "Baixa penetração no Norte (7%)",
                "Dependência do Q4 (30% vendas)",
                "Variação de margem regional",
                "Concentração em poucos produtos"
            ]
            for f in fraquezas:
                st.warning(f"• {f}")
            
            st.markdown("#### 🚨 AMEAÇAS")
            ameacas = [
                "Sazonalidade afeta fluxo de caixa",
                "Concentração regional = risco",
                "Competição crescente",
                "Volatilidade econômica"
            ]
            for a in ameacas:
                st.error(f"• {a}")
        
        # Score Card Final
        st.markdown("### 📈 Score Card de Performance")
        
        score_total = sum([1 for kpi in kpis_avaliacao if kpi['realizado'] >= kpi['meta']])
        percentual_atingimento = (score_total / len(kpis_avaliacao)) * 100
        
        st.progress(percentual_atingimento / 100)
        st.markdown(f"**Performance Geral: {percentual_atingimento:.0f}% das metas atingidas**")
    
    # PÁGINA: DEPLOYMENT
    elif pagina == "6️⃣ Deployment":
        st.title("6️⃣ FASE 6: Deployment")
        st.markdown("### Plano de Ação e Implementação")
        
        # Roadmap
        st.markdown("### 📅 Roadmap Estratégico 2025")
        
        roadmap = {
            'Q1 2025': {
                'foco': 'Expansão Regional',
                'acoes': ['Piloto no Norte', 'Parceiros locais', 'Análise de mercado'],
                'cor': CORES['principal']
            },
            'Q2 2025': {
                'foco': 'Novos Produtos',
                'acoes': ['Linha Premium', 'Testes A/B', 'Feedback clientes'],
                'cor': CORES['secundaria']
            },
            'Q3 2025': {
                'foco': 'Otimização',
                'acoes': ['Logística', 'Automação', 'Redução custos'],
                'cor': CORES['alerta']
            },
            'Q4 2025': {
                'foco': 'Black Friday',
                'acoes': ['Estoque', 'Marketing', 'Promoções'],
                'cor': CORES['destaque']
            }
        }
        
        cols = st.columns(4)
        for i, (trimestre, info) in enumerate(roadmap.items()):
            with cols[i]:
                st.markdown(f"""
                <div style='background-color: {info['cor']}; color: white; padding: 15px; 
                           border-radius: 10px; text-align: center; height: 200px;'>
                    <h4>{trimestre}</h4>
                    <h5>{info['foco']}</h5>
                    <ul style='text-align: left; font-size: 12px;'>
                        {''.join([f"<li>{acao}</li>" for acao in info['acoes']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Matriz de Priorização
        st.markdown("### 🎯 Matriz de Priorização de Iniciativas")
        
        iniciativas = {
            'Expansão Regional': {'impacto': 8, 'esforco': 7},
            'Novos Produtos': {'impacto': 6, 'esforco': 9},
            'Otimização Margem': {'impacto': 9, 'esforco': 5},
            'Marketing Digital': {'impacto': 5, 'esforco': 6},
            'Automação': {'impacto': 7, 'esforco': 4},
            'Fidelização': {'impacto': 6, 'esforco': 3},
            'Parcerias': {'impacto': 4, 'esforco': 8}
        }
        
        fig_matriz = go.Figure()
        
        for nome, valores in iniciativas.items():
            # Determinar quadrante
            if valores['impacto'] >= 5 and valores['esforco'] < 5:
                cor = CORES['sucesso']  # Quick wins
                simbolo = 'star'
            elif valores['impacto'] >= 5 and valores['esforco'] >= 5:
                cor = CORES['principal']  # Estratégico
                simbolo = 'diamond'
            elif valores['impacto'] < 5 and valores['esforco'] < 5:
                cor = CORES['neutro']  # Baixa prioridade
                simbolo = 'circle'
            else:
                cor = CORES['alerta']  # Repensar
                simbolo = 'x'
            
            fig_matriz.add_trace(go.Scatter(
                x=[valores['esforco']],
                y=[valores['impacto']],
                mode='markers+text',
                name=nome,
                text=[nome],
                textposition='top center',
                marker=dict(size=20, color=cor, symbol=simbolo),
                showlegend=False
            ))
        
        # Adicionar quadrantes
        fig_matriz.add_hline(y=5, line_dash="dash", line_color="gray", opacity=0.5)
        fig_matriz.add_vline(x=5, line_dash="dash", line_color="gray", opacity=0.5)
        
        # Adicionar labels dos quadrantes
        fig_matriz.add_annotation(x=2.5, y=8, text="Quick Wins", showarrow=False, font=dict(size=12, color="green"))
        fig_matriz.add_annotation(x=7.5, y=8, text="Estratégico", showarrow=False, font=dict(size=12, color="blue"))
        fig_matriz.add_annotation(x=2.5, y=2, text="Baixa Prioridade", showarrow=False, font=dict(size=12, color="gray"))
        fig_matriz.add_annotation(x=7.5, y=2, text="Repensar", showarrow=False, font=dict(size=12, color="orange"))
        
        fig_matriz.update_layout(
            title="Matriz de Priorização (Impacto vs Esforço)",
            xaxis_title="Esforço →",
            yaxis_title="Impacto →",
            xaxis=dict(range=[0, 10]),
            yaxis=dict(range=[0, 10]),
            height=500
        )
        
        st.plotly_chart(fig_matriz, use_container_width=True)
        
        # Recomendações finais
        st.markdown("### 📋 Recomendações Estratégicas")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🚀 Curto Prazo (Q1 2025)")
            st.write("""
            • Implementar dashboard real-time
            • Piloto expansão Norte
            • Otimizar estoque sazonal
            • Treinar equipe de vendas
            """)
        
        with col2:
            st.markdown("#### 📈 Médio Prazo (Q2-Q3)")
            st.write("""
            • Lançar linha Premium
            • Parcerias marketplaces
            • Programa fidelidade
            • Automação processos
            """)
        
        with col3:
            st.markdown("#### 🎯 Longo Prazo (Q4+)")
            st.write("""
            • Expansão completa regiões
            • 3 novos produtos
            • Meta: 50% crescimento
            • Liderança no segmento
            """)
    
    # PÁGINA: CONCEITOS DE VISUALIZAÇÃO
    else:  # Conceitos de Visualização
        st.title("🎓 Conceitos de Visualização e Percepção Visual")
        st.markdown("### Princípios Aplicados neste Dashboard")
        
        # Tabs para diferentes conceitos
        tab1, tab2, tab3, tab4 = st.tabs(["Atributos Pré-Atentivos", "Princípios Gestalt", 
                                          "Boas Práticas", "Antes vs Depois"])
        
        with tab1:
            st.markdown("### 👁️ Atributos Pré-Atentivos")
            st.info("Características visuais processadas automaticamente pelo cérebro em milissegundos")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🎨 COR")
                st.write("""
                • Diferenciação instantânea de categorias
                • Destaque de informações críticas
                • Indicação de performance (verde/vermelho)
                """)
                
                # Demonstração
                fig_cor = go.Figure(data=[
                    go.Bar(
                        x=['A', 'B', 'C', 'D', 'E'],
                        y=[10, 15, 13, 17, 9],
                        marker_color=[CORES['neutro'], CORES['neutro'], CORES['destaque'], 
                                     CORES['neutro'], CORES['neutro']]
                    )
                ])
                fig_cor.update_layout(
                    title="Cor direciona atenção instantaneamente",
                    showlegend=False,
                    height=300
                )
                st.plotly_chart(fig_cor, use_container_width=True)
            
            with col2:
                st.markdown("#### 📏 TAMANHO")
                st.write("""
                • Representação de magnitude
                • Hierarquia de importância
                • Comparação visual rápida
                """)
                
                # Demonstração
                fig_tamanho = go.Figure(data=[
                    go.Scatter(
                        x=[1, 2, 3, 4, 5],
                        y=[1, 1, 1, 1, 1],
                        mode='markers',
                        marker=dict(
                            size=[10, 20, 50, 30, 15],
                            color=CORES['principal']
                        )
                    )
                ])
                fig_tamanho.update_layout(
                    title="Tamanho indica magnitude",
                    showlegend=False,
                    height=300,
                    xaxis=dict(showticklabels=False),
                    yaxis=dict(showticklabels=False)
                )
                st.plotly_chart(fig_tamanho, use_container_width=True)
        
        with tab2:
            st.markdown("### 🧩 Princípios Gestalt")
            st.info("Como o cérebro organiza informações visuais em padrões significativos")
            
            princípios = {
                "Proximidade": "Elementos próximos são percebidos como grupo",
                "Similaridade": "Elementos similares são vistos como relacionados",
                "Fechamento": "Tendência a completar formas incompletas",
                "Continuidade": "Olho segue caminhos e linhas",
                "Conexão": "Elementos conectados são um grupo"
            }
            
            for principio, descricao in princípios.items():
                st.markdown(f"**{principio}**: {descricao}")
        
        with tab3:
            st.markdown("### ✅ Boas Práticas Aplicadas")
            
            praticas = [
                "📊 **Escolha apropriada de gráficos**: Linha para tendências, Barra para comparações",
                "🎨 **Uso estratégico de cores**: Máximo 5-7 cores distintas",
                "📝 **Hierarquia clara**: Títulos, subtítulos e anotações",
                "🎯 **Foco no essencial**: Eliminação de elementos desnecessários",
                "📖 **Narrativa visual**: Guiar o leitor através dos dados",
                "♿ **Acessibilidade**: Contraste adequado e texto legível"
            ]
            
            for pratica in praticas:
                st.write(pratica)
        
        with tab4:
            st.markdown("### 🔄 Transformação: Antes vs Depois")
            
            col1, col2 = st.columns(2)
            
            dados_exemplo = df.groupby('produto')['faturamento'].sum().head(5)
            
            with col1:
                st.markdown("#### ❌ Sem Princípios de Design")
                
                fig_antes = go.Figure(data=[
                    go.Bar(
                        x=dados_exemplo.index,
                        y=dados_exemplo.values,
                        marker_color='blue'
                    )
                ])
                fig_antes.update_layout(
                    title="Gráfico Básico",
                    xaxis_title="Produtos",
                    yaxis_title="Valores",
                    height=400
                )
                st.plotly_chart(fig_antes, use_container_width=True)
                
                st.error("""
                **Problemas:**
                • Difícil identificar insights
                • Sem hierarquia visual
                • Cores sem significado
                • Falta contexto
                """)
            
            with col2:
                st.markdown("#### ✅ Com Princípios Aplicados")
                
                dados_sorted = dados_exemplo.sort_values(ascending=True)
                cores = [CORES['sucesso'] if v == dados_sorted.max() else 
                        CORES['destaque'] if v == dados_sorted.min() else 
                        CORES['neutro'] for v in dados_sorted.values]
                
                fig_depois = go.Figure(data=[
                    go.Bar(
                        y=dados_sorted.index,
                        x=dados_sorted.values,
                        orientation='h',
                        marker_color=cores,
                        text=dados_sorted.apply(lambda x: f'R$ {x/1e6:.1f}M'),
                        textposition='outside'
                    )
                ])
                
                fig_depois.update_layout(
                    title="📊 Performance de Produtos - Análise Visual",
                    xaxis_title="Faturamento Total",
                    yaxis_title="",
                    height=400,
                    xaxis=dict(tickformat='R$ ,.0f')
                )
                
                # Adicionar anotação
                fig_depois.add_annotation(
                    x=dados_sorted.max(),
                    y=dados_sorted.idxmax(),
                    text="Líder de vendas!",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor=CORES['sucesso']
                )
                
                st.plotly_chart(fig_depois, use_container_width=True)
                
                st.success("""
                **Melhorias:**
                • Insights imediatos
                • Cores com significado
                • Valores destacados
                • Contexto claro
                """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    Dashboard CRISP-DM | Análise de Vendas 2023-2024 | 
    Desenvolvido para demonstração de conceitos de visualização de dados
</div>
""", unsafe_allow_html=True)