import streamlit as st
from fpdf import FPDF
import tempfile
import os

# --- CONFIGURAÇÃO DO QUESTIONÁRIO ---
questionario = [
    {"pergunta": "Nome completo do cliente?", "tipo": "texto"},
    {"pergunta": "Qual seu CPF?", "tipo": "cpf"},
    {"pergunta": "Qual seu RG?", "tipo": "texto"},  # <-- Agora é campo de texto livre
    {"pergunta": "Qual seu estado Cívil? Ex: Solteiro, Casado, etc.", 
     "tipo": "opcoes", "opcoes": ["CASADO(A)", "SOLTEIRO(A)", "DIVORCIADO(A)", "VIÚVO(A)", "UNIÃO ESTÁVEL", "OUTROS"]},
    {"pergunta": "Qual seu endereço completo com CEP?", "tipo": "texto"},
    {"pergunta": "Qual sua profissão?", "tipo": "texto"},
    {"pergunta": "O senhor(a) recebeu algum cartão?", "tipo": "opcoes", "opcoes": ["SIM", "NÃO", "TALVEZ"]},
    {"pergunta": "Em caso afirmativo, o senhor(a) faz uso?", "tipo": "opcoes", "opcoes": ["SIM", "NÃO", "TALVEZ"]},
    {"pergunta": "O senhor(a) desbloqueou o cartão?", "tipo": "opcoes", "opcoes": ["SIM", "NÃO", "TALVEZ"]},
    {"pergunta": "O senhor(a) sabe se possui algum cartão vinculado no seu benefício?", "tipo": "opcoes", "opcoes": ["SIM", "NÃO", "TALVEZ"]},
    {"pergunta": "O senhor(a) recebeu algum valor em alguma de suas contas?", "tipo": "opcoes", "opcoes": ["SIM", "NÃO", "TALVEZ"]},
    {"pergunta": "O senhor(a) recebe faturas desse cartão?", "tipo": "opcoes", "opcoes": ["SIM", "NÃO", "TALVEZ"]},
    {"pergunta": "O senhor(a) chegou a pagar alguma fatura ou somente por meio dos descontos?", "tipo": "texto"},
    {"pergunta": "O senhor(a) possui ação judicial sobre esse assunto com outro advogado?", "tipo": "opcoes", "opcoes": ["SIM", "NÃO", "TALVEZ"]},
    {"pergunta": "O senhor(a) deseja discutir em juizo os descontos efetuados no seu benefício?", "tipo": "opcoes", "opcoes": ["SIM", "NÃO"]}
]

st.title("📋 Questionário de Informações Essenciais")

respostas = []

for idx, q in enumerate(questionario):
    st.subheader(f"{idx+1}. {q['pergunta']}")
    
    if q["tipo"] == "texto":
        resposta = st.text_input("Digite a resposta:", key=f"q{idx}")
    
    elif q["tipo"] == "cpf":
        entrada = st.text_input("Digite apenas números (11 dígitos):", key=f"q{idx}")
        if entrada and not entrada.isdigit():
            st.error("⚠️ CPF deve conter apenas números!")
            resposta = ""
        elif entrada and len(entrada) != 11:
            st.error("⚠️ CPF deve ter exatamente **11 números**!")
            resposta = ""
        else:
            resposta = entrada

    elif q["tipo"] == "opcoes":
        opcoes = ["-- Selecione --"] + q["opcoes"]
        resposta = st.selectbox("Escolha uma opção:", opcoes, key=f"q{idx}")

        if resposta == "-- Selecione --":
            resposta = ""

        if resposta == "OUTROS":
            resposta_outros = st.text_input("Especifique:", key=f"extra_{idx}")
            if resposta_outros.strip():
                resposta = resposta_outros
    else:
        resposta = ""
    
    respostas.append((q["pergunta"], resposta))

st.write("---")

# --- FUNÇÃO PARA GERAR PDF ---
def gerar_pdf(lista_respostas):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Respostas do Questionário", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    for i, (pergunta, resposta) in enumerate(lista_respostas, start=1):
        pdf.multi_cell(0, 10, f"{i}. {pergunta}\nResposta: {resposta}")
        pdf.ln(5)

    temp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(temp_dir, "respostas_questionario.pdf")
    pdf.output(pdf_path)
    return pdf_path

# --- BOTÃO PARA FINALIZAR ---
if st.button("📄 Gerar PDF das respostas"):
    faltando = [pergunta for pergunta, resposta in respostas if resposta.strip() == ""]
    
    if faltando:
        st.error("⚠️ Você precisa responder **todas as perguntas obrigatórias** antes de gerar o PDF!")
        st.warning("Perguntas sem resposta:\n" + "\n".join([f"- {p}" for p in faltando]))
    else:
        pdf_file = gerar_pdf(respostas)
        st.success("✅ PDF gerado com sucesso!")
        
        with open(pdf_file, "rb") as f:
            st.download_button("⬇️ Baixar respostas em PDF", f, file_name="respostas_questionario.pdf")

        st.balloons()
