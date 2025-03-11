# 🚀 Challenge 48 Heures DATA/DEV : Analyse des tweets clients d'Engie et paramétrage d'Agents IA 

## 📌 Présentation  
Ce projet vise à analyser les tweets relatifs à ENGIE afin d'extraire des indicateurs clés (KPI) et d'automatiser la gestion des réclamations via un agent IA basé sur **Gemini 1.5 Flash**.  

L'outil permet de :  
✅ Nettoyer et structurer les données Twitter.  
✅ Détecter le sentiment des tweets et catégoriser les problématiques.  
✅ Générer automatiquement des réponses et mesurer l'urgence des réclamations.  
✅ Visualiser les résultats grâce à une interface interactive Streamlit.  

---

## 🛠️ Méthodologie  

### 🔹 Pré-traitement des données  
1️⃣ **Suppression de la colonne `name`** du fichier CSV.  
2️⃣ **Nettoyage des tweets** pour retirer les caractères spéciaux.  
3️⃣ **Suppression des tweets publiés par ENGIE** pour éviter tout biais.  
4️⃣ **Fusion des tweets successifs** d’un même utilisateur dans un court laps de temps.  
5️⃣ **Réattribution des ID** pour faciliter le traitement.  

### 🔹 Indicateurs Clés de Performance (KPI)  
| KPI | Description |
|------|------------|
| **Heure** | Nombre de tweets par heure |
| **Date** | Formatage propre de la date |
| **Jour** | Nombre de tweets par jour |
| **Mois** | Nombre de tweets par mois |
| **Année** | Nombre de tweets par année |
| **Sentiment** | Classification : `Positif`, `Neutre`, `Négatif` |
| **Problématique** | Catégorie de réclamation (ex. : `Problèmes de facturation`, `Pannes`, etc.) |
| **Score** | Score d’inconfort (0 à 100%) |
| **Urgence** | Niveau d’urgence du tweet |
| **Réponse automatique** | Message généré automatiquement |
| **Lieu** | Localisation si mentionnée |
| **Réparabilité** | Score de réparabilité (1 à 5) |
| **Solution** | Proposition de solution possible |
| **Type** | Nature du tweet (`Plainte`, `Question`, `Positif`) |

---

## 🤖 Processus de Création de l’Agent IA  

Nous avons utilisé **Gemini 1.5 Flash** pour analyser et classer les tweets.  

### 🔹 Détection des types de réclamations  
L'agent a été entraîné avec un **prompt détaillé** spécifiant les types de réclamations à identifier.  

### 🔹 Prompt et Fine-Tuning  
Un **pré-prompt** détaillé est fourni à l’agent, incluant des instructions sur :  
- L'interprétation des tweets.  
- La classification des sentiments et des problématiques.  
- La génération des réponses automatiques.  

