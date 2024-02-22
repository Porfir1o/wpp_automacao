import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
from winotify import Notification
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


# verifica se foi importação via arquivo
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()

    df = pd.read_csv(uploaded_file)

    import_contatos = df['name'].unique()

    import_contatos = import_contatos.tolist()

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

        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)

        service = Service(ChromeDriverManager().install())
        nav = webdriver.Chrome(service=service, options=options)
        nav.get("https://web.whatsapp.com")
        time.sleep(30)

        # mensagem

        nav.find_element('xpath', '//*[@id="side"]/div[1]/div/div[2]/button/div[2]/span').click()
        nav.find_element('xpath', '// *[ @ id = "side"] / div[1] / div / div[2] / div[2] / div / div[1] / p').send_keys("You")
        time.sleep(2)
        nav.find_element('xpath', '// *[ @ id = "side"] / div[1] / div / div[2] / div[2] / div / div[1] / p').send_keys(Keys.ENTER)

        # Escrever a mensagem para nós mesmos
        
        nav.find_element('xpath','// *[ @ id = "main"] / footer / div[1] / div / span[2] / div / div[2] / div[1] / div / div[1] / p').send_keys(mensagem)
        time.sleep(2)
        nav.find_element('xpath', '// *[ @ id = "main"] / footer / div[1] / div / span[2] / div / div[2] / div[1] / div / div[1] / p').send_keys(Keys.ENTER)
        time.sleep(1)

        qtd_contatos = len(lista_contatos)

        if qtd_contatos % 5 == 0:
            qtde_blocos = qtd_contatos / 5
        else:
            qtde_blocos = int(qtd_contatos / 5) + 1

        for i in range(qtde_blocos):
            inicial = i * 5
            final = (i + 1) * 5
            lista_enviar = lista_contatos[inicial:final]

            # seleciona a mensagem que vai enviar e abre a caixa de emcaminhar

            lista_elementos = nav.find_elements('class name', '_2AOIt')

            for item in lista_elementos:
                mensagem = mensagem.replace("\n", "")
                texto = item.text.replace("\n", "")
                if mensagem in texto:
                    elemento = item
            
            ActionChains(nav).move_to_element(elemento).perform()
            elemento.find_element('class name', '_3u9t-').click()
            time.sleep(1)
            nav.find_element('xpath', '// *[ @ id = "app"] / div / span[5] / div / ul / div / li[4] / div').click()
            time.sleep(1)
            nav.find_element('xpath', '//*[@id="main"]/span[2]/div/button[4]/span').click()
            time.sleep(1)

            for nome in lista_enviar:
                # seleciona os 5 contatos para enviar
                
                nav.find_element('xpath', '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[1]/p').send_keys(nome)
                time.sleep(1.5)

                # Verifica se o destinário existe na lista de envio
                lista_elementos_user_not_found = nav.find_elements('class name', 'hp667wtd')

                user = ''

                for not_found in lista_elementos_user_not_found:
                    user = not_found.text.replace("\n", "")

                nav.find_element('xpath', '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[1]/p').send_keys(Keys.ENTER)
                time.sleep(1.5)

                if user == 'No chats, contacts or messages found':
                    nav.find_element('xpath', '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[1]/p').send_keys(Keys.CONTROL + "A")
                    nav.find_element('xpath', '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[1]/p').send_keys(Keys.BACKSPACE)
                    time.sleep(1.5)

                    st.write(f"Destinatário informado não existe na sua lista de contatos, favor verificar: {nome}")

                else:

                    nav.find_element('xpath', '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[1]/p').send_keys(Keys.BACKSPACE)
                    time.sleep(1.5)
            try:
                nav.find_element('xpath', '// *[ @ id = "app"] / div / span[2] / div / div / div / div / div / div / div / span / div / div / div').click()
                time.sleep(3)
            except:
                pass

        if user == 'No chats, contacts or messages found':
            try:
                nav.find_element('xpath', '// *[ @ id = "app"] / div / span[2] / div / div / div / div / div / div / div / header / div / div[1] / div').click()
            except:
                pass

            notificacao = Notification(app_id='Automação do Whatsapp',
                                       title='Notificação da Automação',
                                       msg='A Automação finalizou, porém existe destinatários que não foram encotrados. Verique os nomes na tela do sistema.',
                                       duration="long",
                                       icon="C:\\Users\\Porfirio\\PycharmProjects\\GUPPE\\wpp\\logo.png")
            notificacao.show()

        else:
            notificacao = Notification(app_id='Automação do Whatsapp',
                                       title='Notificação da Automação',
                                       msg='A Automação finalizou',
                                       duration="long",
                                       icon="C:\\Users\\Porfirio\\PycharmProjects\\GUPPE\\wpp\\logo.png")
            notificacao.show()
