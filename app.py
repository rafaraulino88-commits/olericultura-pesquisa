import os
import pandas as pd
import streamlit as st

# Criar pasta para salvar as fotos se não existir
PASTA_FOTOS = "fotos_pesquisa"
if not os.path.exists(PASTA_FOTOS):
    os.makedirs(PASTA_FOTOS)

# Configuração da página otimizada para tablet
st.set_page_config(
    page_title="Olericultura Biometria", page_icon="🌱", layout="centered"
)

st.title("🌱 Olericultura: Coleta de Dados Biométricos & Fotos")
st.markdown(
    "Registre parâmetros de folhas, frutos, desenvolvimento e fitossanidade direto do campo."
)

# Inicializar banco de dados temporário na sessão com os novos campos
if "dados_campo" not in st.session_state:
    st.session_state["dados_campo"] = pd.DataFrame(
        columns=[
            "Ensaio",
            "Tratamento",
            "Repetição",
            "Data Avaliação",
            "Altura da Planta (cm)",
            "Qtd de Folhas",
            "Tamanho da Folha (cm)",
            "Largura da Folha (cm)",
            "Tamanho do Fruto (cm)",
            "Espessura do Fruto (mm)",
            "Doença / Patógeno",
            "Severidade (%)",
            "Observações",
            "Foto Caminho",
        ]
    )

menu = st.sidebar.selectbox(
    "Navegação",
    ["1. Lançar Dados Biométricos", "2. Visualizar e Gráficos", "3. Relatórios"],
)

# ==========================================
# 1. LANÇAMENTO DE DADOS COM PARÂMETROS
# ==========================================
if menu == "1. Lançar Dados Biométricos":
    st.header("📝 Novo Registro de Campo")

    with st.form("form_biometria"):
        st.subheader("📌 Identificação da Amostra")
        col_id1, col_id2, col_id3 = st.columns(3)
        with col_id1:
            ensaio = st.text_input(
                "Nome do Ensaio", placeholder="Ex: Alface Crespa - Inverno"
            )
        with col_id2:
            tratamento = st.text_input(
                "Tratamento", placeholder="Ex: T1 (Controle), T2 (Dose X)"
            )
        with col_id3:
            repeticao = st.selectbox("Repetição / Bloco", ["R1", "R2", "R3", "R4"])

        st.markdown("---")
        st.subheader("🌿 Parâmetros Vegetativos (Folhas e Planta)")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            altura_planta = st.number_input(
                "Altura da Planta (cm)", min_value=0.0, format="%.2f"
            )
            qtd_folhas = st.number_input(
                "Quantidade de Folhas", min_value=0, step=1
            )
        with col_v2:
            tamanho_folha = st.number_input(
                "Comprimento da Folha (cm)", min_value=0.0, format="%.2f"
            )
            largura_folha = st.number_input(
                "Largura da Folha (cm)", min_value=0.0, format="%.2f"
            )

        st.markdown("---")
        st.subheader("🍅 Parâmetros de Frutos (Se aplicável)")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            tamanho_fruto = st.number_input(
                "Tamanho / Diâmetro do Fruto (cm)", min_value=0.0, format="%.2f"
            )
        with col_f2:
            espessura_fruto = st.number_input(
                "Espessura do Fruto (mm)", min_value=0.0, format="%.2f"
            )

        st.markdown("---")
        st.subheader("🦠 Fitossanidade e Observações")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            doenca = st.text_input(
                "Doença / Patógeno", placeholder="Ex: Míldio, Requeima"
            )
        with col_p2:
            severidade = st.slider("Severidade estimada (%)", 0, 100, 0)

        obs = st.text_area(
            "Observações de Campo", placeholder="Clima, vigor, pragas..."
        )

        st.markdown("---")
        st.subheader("📷 Registro Fotográfico")
        foto_capturada = st.camera_input("Tirar Foto (Câmera ou Galeria)")

        submit = st.form_submit_button("💾 Salvar Avaliação")

        if submit:
            if ensaio and tratamento:
                caminho_foto_salva = ""
                if foto_capturada is not None:
                    nome_arquivo = f"{ensaio}_{tratamento}_{repeticao}_{foto_capturada.name}".replace(
                        " ", "_"
                    )
                    caminho_foto_salva = os.path.join(
                        PASTA_FOTOS, nome_arquivo
                    )
                    with open(caminho_foto_salva, "wb") as f:
                        f.write(foto_capturada.getbuffer())

                novo_registro = {
                    "Ensaio": ensaio,
                    "Tratamento": tratamento,
                    "Repetição": repeticao,
                    "Data Avaliação": str(pd.Timestamp.today().date()),
                    "Altura da Planta (cm)": altura_planta,
                    "Qtd de Folhas": qtd_folhas,
                    "Tamanho da Folha (cm)": tamanho_folha,
                    "Largura da Folha (cm)": largura_folha,
                    "Tamanho do Fruto (cm)": tamanho_fruto,
                    "Espessura do Fruto (mm)": espessura_fruto,
                    "Doença / Patógeno": doenca if doenca else "Nenhum",
                    "Severidade (%)": severidade,
                    "Observações": obs,
                    "Foto Caminho": caminho_foto_salva,
                }

                st.session_state["dados_campo"] = pd.concat(
                    [
                        st.session_state["dados_campo"],
                        pd.DataFrame([novo_registro]),
                    ],
                    ignore_index=True,
                )
                st.success("Dados salvos com sucesso!")
            else:
                st.warning("Preencha pelo menos o Ensaio e o Tratamento.")

