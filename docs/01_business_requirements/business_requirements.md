# Exigences Métier (Business Requirements)
##  Exigences Fonctionnelles

### Question 1: Evaluation de la performance commerciale et financière des offres
#### Question Métier

Quelles offres télécoms présentent les meilleures performances commerciales et financières, et lesquelles méritent des ajustements pour améliorer leur attractivité et rentabilité?

#### 1. Description
- Evaluer les perforamncas commerciales et financières des differentes offres télécoms afin d'identifier celles qui génèent le plus de revenus, atirent le plus de clients et présentent le meilleur niveau d'adoption.
- Déterminer les offres à privilégier dans les campagnes marketing
- Identifier les offres dont les caracteristiques (bénéfices, facturations, durée de validité)  méritent d'être revues
- Identifier les offres qui pouraient être retirées du catalogue
- Comparer les offres selon
    1. leur contribution financière (chiffres d'affaires généré )
    2. leur attractivité commerciale (nombres de clients acheteurs distincts & Taux de pénétration dans la base des clients actifs)
    
#### 2. Utilisateurs / Départements / Equipes / Parties Prenantes

- Département Marketing
- Dépatement Commercial

#### 3. KPIs

KPI n°| Dimension évaluée/mesurée | KPI | Formule / Description |
---------|-----------------------|--------|--------|
1 | Performance financière de chaque offre | Chiffre d'affaires généré par chaque offre | Somme des montants de tous les achats de l'offre effectués pendant la période d'analyse |
2 | Attractivité commerciale e chaque offre | Nombre de clients acheteurs distincts de chaque offre | Nombre de clients distincts ayant acheté l'offre au moins une fois pendant la période d'analyse |
3 | Adoption de chaque offre | Taux de pénétation de chaque offre | (Nombre de clients distincts ayant acheté l'offre au moins une fois pendant la période d'analyse)  / ( Nombre total de clients actifs pendant la période d'analyse) |
4 | Dynamique Commerciale de chaque offre | Nombre d'achats de chaque offre | Nombre total d'achats de l'offre effectués pendant la période d'analyse |

#### 4. Axes d'Analyse
- Analyse par
    - offre commerciale: par ex DATA100, DATA200, etc.
    - type d'offre: DATA, MOBILE, BUNDLE
    - catégorie d'offre: INTERNET, MAXI
- Période d'analyse: Mensuelle, trimestrielle, anuelle, personnalisée


#### 5. Règles Métiers
1. Un client actif est un client possédant au moins un numéro téléphonique actif pendant la période d'analyse considérée

### Question 2: Quels segments de clients génèrent le plus de revenus à travers leurs achats d'offres télécoms?

#### 1. Description
- Comparer les différents segments de clients sur la base de leur contribution au chiffre d'affaires de ventes d'offres télécoms de l'opérateur
- Concentrer les efforts commerciaux sur les segments les plus contributifs
- Identiier les segments présentant un potentiel de développement commercial

#### 2. Utilisateurs / Départements / Equipes / Parties Prenantes

- Département Commercial
- Département Marketing

#### 3. KPIs

KPI n°| Dimension évaluée/mesurée | KPI | Formule / Description |
---------|-----------------------|--------|--------|
1 | Performance financière globale | Chiffre d'affaires issus des ventes des offres télécoms | Somme de tous les montants correspondants aux achats d'offres télécoms pendant la période d'analyse |
2 | Contribution financière de chaque segment | chiffre d'affaires total généré  par chaque segment | Somme de tous les prix correspondants aux achats d'offres télécoms effectués par le segment |
3 | Contribution financière de chaque segment | contribution du segment au chiffre d'affaires télécom  de l'opérateur | (Somme de tous les prix corresspondants aux achats d'offres télécoms effectués par les clients du segment) / (Chiffres d'affaires des offres télécoms) |
4 | Valeur client de chaque segment | chiffre d'affaires moyen généré par les clients actifs du segment | (Somme de tous les prix correspondants aux achats d'offres télécoms effectués par les clients du segment) / (Nombre total de clients actifs du segment) |

#### 4. Axes d'Analyse
- Analyse par:
    - segment de clients: PREMIUM, YOUTH, SME, STANDARS
    - type de client: INDIVIDUAL, BUSINESS
- Période d'analyse: Mensuelle, trimestrielle, anuelle, personnalisée

#### 5. Règles Métiers

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

KPI n°| Dimension évaluée/mesurée | KPI | Formule / Description |
---------|-----------------------|--------|--------|
1 | - | Taux global de consommation des bénéfices pour les offres MAXI | (Somme des équivalents en FCFA consommés pour tous les services utilisés) / (Somme des valeurs totales en FCFA accordées) |
2 | - | Taux global de consommation des bénéfices pour les offres INTERNET | (Somme des MB consommés ) / (Somme des MB accordés) |
3 |- | Contribution de la consommation Data à la consommation globale (Uniquement pour les offres BUNDLE) | (Somme des équivalents FCFA des MB consommés) / (Somme des valeurs totales en FCFA accordées) |
4 | - | Contribution de la consommation d'appels à la consommation globale (Uniquement pour les offres MAXI) | (Somme des équivalents FCFA des appels effectués) / (Somme des valeurs totales en FCFA accordées) |
5 | - | Contribution de la consommation de SMS à la consommation globale (Uniquement pour les offres BUNDLE) | (Somme des équivalents FCFA des SMS envoyés) / (Somme des valeurs totales en FCFA accordées) |
    
#### 4. Axes d'Analyse
- Analyse par
    - offre commerciale: par ex DATA100, DATA200, etc.
    - type d'offre: DATA, MOBILE, BUNDLE
    - catégorie d'offre: INTERNET, MAXI
- Période d'analyse: Mensuelle, trimestrielle, anuelle, personnalisée

#### 5. Règles Métiers

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

KPI n°| Dimension évaluée/mesurée | KPI | Formule / Description |
---------|-----------------------|--------|--------|
1 | - | Taux de croissance des clients actifs par région | (Nombre de clients actifs dans la région pendant la période actuelle - Nombre de clients actifs dans la région pendant période précédente) / ombre de clients actifs dans la région pendant période précédente |
2 | - | Taux de croissance des achats par région | (Nombre d'achats effectués dans la région  au cours de la période actuelle - Nombre d'achats effectués dans la région au cours de la période précédente) / Nombre d'achats effectués dans la région au cours de la période précédente |
3 | - | Taux de croissance du chiffre d'affaires par région | (Chiffre d'affaires de la région durant la période actuelle - Chiffre d'affaires de la région durant la période précédente) / Chiffre d'affaires de la région durant la période précédente |
4 | - | Chiffre d'affaires moyen généré par client actif par région | (Chiffre d'affaires généré par la région) / Nombre total de clients actifs dans la région |

