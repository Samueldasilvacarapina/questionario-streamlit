import streamlit as st
from fpdf import FPDF
import tempfile
import os

# --- CONFIGURAÇÃO DO QUESTIONÁRIO ---
questionario = [
    {"pergunta": "Nome completo do cliente?", "opcoes": []},
    {"pergunta": "Qual seu CPF?", "opcoes": []},
    {"pergunta": "Qual seu RG?", "opcoes": []},
    {"pergunta": "Qual seu estado Cívil? Ex: Solteiro, Casado, etc.", "opcoes": ["CASADO(A)", "SOLTEIRO(A)", "DIVORCIADO(A)", "VIÚVO(A)", "UNIÃO ESTÁVEL", "OUTROS"]},
    {"pergunta": "Qual seu endereço completo com CEP?", "opcoes": []},
    {"pergunta": "Qual sua profissão?", "opcoes": []},
    {"pergunta": "O senhor(a) recebeu algum cartão?", "opcoes": ["SIM", "NÃO", "TALVEZ"]},
    {"pergunta": "Em caso afirmativo, o senhor(a) faz uso?", "opcoes": ["SIM", "NÃO", "TALVEZ"]},
    {"pergunta": "O senhor(a) desbloqueou o cartão", "opcoes": ["SIM", "NÃO", "TALVEZ"]},
    {"pergunta": "O senhor(a) sabe se possui algum cartão vinculado no seu benefício?", "opcoes": ["SIM", "NÃO", "TALVEZ"]},
    {"pergunta": "O senhor(a) recebeu algum valor em alguma de suas contas?", "opcoes": ["SIM", "NÃO", "TALVEZ"]},
    {"pergunta": "O senhor(a) recebe faturas desse cartão?", "opcoes": ["SIM", "NÃO", "TALVEZ"]},
    {"pergunta": "O senhor(a) chegou a pagar alguma fatura ou somente por meio dos descontos?", "opcoes": ["SIM", "NÃO", "TALVEZ"]},
    {"pergunta": "O senhor(a) possui ação judicial sobre esse assunto com outro advogado?", "opcoes": ["SIM", "NÃO", "TALVEZ"]},
    {"pergunta": "O senhor(a) deseja discutir em juizo os descontos efetuados no seu benefício?", "opcoes": ["SIM", "NÃO"]}
]

st.title("📋 Questionário de Informações Essenciais")

# --- LOOP DAS PERGUNTAS ---
respostas = []
faltando_resposta = False

for idx, q in enumerate(questionario):
    st.subheader(f"{idx+1}. {q['pergunta']}")

    if len(q["opcoes"]) == 0:
        # Pergunta sem opções -> campo de texto livre
        resposta = st.text_input("Digite a resposta:", key=f"q{idx}")
    else:
        # Pergunta com opções -> radio button
        resposta = st.radio("Escolha uma opção:", q["opcoes"], key=f"q{idx}")

    # Checa se ficou vazio
    if not resposta.strip():
        faltando_resposta = True
    
    respostas.append((q["pergunta"], resposta))

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
    if faltando_resposta:
        st.warning("⚠️ Preencha TODAS as respostas antes de gerar o PDF!")
    else:
        pdf_file = gerar_pdf(respostas, anotacao)
        st.success("✅ PDF gerado com sucesso!")
        
        # Exibir botão para download
        with open(pdf_file, "rb") as f:
            st.download_button("⬇️ Baixar respostas em PDF", f, file_name="respostas_questionario.pdf")