# ==========================================
# 2. VISUALIZAR DADOS E GRÁFICOS
# ==========================================
elif menu == "2. Visualizar e Gráficos":
    st.header("📊 Análise Gráfica dos Parâmetros")

    df = st.session_state["dados_campo"]

    if df.empty:
        st.info("Nenhum dado cadastrado ainda.")
    else:
        ensaio_sel = st.selectbox(
            "Selecione o Ensaio para Analisar", df["Ensaio"].unique()
        )
        df_f = df[df["Ensaio"] == ensaio_sel]

        colunas_numericas = [
            "Altura da Planta (cm)",
            "Qtd de Folhas",
            "Tamanho da Folha (cm)",
            "Largura da Folha (cm)",
            "Tamanho do Fruto (cm)",
            "Espessura do Fruto (mm)",
            "Severidade (%)",
        ]
        df_medias = df_f.groupby("Tratamento")[colunas_numericas].mean().reset_index()

        st.subheader("Médias Calculadas por Tratamento")
        st.dataframe(df_medias, use_container_width=True)

        st.subheader("Gráficos Comparativos")
        param_escolhido = st.selectbox(
            "Escolha o parâmetro para gerar o gráfico", colunas_numericas
        )

        if not df_medias.empty:
            st.bar_chart(
                df_medias.set_index("Tratamento")[param_escolhido]
            )

        st.markdown("---")
        st.subheader("🖼️ Galeria de Fotos Registradas")
        for index, row in df_f.iterrows():
            if (
                pd.notna(row["Foto Caminho"])
                and row["Foto Caminho"] != ""
                and os.path.exists(row["Foto Caminho"])
            ):
                st.image(
                    row["Foto Caminho"],
                    caption=f"Tratamento: {row['Tratamento']} ({row['Repetição']}) - {row['Doença / Patógeno']}",
                    width=250,
                )

# ==========================================
# 3. RELATÓRIOS
# ==========================================
elif menu == "3. Relatórios":
    st.header("📄 Relatório Técnico e Exportação")
    df = st.session_state["dados_campo"]

    if df.empty:
        st.info("Sem dados para exportar.")
    else:
        ensaio_rel = st.selectbox(
            "Selecione o Ensaio para o Relatório", df["Ensaio"].unique()
        )
        df_rel = df[df["Ensaio"] == ensaio_rel]

        st.markdown(f"### Resumo do Ensaio: **{ensaio_rel}**")
        resumo_final = (
            df_rel.groupby("Tratamento")[
                [
                    "Altura da Planta (cm)",
                    "Qtd de Folhas",
                    "Tamanho da Folha (cm)",
                    "Largura da Folha (cm)",
                    "Tamanho do Fruto (cm)",
                    "Espessura do Fruto (mm)",
                    "Severidade (%)",
                ]
            ]
            .mean()
            .reset_index()
        )
        st.dataframe(resumo_final, use_container_width=True)

        csv = df_rel.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Baixar Relatório em Planilha (CSV)",
            data=csv,
            file_name=f"relatorio_biometria_{ensaio_rel}.csv",
            mime="text/csv",
)
