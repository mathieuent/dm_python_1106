import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def afficher_score_vs_membres(df: pd.DataFrame) -> plt.Figure:
    """Crée un graphique scatter Score vs Membres.

    :param df: Le DataFrame contenant les colonnes Score et Members.
    :return: La figure matplotlib générée.
    """
    # On crée la figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # On trace le nuage de points
    ax.scatter(df["Members"], df["Score"], alpha=0.3, s=5)

    # On ajoute les titres et labels
    ax.set_title("Score en fonction du nombre de membres")
    ax.set_xlabel("Nombre de membres")
    ax.set_ylabel("Score")

    plt.tight_layout()
    return fig

# Set the page configuration
st.set_page_config(
    page_title="Devoir maison - Master MIMO - 2026",
    page_icon=":python:",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("Devoir maison - Master MIMO - 2026")
st.subheader("Analyse de données sur les anime récupérés depuis myAnimeList")
st.write("Données récupérées sur Kaggle : https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset/")
st.write("par Mathieu Bouffé")

# Load the dataset
# 4.1 - Visualiser les jeux de données
df1 = pd.read_csv("data/anime-dataset-2023.csv")
df2 = pd.read_csv("data/anime-filtered.csv", na_values="Unknown")
st.write("## JDD 1 : Informations titre sur les anime")
st.dataframe(df1)
st.write("## JDD 2 : Données spécifiques à myAnimeList (MAL)")
st.dataframe(df2)

# 4.2 - Visualiser des indicateurs statistiques sur les données

st.write("## Indicateurs statistiques")

st.metric("Nombre d'anime", len(df2))
st.metric("Score moyen", f"{df2['Score'].mean():.2f}")
st.metric("Nombre de membres moyen suivant un anime", f"{df2['Members'].mean():.0f}")


# 4.3 - Interagir avec l'utilisateur pour lui fournir des informations sur les données

st.write("## Visualiser une moyenne")

numeric_columns = ['Score', 'Episodes', 'Ranked', 'Popularity', 'Members', 'Favorites', 'Watching', 'Completed', 'On-Hold', 'Dropped']
column = st.selectbox("Sélectionner une colonne", numeric_columns)

st.write(f"Vous avez sélectionné la colonne: {column}")
st.write(f"Moyenne de la colonne {column}: {df2[column].mean():.2f}")

st.write("## Top 10 anime")
critere = st.selectbox("Sélectionner un critère", ["Score", "Episodes", "Members", "Favorites"])

st.dataframe(df2.nlargest(10, critere)[["Name", critere]])

# 4.4 - Afficher un graphique avec st.pyplot
st.write("## Score en fonction du nombre de membres")
st.write("Les animé les plus suivis ont ils le meilleur score ?")

st.pyplot(afficher_score_vs_membres(df2))


# Autres, exploration de mes données, visualisations supplémentaires

st.write("## Voir la fiche d'un anime")

df_merged = df2.merge(
    df1[["anime_id",
         "Image URL",
         "Synopsis",
         "Status",
         "Scored By"]],
    on="anime_id",
    how="inner",
)

anime_name = st.selectbox("Sélectionner un anime", df2["Name"].sort_values())
row = df_merged[df_merged["Name"] == anime_name].iloc[0]

st.image(row["Image URL"], width=200) 
st.write(f"### {row['Name']}")
st.write(f"**Titre anglais :** {row['English name']} | **Titre japonais :** {row['Japanese name']}")
st.write(f"**Type :** {row['Type']} | **Épisodes :** {row['Episodes']} | **Statut :** {row['Status']}")
st.metric("Score", row["Score"])
st.metric("Membres", int(row["Members"]))
st.write(f"**Synopsis en anglais :** {row['Synopsis']}")


