# Inventaire des Sources de Données

|N°| Source Logique | Source Physique | Type/Format | Données|
|---|--------------|------------------|------------|-----------|
| 1.    | Système de Gestion du Catalogues d'Offres | BDD: ben_telecom Schéma: offers_catalog Tables: offers, offer_billings, offer_configurations | BDD Relationelle SGBD: PostgreSQL | Données sur différentes offres de communication tléphoniques |
| 2.    | CRM | BDD: ben_telecom Schéma: crm Table: customers | BDD Relationelle SGBD: PostgreSQL | Données sur les clients |
| 3.    | Système de Gestion des Souscriptions | BDD: ben_telecom Schéma: subscriptions Tables: subscriptions | BDD Relationelle SGBD: PostgreSQL | Données sur les lignes téléphoniques des clients |
| 4.    | Système de Gestion des Recharges et des Achats | Dossier de Fichiers | Fichiers Parquet géréré au quotidien | Données sur les achats des différentes offres de communication téléphonique |
| 5.    | Système de Médiation d'Usage | Kafka | JSON Topic: TelecomUsage | Données d'usage des services téléphoniques DATA, VOICE et SMS |

[Notebook pour identifier les sources](../notebooks/data_sources_analysis/01_data_sources_identification.ipynb)
