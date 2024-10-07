import requests
import streamlit as st
from pyhtml2pdf import converter
import base64
from PIL import Image
import numpy as np
import pdfkit
from streamlit import session_state as ss
from streamlit_pdf_viewer import pdf_viewer
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="🎈 Bon de CI",layout="wide")

logo = Image.open("img/logo_capstech.png")
st.session_state["tmp"] = []


listBoissons = ["CHAMPAGNE","VIN EFFERVESCENT","CREMANT","RATAFIA","MARC","VIN TRANQUILLE","PETILLANT AROMATISE A BASE DE VIN"]
listeCentilisations = [18.75,20,37.5,50,70,75,100,150,300,450,600,900,1200,1500]
listeCouleurs = ["VERT","BLEU","LIE DE VIN","BLANC","GRIS"]

def generate_site_liv():
    st.session_state["stage"] = "select_site_liv"


def finalise_bonci():
    st.session_state["stage"] = "finalise_bonci"
    # st.session_state["tmp"] = [st.session_state["comboBoisson"],st.session_state["comboCentili"],st.session_state["quantite"]]    
    # st.session_state["bonci"] = np.vstack([st.session_state["bonci"], st.session_state["tmp"]])
    disp_lines = np.vstack([st.session_state["bonci"]])
    df = pd.DataFrame(disp_lines)
    st.dataframe(df,
                 use_container_width=True,
                  column_config={
                    "0": st.column_config.TextColumn("Type de boisson",width='small'),
                    "1": st.column_config.TextColumn("Couleur du timbre",width='small'),
                    "2": st.column_config.TextColumn("Centilisation",width='small'),
                    "3": st.column_config.TextColumn("Quantité",width='small'),
                   })

def goto_product():
    st.session_state["stage"] = "add_product_line"

def add_product():
    if 'bonci' not in st.session_state:
        st.session_state["tmp"] = [st.session_state["comboBoisson"],st.session_state["comboCouleur"],st.session_state["comboCentili"],st.session_state["quantite"]]
        st.session_state["bonci"] = st.session_state["tmp"]
        # st.info("empty")
    else:
        st.session_state["tmp"] = [st.session_state["comboBoisson"],st.session_state["comboCouleur"],st.session_state["comboCentili"],st.session_state["quantite"]]    
        st.session_state["bonci"] = np.vstack([st.session_state["bonci"], st.session_state["tmp"]])
        # st.info("exist")
    # st.info(st.session_state["bonci"])
    # disp_lines = np.vstack([["Type boisson","Couleur du timbre","Centilisation"],st.session_state["bonci"]])
    disp_lines = np.vstack([st.session_state["bonci"]])
    df = pd.DataFrame(disp_lines)
    st.dataframe(df,
                 use_container_width=True,
                  column_config={
                    "0": st.column_config.TextColumn("Type de boisson",width='small'),
                    "1": st.column_config.TextColumn("Couleur du timbre",width='small'),
                    "2": st.column_config.TextColumn("Centilisation",width='small'),
                    "3": st.column_config.TextColumn("Quantité",width='small'),
                   })

def update_tmp_centi(val):
    st.session_state['tmp'][1]=val

def update_tmp_typeBoissons(val):
    st.session_state['tmp'][0]=val

def view_pdf():
    st.info("view pdf")
    st.write(st.session_state["bonci"] )

def send_bonci():
    st.info("send bon ci")

if "stage" not in st.session_state:
    st.session_state["stage"] = "select_site_liv"

if st.session_state["stage"] == "select_site_liv":
    with st.form("siteliv_form"):
        st.image(logo)
        st.write("Choississez l'adresse de livraison")
        submitted = st.form_submit_button(
            "Suivant", on_click=goto_product
        )

elif st.session_state["stage"] == "add_product_line":
    with st.form("product_form"):
        st.image(logo)
        comboBoisson = st.selectbox('Type de boisson',listBoissons,key="comboBoisson")
        comboCouleur = st.selectbox('Couleur du timbre',listeCouleurs,key="comboCouleur")
        comboCentili = st.selectbox('Centilisation',listeCentilisations,key="comboCentili")
        quantite = st.number_input(label='Quantité',format="%0d",step=1,key="quantite")
        btn1,btn2,btn3 = st.columns([1,1,1])
        submitted = btn1.form_submit_button("Ajouter un autre produit", on_click=add_product)
        submitted = btn2.form_submit_button("Finaliser", on_click=finalise_bonci)
        submitted = btn3.form_submit_button("Retour", on_click=generate_site_liv)
        st.session_state["tmp"] = [comboBoisson,comboCouleur,comboCentili,quantite]
        # st.info(st.session_state['tmp'])
        # if 'bonci' in st.session_state:
        #     st.info(st.session_state['bonci'])
        # if submitted:
        #      st.session_state["tmp"]=[comboBoisson,comboCentili,quantite]

elif st.session_state["stage"] == "finalise_bonci":
    with st.form("finalise_form"):
        st.image(logo)
        st.write("Que souhaitez-vous faire ?")
        btn1,btn2,btn3,btn4 = st.columns([1,1,1,1])

        submitted = btn1.form_submit_button("Envoyer le bon de ci", on_click=send_bonci)
        submitted = btn2.form_submit_button("Visualiser le pdf", on_click=view_pdf)
        submitted = btn3.form_submit_button("Quitter", on_click=generate_site_liv)
        submitted = btn4.form_submit_button("Retour", on_click=add_product)

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
      img_to_bytes(img_path)
    )
    return img_html


