#import pyautogui
import streamlit as st
from urllib.parse import quote
import webbrowser
from time import sleep
from io import StringIO
import pandas as pd

st.set_page_config(page_title="Automação Whatsapp", layout='wide')

# titulo
st.markdown("<h1 style='text-align: center; color: green;'>Automação WhatsApp</h1>", unsafe_allow_html=True)

texto = st.text_input("Informe a mensagem a ser enviada:", max_chars=100)
contatos = st.text_input("Informe a Lista de contatos:", max_chars=100)
uploaded_file = st.file_uploader("Importe a Lista de Contatos")
mensagem = ''
lista_contatos = ''
import_contatos = ''

# Importa o arquivo de contatos
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()

    df = pd.read_csv(uploaded_file)

    import_contatos = df['name'].unique()

    import_contatos = import_contatos.tolist()

# Tratamento dos inputs
if len(texto) > 0:
    mensagem = texto

if len(contatos) > 0:
    contatos = contatos.replace('  ', ' ')
    lista_contatos = contatos.split(", ")

if st.button('Iniciar Automação'):
    if len(lista_contatos) > 0 and len(import_contatos) > 0:
        st.write("Não é possivel inserir a lista de contatos e importar uma lista com contatos. Escolha apenas uma opção!")
    elif len(mensagem) == 0 or len(lista_contatos) == 0 and len(import_contatos) == 0:
        st.write("Favor informar a mensagem e a lista de contatos!")
    elif len(mensagem) == 0:
        st.write("Favor informar a mensagem a ser enviada!")
    else:
        st.write("Automação Iniciada")

    if len(contatos) == 0:
        lista_contatos = import_contatos

    for numero in lista_contatos:
        contato = numero

        link_mensagem_wpp = f'https://web.whatsapp.com/send?phone={contato}&text={quote(texto)}'
        webbrowser.open_new_tab(link_mensagem_wpp)
        sleep(5)