📌 *Pré-prompt :*  
> `Tu es un agent chargé d'analyser des tweets mentionnant le compte de Engie.
> Il te sera fourni le commentaire d'un utilisateur.
> Ton rôle sera d'identifier et de renvoyer 9 facteurs :
> - "Sentiment" : Qui peut être :  "Positif" , "Neutre" ou "Négatif". 
> Ce facteur doit identifier le sentiment du commentaire et renvoyer l'une des 3 possibilités ("Positif" , "Neutre" ou "Négatif"). L'utilisateur est positif quand il est engoué par un projet Engie, quand il est content d'un service ou d'un changement. Toutes les plaintes, réclamations, mécontentement sont négatifs.
> - "Problématique" : "Problèmes de facturation", "Pannes et urgences","Service client injoignable", "Problèmes avec l’application", "Délai d’intervention" ou "aucune". Ce facteur doit identifier le type de problème que rencontre le client et renvoyer l'une des 5 possibilités. Voici à quoi correspondent ces 5 possibilités : 
> Problèmes de facturation : erreurs de montant, prélèvements injustifiés.
> Pannes et urgences : absence de gaz, d’électricité, problème d’eau chaude.
> Service client injoignable : absence de réponse, relances infructueuses.
> Problèmes avec l’application : bugs, indisponibilité du service.
> Délai d’intervention : retards dans la gestion des dossiers ou des réparations.
aucune : l'utilisateur n'a pas de problème.
> - "Score" : Calculer un score d’inconfort entre 0 et 100% pour le client. (0 n’a aucune conséquence pour le client, et 100 est un problème majeur qui le met en danger.)
> - "Urgence" : Mesure l'urgence de la situation pour l’entreprise de 0 à 10. (0 est une situation sans conséquence, 10 peut avoir des répercussions graves sur l’entreprise).
> - "Réponse automatique" : Génère une réponse automatique au tweet. La réponse engage Engie et devra donc être respectueuse. En cas de problème, cette réponse doit s'excuser et proposer une solution si cela est possible (comme contacter le support Engie au 09 74 73 54 01). Remercier l'utilisateur s'il est content du service. Tu peux t'adapter à la situation. 
> - "Lieu" : Si le lieu est mentionné, remplir cet emplacement avec le lieu concerné par le tweet, sinon laisser nul. 
> - "Réparabilité" : Une valeur de 0 (pas de panne) à 5 (panne très coûteuse ou complexe à résoudre). 
> - "Solution" : Proposer une solution éventuelle en une ligne que l'entreprise pourrait réaliser pour résoudre le problème. 
> - "Type" : Identifier le type de tweet :"Positif" : l'utilisateur est content du service que propose Engie, des ces engagements ou de ce que Engie organise. “Plainte" : l'utilisateur se plaint d'un problème."Question : l'utilisateur pose une question. 
> 
> Voici le message utilisateur : `  

### 🔹 Exemples d’interactions  
> ![Image d'exemple d'intéraction avec l'agent](images/Interaction.png)

---

## 🏗️ Structure de l'Outil  

L’outil est divisé en **deux fichiers principaux** :  

### 📌 **1. a.ipynb** (Notebook de traitement des données)  
🟢 **Importation & Nettoyage des Données**  
- Chargement du fichier `filtered_tweets_engie.csv`  
- Suppression des colonnes inutiles et nettoyage des caractères spéciaux  

🟢 **Création des KPI**  
- Extraction des indicateurs : heure, jour, mois, année  
- Comptage des mentions pour chaque compte ENGIE (`ENGIEgroup`, `ENGIEpartFR`, `ENGIEpartSAV`)  

🟢 **Intégration de l’IA (Gemini 1.5 Flash)**  
- Création des colonnes : `Sentiment`, `Problématique`, `Score`, `Urgence`, `Réponse automatique`, `Lieu`, `Réparabilité`, `Solution`, `Type`  
- Génération du fichier `filtered_tweets_engie_cleaned.csv` contenant les nouvelles données enrichies  

### 📌 **2. streamlit.py** (Interface utilisateur)  
Ce fichier gère **l’affichage des données** via des **graphiques interactifs et des filtres**.  

---

## 📥 Installation  

### 1️⃣ **Prérequis**  
Assurez-vous d’avoir une **version récente de Python** installée :  
🔗 [Télécharger Python](https://www.python.org/downloads/)  

### 2️⃣ **Installation des dépendances**  
Exécutez les commandes suivantes pour installer les librairies requises :  

```bash
# Manipulation des données
pip install pandas 

# Librairies Google pour l’IA Gemini
pip install google.ai.generativelanguage
pip install google.generativeai

# Visualisation des données avec Streamlit, Plotly et Openpyxl
pip install streamlit
pip install plotly 
pip install openpyxl
```

---

## 🎯 Utilisation

### 1️⃣ Exécuter le notebook Jupyter (a.ipynb)

Ouvrir a.ipynb dans Jupyter Notebook ou VS Code
Exécuter les cellules pour traiter et analyser les tweets
Un fichier nettoyé filtered_tweets_engie_cleaned.csv sera généré

### 2️⃣ Lancer l’interface Streamlit (streamlit.py)

```bash
streamlit run streamlit.py
```

Une interface s’ouvrira dans votre navigateur avec des graphiques et filtres interactifs

## 📌 Auteurs
📍 BEN YOUSSEF Sajed
📍 CAMARA Djibril
📍 LIENARD Mathieu
📍 DUMET Ludovic
📍 SOUBRAMANIEN Baayvin