# intro_markdown = '''
#   <p align="center">Bon de commande Capsules Représentatives de Droits</p> 
# <style>
#     .heatMap {
#         width: 70%;
#         text-align: center;
        
#     }
#     .heatMap th {
#         background: white;
#         word-wrap: break-word;
#         text-align: center;
#          border:none
#     }
#      .heatMap td {border:none;font-size:12px;}
#     .heatMap tr:nth-child(1) { background: white; border:none }
#     .heatMap tr:nth-child(2) { background: white; border:none }
#     .heatMap tr:nth-child(3) { background: hite;  border:none}
# </style>

# <div class="heatMap">

# | <div style="width:190px"> Adresse du client</div> |<div style="width:390px"></div> |<div style="width:190px"> Adresse de livraison </div>|
# |------------------|--------------------------|--------------------|
# |adresse client ligne1|                       | ligne adresse livraison1|
# |adresse client ligne2|                       | ligne adresse livraison1|
# |adresse client ligne3|                       | ligne adresse livraison1|
# |adresse client ligne4|                       | ligne adresse livraison1|

# </div>

# | Type de boisson    | Couleur de timbre | Centilisation | quantité | Texte fiscal    |
# | ------------------ |:-----------------:| ------------- | -------- | --------------- |
# | CHAMPAGNE           | VERT              | 75 cl         | 23 000   | 51 RECOLTANT 01 |
# | CHAMPAGNE           | VERT              | 37,5 cl       | 23 000   | 51 RECOLTANT 01 |
# | CHAMPAGNE           | VERT              | 150 cl        | 23 000   | 51 RECOLTANT 01 |


# <div class="heatMap">

# | <div style="width:190px"> Visa du service local des douanes</div> |<div style="width:390px"></div> |<div style="width:190px"> Signature du client : </div>|
# |------------------|--------------------------|:--------------------|
# |                  |                          |Fait à : <br> Le : |

# </div>
# '''
# st.markdown(f'{img_to_html("img/logo_capstech.png")} {intro_markdown}' , unsafe_allow_html=True)

# def readpdf(pdf_file):
#     with open(pdf_file, "rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode('utf-8')
#         pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
#     return pdf_display


# if st.button("Print"):
#     pdf_file = "download.pdf"
#     converter.convert('https://gaston.caps-tech.com/bonci/397/1', pdf_file, print_options={"landscape": True} )
#     pdf_display = readpdf(pdf_file)
#     st.info('Successful finished. See PDF below.')
#     st.markdown(pdf_display, unsafe_allow_html=True)

# def html2pdf(url, pdf_file):
#     pdfkit.from_url(url, pdf_file)


# # st.balloons()
# if st.button('request'):
#         url = "https://gaston.caps-tech.com/bonci/398/1/1"
#         client=397
#         sitecli=1
#         output = "bonci.pdf"
#         st.info(f'Download and render pdf from url: {url}')
#         st.info('sending request, please wait...')

#         filename = Path(output)
#         #response = requests.get(f'https://gaston.caps-tech.com/bonci/download')
#         response = requests.get(url)
#         with open('/tmp/metadata.pdf', 'wb') as f:
#             filename.write_bytes(response.content)
#         pdf_display = readpdf(filename)
#         st.markdown(pdf_display, unsafe_allow_html=True)


# if st.button('download'):
#         output = "bonci.pdf"
#         st.info('sending request, please wait...')
#         filename = Path('metadata.pdf')
#         response = requests.get(f'https://gaston.caps-tech.com/bonci/download')
#         with open('/tmp/metadata.pdf', 'wb') as f:
#             filename.write_bytes(response.content)
#         pdf_display = readpdf(filename)
#         st.markdown(pdf_display, unsafe_allow_html=True)


# if st.button('pdfkit'):
#     # URL to fetch
#     url = "https://gaston.caps-tech.com/bonci/397/1"
#     # PDF path to save
#     pdf_path = 'example.pdf'
#     pdfkit.from_url(url, pdf_path)
#     # Declare variable.

# if 'pdf_ref' not in ss:
#     ss.pdf_ref = None


# # Access the uploaded ref via a key.
# st.file_uploader("Upload PDF file", type=('pdf'), key='pdf')

# if ss.pdf:
#     ss.pdf_ref = ss.pdf  # backup

# # Now you can access "pdf_ref" anywhere in your app.
# if ss.pdf_ref:
#     binary_data = ss.pdf_ref.getvalue()
#     pdf_viewer(input=binary_data, width=700)

# # Start a form
# listBoissons = ["CHAMPAGNE","VIN EFFERVESCENT","CREMANT","RATAFIA","MARC","VIN TRANQUILLE","PETILLANT AROMATISE A BASE DE VIN"]
# listeCentilisations = [18.75,20,37.5,50,70,75,100,150,300,450,600,900,1200,1500]
# with st.form(key='my_form'):
#     text_input = st.text_input(label='Enter some text')
#     comboBoisson = st.selectbox('Type de boisson',listBoissons,key="comboBoisson")
#     comboCentili = st.selectbox('Centilisation',listeCentilisations,key="comboCentili")
#     quantite = st.number_input(label='Quantité',format="%0d",step=1)
#     submit_button = st.form_submit_button(label='Submit')

# # Do something with the submitted data
# if submit_button:
#     st.write('You entered:', text_input)