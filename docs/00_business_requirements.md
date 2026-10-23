# Exigences Métier (Business Requirements)
##  Exigences Fonctionnelles

### Question 1: Quelles offres l'opérateur devrait-il promouvoir, repenser ou retirer du catalogue d'offres?
#### 1. Description
- Comparer les offres en terme
1. de performance financière
2. d'attraction ou d'adoption par les clients
3. de fidélisation et de satisfaction des clients (comment l'offre contribue à fideliser le client et à le satisfaire)
4. d'adéquation entre l'offre achetée et son utilisation
- Déterminer les offres à privilégier dans les campagnes marketing, celles à revoir (modifier ou ajuster les prix, bénéfices, facturation et autres) et celles à retirer du catalogue

#### 2. Utilisateurs / Départements / Equipes / Parties Prenantes

- Département Marketing, Responsable Marketing

#### 3. KPIs
Pour chaque offre X:
1. Le revenu généré par l'offre  (Pour mesurer la performance financière de l'offre):

Somme de tous les montants de tous les achats effectués par les clients avec leurs différentes lignes téléphoniques

2. Le taux d'achat de l'offre par les clients (Pour mesurer l'attractivité ou l'adoption de l'offre par les clients)

    (Nombre total de clients elligibles pour l'offre X ayant acheté loffre X au moins une fois) / (Nombre total de clients elligibles pour l'offre X)

3. Le taux de reachat de l'offre par les clients (Pour mesurer la fidélisation et de satisfaction des clients)

    (Nombre total de clients elligibles pour l'offre X ayant acheté loffre X au moins deux fois) / (Nombre total de clients elligibles pour l'offre X ayant acheté l'offre X au moins une fois)

4. Le taux de consommation des bénéfices de l'offre par les clients (Pour mesurer l'adéquation entre l'offre achetée et sa consommation)

    (Somme des bénéfices consommés en FCFA pour tous les achats) / (Somme des valeurs des bénéfices offerts en FCFA pour tous les achats)

#### 4. Fréquence
Mensuelle

#### 5. Données Nécessaires
1. Informations sur les clients
2. Les souscripions
3. Le catalogue des offres
4. Les achats effectués
4. Les données de consommation des bénéfices

#### 6. Règles métier
1. Un client elligible pour une offre X est un client possédant au moins un numéro téléphonique actif pendant la période d'activité considérée, et qui n'est exclut par aucune règle spécifique à l'offre X (par exemple anncienneté du client, segment du client, ...)

### Question 2: Quels segments de clients génèrent le plus de revenus?

#### 1. Description
- Comparer les différents segments de clients sur la base de leur contribution au chiffre d'affaire de l'opérateur
- Concentrer les efforts commerciaux sur les segments les plus rentables/contributifs

#### 2. Utilisateurs / Départements / Equipes / Parties Prenantes

- Département Commercial, Responsable Commercial

#### 3. KPIs
1. Revenu total de l'opérateur:

Somme de tous les prix corresspondants aux achats effectués par les clients

2. Pour chaque segment X, le revenu total généré  par le segment

(Somme de tous ls prix correspondants aux achats effectués par le segment)

3. Pour chaque segment X, la a cntribution du segment au chiffre d'affaires de l'opérateur

    (Somme de tous les prix corresspondants aux achats effectués par les clients du segment) / (Revenu toal de l'opérateur)

4. Pour chaque segment X, le revenu moyen généré par les client du segment:

(Revenu total généré par le segment) / (Nombre total de clients du segment)

#### 4. Fréquence
Mensuelle

#### 5. Données Nécessaires
1. Informations sur les clients
2. Les souscripions
3. Le catalogue des offres
4. Les achats effectués (pour tous les produits de l'opérateur)


#### 6. Règles métier
1. Les achats ici ne concernent pas uniquement les offres de communications téléphoniques (data, SMS, appel); ils concernent tous les produits commercialisés par l'opérateur, y compris les cartes SIM, pocket WIFI, téléphones portables, etc


### Question 3: Les clients consomment-ils effectivement les bénéfices et services inclus dans les offres qu'ils achètent?

#### 1. Description
- Comparer les volumes bénéficiés aux volumes réellement consommés globalement et spécifiquement concernant chacun des services bénéficiés (DATA, VOICE, SMS)
- Permettre de voir si certains bénéfices/services inclus dans les bénéfices sont sous-utliisés
- Creer de nouvelles offres, retirer des offres, ajuster les offfres, modiifer les offres?

#### 2. Utilisateurs / Départements / Equipes / Parties Prenantes

- Département Produits

#### 3. KPIs
- Pour les forfaits Internet:
    1. Taux de consommation Data = (Somme des volume MB consommés) / (Somme des volume MB accordés)

- Pour les forfaits Maxi sans Internet:

    2. Taux d'utilisation d'appels:
    
    (Somme des équivalents en FCFA des appels effectués) / (Somme des valeurs totales en FCFA accordées)

    3. Taux d'utilisation de SMS:
    
    (Sommme des équivalents en FCFA des SMS envoyés) / (Somme des Valeurs totales en FCFA accordées)

    4. Taux d'utilisation globale du forfait:
    
    (Somme des équivalents en FCFA consommés pour tous les services utlisés) / (Somme des valeurs totales en FCFA accordées)

- Pour les forfaits Maxi avec internet:

    5. Taux d'utilisation d'appels:
    
    (Somme des équivalents en FCFA des appels effectués) / (Somme des valeurs totales en FCFA accordées)

    6. Taux d'utilisation de SMS:
    
    (Somme des équivalents en FCFA des SMS envoyés) / (Somme des valeurs totales en FCFA accordées)

    7. Taux d'utilisation de Data
    
    (Somme des équivalents en FCFA des data consommés) / (Somme des valeurs totales en FCFA accordées)

    8. Taux d'utlisation globale du forfait:
     
     (Somme des équivalents en FCFA consommés pour tous les services utilisés) / (Somme des valeurs totales en FCFA accordées)

#### 4. Fréquence
Mensuelle

#### 5. Données Nécessaires
1. Le catalogue des offres
2. Les achats effectués
3. Les données de consommation

### Question 4: Quelles régions présentent-ils le plus fort potentiel de croissance?
#### 1. Description
- régions ou l'opérateur a encore le plus fort potentiel pour développer son activité
- Croissance = augmentation d'une activité dans le temps
- Par exemple les régions ou
    - il y a beaucoup de clients mais relativement peu d'achats
    - les revenus augmentent
    - le nombre de clients augmentent
    - la consommation des offres est forte
- Comparer les régions en terme de nombre de clients, de revenus générés, d'achats, de consommation, et ceci au fil du temps, pour mesurer la croissance de ces differentes métriques dans le temps pour chaque région

#### 2. Utilisateurs / Départements / Equipes / Parties Prenantes

- Direction génerale
- Direction commerciale
- Departement Marketing

#### 3. KPIs
1. Taux de croissance des clients par région

(Nombre de clients de la période précédente - Nombre de clients de la période actuelle) / Nombre de clients de la période précédente

2. Taux de croissance des achats par région
(Nombre d'achats effectués  au cours de la période précédente - Nombre d'achats effectués au cours de la période actuelle) / Nombre d'achats effectués  au cours de la période précédente
3. Taux de croissance des revenus par région
(Revenu de la période précédente - Revenu de la période actuelle) / Revenu de la période précédente

4. Revenu moyen généré par client dans chaque région

(Revenu généré par la région) / Nombre total de clients dans la région

[!!!Prendre la photo de la page ou jai demontre la formule , pis linserer pkus tart icic]

#### 4. Fréquence
Mensuelle

#### 5. Données Nécessaires
1. Les informations sur les clients y compris leur région
2. Les achats effectués


#### 6. Règles métier
1. ...


### Question 5: Quels clients présentent actuellemt des signes de baisse d'activité? (Fidélisation/Retention)
#### 1. Description
- Identifier les clients dont l'activité diminue afin que l'équipe commerciale/marketing/de fidélisation/retention puisse mettre en place des actions de retention avant qu'ils deviennent inactifs
- Les clients dont le nombre d'achats diminue et ceux qui utlisent de moins en moins les services (DATA, VOICE, SMS) de l'opérateur

#### 2. Utilisateurs / Départements / Equipes / Parties Prenantes

- Equipe commerciale
- Equipe Marketing
- Equipe de fidélisation/retention

#### 3. KPIs
- Pour chaque client:
    - L'évolution du nombre d'achats effectués par le client sur chacune des périodes considérées (KPI 1)
    - L'évolution de la consommation des services DATA (KPI 2), VOICE (KPI 3) et SMS (KPI 4) 
- Nombre (KPI 5) et pourcentage (KPI 6 ) de clients presentant des signes de baisse d'activité
#### 4. Fréquence
Quotidien

#### 5. Données Nécessaires
1. Les clients
2. Les achats effectués
3. Les données de consommation des services DATA, VOICE et SMS

#### 6. Règles métier
1. Un client présentant un signe de baisse d'activité est un client présentant une baisse pour au moins deux des 4 KPI 1, 2, 3 et 4 sur les périodes considérées, ou une baisse d'au mois 30% pour 2 de ces même KPIs au cas ou seulement deux périodes d'étude sont considérées.



## Exigences Non Fonctionelles (y compris techniques)

1. **Scalabilité:** Supporter l'augmentation des volumes de données sans modification majeure de l'architecture
2. **Fraicheur des données:** Rendre les données disponibles dans les délais nécessaires aux analyses BI et aux prédictions ML
3. **Performance:** Permettre l'exécution des requêtes analytiques et l'affichage des tableaux de bord dans un délai acceptable
4. **Qualité des Données:** Détecter et traiter les données incomplètes, invalides, incohérentes ou dupliquées
5. **Sécurité:**  Protéger les données contre les accès non autorisés
6. **Historisation:** Conserver l'historique nécessaire aux analyses temporelles et au suivi des évolutions
7. **Traçabilité:** Permettre de suivre l'origine, les transformations et le chargement des données
8. **Fiabilité:** Garantir que les traitements peuvent être repris après une erreur sans créer d'incohérence ou de doublons
9. **Maintenabilité:** Faciliter la modification, la correction et l'évolution des pipelies et des composants de la plateforme
10. **Disponibilité:** Garantir l'accès aux services critiques pendant les périodes prévues d'utliisation