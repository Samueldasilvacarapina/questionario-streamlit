import streamlit as st
from fpdf import FPDF
import tempfile
import os

# --- CONFIGURAÇÃO DO QUESTIONÁRIO ---
questionario = [
    {"pergunta": "Qual é a sua linguagem favorita?", "opcoes": ["Python", "JavaScript", "Java", "C#"]},
    {"pergunta": "Qual é o seu sistema operacional?", "opcoes": ["Windows", "Linux", "MacOS"]},
    {"pergunta": "Você gosta de IA?", "opcoes": ["Sim", "Não", "Talvez"]},
    {"pergunta": "Qual é a sua linguagem favorita?", "opcoes": ["Python", "JavaScript", "Java", "C#"]},
    {"pergunta": "Qual é o seu sistema operacional?", "opcoes": ["Windows", "Linux", "MacOS"]},
    {"pergunta": "Você gosta de IA?", "opcoes": ["Sim", "Não", "Talvez"]},
    {"pergunta": "Qual é a sua linguagem favorita?", "opcoes": ["Python", "JavaScript", "Java", "C#"]},
    {"pergunta": "Qual é o seu sistema operacional?", "opcoes": ["Windows", "Linux", "MacOS"]},
    {"pergunta": "Você gosta de IA?", "opcoes": ["Sim", "Não", "Talvez"]},
    {"pergunta": "Qual é a sua linguagem favorita?", "opcoes": ["Python", "JavaScript", "Java", "C#"]},
    {"pergunta": "Qual é o seu sistema operacional?", "opcoes": ["Windows", "Linux", "MacOS"]},
    {"pergunta": "Você gosta de IA?", "opcoes": ["Sim", "Não", "Talvez"]}
]

st.title("📋 Questionário de Informações Essenciais")

# --- LOOP DAS PERGUNTAS ---
respostas = []  # lista para manter todas as respostas na ordem
for idx, q in enumerate(questionario):
    st.subheader(f"{idx+1}. {q['pergunta']}")
    resposta = st.radio("Escolha uma opção:", q["opcoes"], key=f"q{idx}")
    respostas.append((q["pergunta"], resposta))  # salva como tupla (pergunta, resposta)

st.write("---")

# --- CAMPO PARA ANOTAÇÕES ---
anotacao = st.text_area("📝 Anotações Finais (opcional)", height=150)

def gerar_pdf(lista_respostas, anotacao_texto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Respostas do Questionário", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    for i, (pergunta, resposta) in enumerate(lista_respostas, start=1):
        pdf.multi_cell(0, 10, f"{i}. {pergunta}\nResposta: {resposta}")
        pdf.ln(5)

    # Se tiver anotação, adiciona no final
    if anotacao_texto.strip():
        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Anotações Finais:", ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, anotacao_texto)

    # Salvar em arquivo temporário
    temp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(temp_dir, "respostas_questionario.pdf")
    pdf.output(pdf_path)
    return pdf_path

# --- BOTÃO PARA FINALIZAR ---
if st.button("📄 Gerar PDF das respostas"):
    pdf_file = gerar_pdf(respostas, anotacao)
    st.success("✅ PDF gerado com sucesso!")
    
    # Exibir botão para download
    with open(pdf_file, "rb") as f:
        st.download_button("⬇️ Baixar respostas em PDF", f, file_name="respostas_questionario.pdf")