[!!!Prendre la photo de la page ou jai demontre la formule , pis linserer pkus tart icic]

#### 4. Axes d'Analyse
- Analyse par:
    - ville: Covè, Abomey, Cotonou, Porto-Novo, etc
    - département: Zou, Littoral, Ouémé, etc
- Période d'analyse:
    - Analyse Mensuelle, trimestrielle, anuelle, personnalisée
    - Analyse comparative de deux périodes conséutives
    - Ex:
        - Septembre 2026 vs Octobre 2026
        - Trimestre 2 2026 vs Trimestre 3 2026
        - 2025 vs 2026

#### 5. Règles Métiers

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
KPI n°| Dimension évaluée/mesurée | KPI | Formule / Description |
---------|-----------------------|--------|--------|
1 | - | L'évolution du nombre d'achats effectués par le client | (Nombre d'achat effectués par le client pendant la période actuelle - Nombre d'achats effectués par le client pendant période précédente) / Nombre d'achats effectués par le client pendant période précédente |
2 | - | L'évolution de la consommation DATA par le client | (Quantité de MB consommés par le client pendant la période actuelle - Quantité de MB consommés par le client pendant la période précédente) / Quantité de MB consommés par le client pendant la période précédente |
3 | - | L'évolution de la consommation CALL par le client | (Nombre total de secondes des appels effectués par le client pendant la période actuelle - Nombre total de secondes des appels effectués par le client pendant la période précédente) / Quantité de MB consommés par le client pendant la période précédente |
4 | - | L'évolution de la consommation SMS par le client | (Nombre total de SMS envoyés par le client pendant la période actuelle - Nombre total de SMS envoyés par le client pendant la période précédente) / Nombre total de SMS envoyés par le client pendant la période précédente |
5 | - | Effectif des clients présentant des signes de baisse d'activité | Nombre total de clients présentant des signes de baisse d'activité |
6 | - | Porcentage des clients présentant des signes de baisse d'activité | (Nombre total de clients présentant des signes de baisse d'activité) * 100 / Nombre total de clients actifs |

#### 4. Axes d'Analyse
- L'analyse se fera chaque premier du mois en prenant comme période actuelle du premier au dernier du mois précédent, et comme période précédente du premier au dernier du mois avant.

#### 5. Règles Métiers

1. Un client présentant un signe de baisse d'activité est un client présentant une baisse d'au mois 30% pour au moins deux des 4 KPI 1, 2, 3 et 4 entre les deux périodes considérées.


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