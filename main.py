import requests
import streamlit as st
import json

# https://discuss.streamlit.io/t/version-0-64-0-deprecation-warning-for-st-file-uploader-decoding/4465
st.set_option("deprecation.showfileUploaderEncoding", False)

# defines an h1 header
st.title("Recommandation de contenu")

# ******************************************** Gestion des articles **********************************************

# displays a file uploader widget
articleSrc = st.sidebar.file_uploader("Sélectionner un fichier article")
if st.sidebar.button("Mise à jour des articles"):
        if articleSrc is not None:
            fileArt = {"file": articleSrc.getvalue()}
            resArt = requests.post(f"https://reco-func.azurewebsites.net/api/articles-sav", files=fileArt)
            st.sidebar.markdown(resArt.content)

# ******************************************** Gestion des consultations d'articles **********************************************

# displays a file uploader widget
usersSrc = st.sidebar.file_uploader("Sélectionner un fichier des utilisateurs")
if st.sidebar.button("Mise à jour des utilisateurs"):
    if usersSrc is not None:
        fileUser = {"file": articleSrc.getvalue()}
        resUser = requests.post(f"https://reco-func.azurewebsites.net/api/users-sav", files=fileUser)
        st.sidebar.markdown(resUser.content)

# ******************************************** Gestion de l'entrainement **********************************************

# displays a file uploader widget
if st.button("Entrainement du modèle"):
    resUser = requests.post(f"https://reco-func.azurewebsites.net/api/train")
    st.markdown('Entraînement terminé avec succès')

# ******************************************** Gestion des utilisateurs **********************************************


resListUsers = requests.get(f"https://oc9recommandation.azurewebsites.net/users")
lstUsers = json.loads(resListUsers.content)
outputUser = st.selectbox("Choix de l''utilisateur", lstUsers)

# ******************************************** Gestion des prédictions **********************************************

topN = st.number_input("Nombre d'articles à afficher", 1, 10, 5, 1, "%i")
if st.button("Prédiction du modèle"):
    requestBody = '{"userId":' + str(outputUser) + ' , "topN":' + str(topN) + '}'
    resPredict = requests.post(f"https://reco-func.azurewebsites.net/api/predict", data=requestBody)
    st.json(resPredict.json())