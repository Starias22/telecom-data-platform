# Exigences Métier (Business Requirements)
##  Exigences Fonctionnelles

### Question 1: Quelles offres présentent les meilleures performances commerciales et financières, et lesquelles méritent des ajustements?
#### 1. Description

- Déterminer les offres à privilégier dans les campagnes marketing
- Identifier les offres dont les caracteristiques (prix, bénéfices, facturations)  méritent d'être revues
- Identifier les offres qui pouraient être retirées du catalogue
- Comparer les offres selon
    1. leur contribution financière (chiffres d'affaires généré )
    2. leur attractivité commerciale (nombres de clients acheteurs distincts & Taux de pénétration dans la base des clients actifs)
    
#### 2. Utilisateurs / Départements / Equipes / Parties Prenantes

- Département Marketing

#### 3. KPIs
Pour chaque offre X:
1. Le chiffre d'affaires généré par l'offre:

Somme des montants de tous les achats de l'offre X pendant la période sélectionnée

2. Le nombre de clients acheteurs (distincts) de l'offre

Nombre de clients distincts ayant acheté l'offre X au moins une fois pendant la période sélectionnée

3. Le taux de pénétration de l'offre dans la base des clients actifs

(Nombre de clients distincts ayant acheté l'offre X au moins une fois pendant la période sélectionnée)  / ( Nombre total de clients actifs pendant la période sélectionnée)

#### 4. Règles Métiers
1. Un client actif est un client possédant au moins un numéro téléphonique actif pendant la période d'activité considérée
2. Les offres sont comparées individuellemnt au sein de leur categories respectives (DATA, MOBILE, BUNDLE), afin d'évaluer leurs performances commerciales sans comparer directement des offres répondant à des besoins différents

### Question 2: Quels segments de clients génèrent le plus de revenus à travers leurs achats d'offres télécoms?

#### 1. Description
- Comparer les différents segments de clients sur la base de leur contribution au chiffre d'affaires de ventes d'offres télécoms de l'opérateur
- Concentrer les efforts commerciaux sur les segments les plus contributifs
- Identiier les segments présentant un potentiel de développement commercial

#### 2. Utilisateurs / Départements / Equipes / Parties Prenantes

- Département Commercial
- Département Marketing

#### 3. KPIs
1. Chiffres d'affaires issus des ventes des offres télécoms:

Somme de tous les prix correspondants aux achats d'offres télécoms

2. Pour chaque segment X, le chiffre d'affaires total généré  par le segment via ses achat d'offres télécoms

(Somme de tous les prix correspondants aux achats d'offres télécoms effectués par le segment)

3. Pour chaque segment X, la contribution du segment au chiffre d'affaires télécom  de l'opérateur

    (Somme de tous les prix corresspondants aux achats d'offres télécoms effectués par les clients du segment) / (Chiffres d'affaires des offres télécoms)

4. Pour chaque segment X, le chiffre d'affaires moyen généré par les clients actifs du segment via leurs achats télécom:

(Somme de tous les prix correspondants aux achats d'offres télécoms effectués par les clients du segment) / (Nombre total de clients actifs du segment)

#### 4. Règles Métiers

1. Les revenus analysés correspondent exclusivement aux achats d'offres télécoms
2. Chaque achat est attribué au segment auquel appartient le client au moment de l'achat
3. Le chiffre d'affaires moyen par client actif est calculé sur l'ensemble des clients actifs du segment durant la periode danalyse, y compris ceux n'ayant effectué aucun achat pendant la période considérée.

### Question 3: Les clients consomment-ils effectivement les bénéfices et services inclus dans les offres qu'ils achètent?

#### 1. Description
- Comparer les volumes bénéficiés aux volumes réellement consommés globalement et spécifiquement concernant chacun des services bénéficiés (DATA, CALL, SMS)
- Permettre de voir si certains bénéfices/services inclus dans les bénéfices sont sous-utliisés
- Fournir des éléments d'aide a la décision pour la création de nouvelles offres, l'ajustement des offres existantes ou le retrait de certaines offres du catalogue

#### 2. Utilisateurs / Départements / Equipes / Parties Prenantes

- Département Produits

#### 3. KPIs

1. Taux global de consommation des bénéfices:
    
    - Pour les offres Maxi:
    
    (Somme des équivalents en FCFA consommés pour tous les services utilisés) / (Somme des valeurs totales en FCFA accordées) 

    - Pour les offres Internet:

    (Somme des MB consommés ) / (Somme des MB accordés)

2. Contribution de la consommation Data à la consommation globale (Uniquement pour les offres BUNDLE)

(Somme des équivalents FCFA des MB consommés) / (Somme des valeurs totales en FCFA accordées)

3. Contribution de la consommation d'appels à la consommation globale (Uniquement pour les offres MAXI)

(Somme des équivalents FCFA des appels effectués) / (Somme des valeurs totales en FCFA accordées)

4. Contribution de la consommation de SMS à la consommation globale (Uniquement pour les offres BUNDLE)

(Somme des équivalents FCFA des SMS envoyés) / (Somme des valeurs totales en FCFA accordées)
    

#### 4. Règles Métiers


### Question 4: Comment évoluent les performances commerciales des différentes régions et quelles régions présentent des opportunités de développement commercial?
#### 1. Description

- Comparer les performances commerciales des différentes régions
- Suivre l'évolution du nombre de clients, des achats d'offres et du chiffre d'affaires par région
- Identifier les régions présentant des opportunités de dévelopement commercial
- Orienter les actions commerciales et marketing en fonction des performances régionales

#### 2. Utilisateurs / Départements / Equipes / Parties Prenantes

- Direction commerciale
- Departement Marketing
- Direction génerale

#### 3. KPIs
1. Taux de croissance du nombre de clients actifs par région

(Nombre de clients actifs dans la région pendant la période actuelle - Nombre de clients actifs dans la région pendant période précédente) / ombre de clients actifs dans la région pendant période précédente

2. Taux de croissance du nombre d'achats par région

(Nombre d'achats effectués dans la région  au cours de la période actuelle - Nombre d'achats effectués dans la région au cours de la période précédente) / Nombre d'achats effectués dans la région au cours de la période précédente

3. Taux de croissance du chiffre d'affaires par région

(Chiffre d'affaires de la région durant la période actuelle - Chiffre d'affaires de la région durant la période précédente) / Chiffre d'affaires de la région durant la période précédente

4. Chiffre d'affaires moyen généré par client actif par région

(Chiffre d'affaires généré par la région) / Nombre total de clients actifs dans la région

[!!!Prendre la photo de la page ou jai demontre la formule , pis linserer pkus tart icic]


### Question 5: Quels clients présentent actuellemt des signes de baisse d'activité? (Fidélisation/Retention)
#### 1. Description
- Identifier les clients dont l'activité commerciale et la consommation des services télécoms diminuent
- Déterminer les changements de comportement pouvant indiquer un risque de désengagment
- Permettre aux équipes commerciales et de retention de mettre en place des actions de fidélisation et de retention avant que ces clients concernés ne deviennent inactifs.

#### 2. Utilisateurs / Départements / Equipes / Parties Prenantes

- Equipe commerciale
- Equipe Marketing
- Equipe de fidélisation/retention

#### 3. KPIs
- Pour chaque client:
    - L'évolution du nombre d'achats effectués par le client sur chacune des périodes considérées (KPI 1)

    - L'évolution de la consommation des services DATA (KPI 2), CALL (KPI 3) et SMS (KPI 4) 
- Nombre (KPI 5) et pourcentage (KPI 6 ) de clients présentant des signes de baisse d'activité

#### 4. Règles métier
1. L'analyse se fera chaque premier du mois en prenant comme période actuelle du premier au dernier du mois précédent, et comme période précédente du premier au dernier du mois avant.
2. Un client présentant un signe de baisse d'activité est un client présentant une baisse d'au mois 30% pour au moins deux des 4 KPI 1, 2, 3 et 4 entre les deux périodes considérées.

### Granularité et Période/Fréquence d'analyse

Question Métier | Niveau de Granularité | Période d'analyse / Fréquence |
-----------------|-----------------------|---------------------------------|
Q1 - Performance commerciale des offres | Offre x Période | Mensuelle, trimestrielle, anuelle, personnalisée |
Q2 - Revenus par segment de clients | Segment x Période | Mensuelle, trimestrielle, anuelle, personnalisée |
Q3 - Consommation des bénéfices des offres | Offre x Période | Mensuelle, trimestrielle, anuelle, personnalisée |
Q4 - Performance commerciale régionale | Région x Période | Mensuelle, trimestrielle, anuelle, personnalisée |
Q5 - Détection de la baisse d'activité des clients | Client x Période | Analyse mensuelle automatisée, comparaison de deux périodes consécutives de 30 jours |

## Exigences Non Fonctionelles (y compris techniques)

1. **Scalabilité:** Supporter l'augmentation des volumes de données sans modification majeure de l'architecture
2. **Fraicheur des données:** Rendre les données disponibles dans les délais nécessaires aux analyses BI
3. **Performance:** Permettre l'exécution des requêtes analytiques et l'affichage des tableaux de bord dans un délai acceptable
4. **Qualité des Données:** Détecter et traiter les données incomplètes, invalides, incohérentes ou dupliquées
5. **Sécurité:**  Protéger les données contre les accès non autorisés
6. **Historisation:** Conserver l'historique nécessaire aux analyses temporelles et au suivi des évolutions
7. **Traçabilité:** Permettre de suivre l'origine, les transformations et le chargement des données
8. **Fiabilité:** Garantir que les traitements peuvent être repris après une erreur sans créer d'incohérence ou de doublons
9. **Maintenabilité:** Faciliter la modification, la correction et l'évolution des pipelines et des composants de la plateforme
10. **Disponibilité:** Garantir l'accès aux services critiques pendant les périodes prévues d'utliisation