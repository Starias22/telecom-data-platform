CREATE TABLE ref.cities(
        id SERIAL PRIMARY KEY,
        city VARCHAR(20) NOT NULL,
        department VARCHAR(20) NOT NULL
);

INSERT INTO ref.cities (department, city)
VALUES
    -- Alibori (6 communes)
    ('Alibori', 'Banikoara'),
    ('Alibori', 'Gogounou'),
    ('Alibori', 'Kandi'),
    ('Alibori', 'Karimama'),
    ('Alibori', 'Malanville'),
    ('Alibori', 'Ségbana'),

    -- Atacora (9 communes)
    ('Atacora', 'Boukoumbé'),
    ('Atacora', 'Cobly'),
    ('Atacora', 'Kérou'),
    ('Atacora', 'Kouandé'),
    ('Atacora', 'Matéri'),
    ('Atacora', 'Natitingou'),
    ('Atacora', 'Péhunco'),
    ('Atacora', 'Tanguiéta'),
    ('Atacora', 'Toucountouna'),

    -- Atlantique (8 communes)
    ('Atlantique', 'Abomey-Calavi'),
    ('Atlantique', 'Allada'),
    ('Atlantique', 'Kpomassè'),
    ('Atlantique', 'Ouidah'),
    ('Atlantique', 'Sô-Ava'),
    ('Atlantique', 'Toffo'),
    ('Atlantique', 'Tori-Bossito'),
    ('Atlantique', 'Zè'),

    -- Borgou (8 communes)
    ('Borgou', 'Bembèrèkè'),
    ('Borgou', 'Kalalé'),
    ('Borgou', 'N''Dali'),
    ('Borgou', 'Nikki'),
    ('Borgou', 'Parakou'),
    ('Borgou', 'Pèrèrè'),
    ('Borgou', 'Sinendé'),
    ('Borgou', 'Tchaourou'),

    -- Collines (6 communes)
    ('Collines', 'Bantè'),
    ('Collines', 'Dassa-Zoumè'),
    ('Collines', 'Glazoué'),
    ('Collines', 'Ouèssè'),
    ('Collines', 'Savalou'),
    ('Collines', 'Savè'),

    -- Couffo (6 communes)
    ('Couffo', 'Aplahoué'), -- Azovè est un arrondissement de la commune d'Aplaphoué
    ('Couffo', 'Djakotomey'),
    ('Couffo', 'Dogbo'),
    ('Couffo', 'Klouékanmè'),
    ('Couffo', 'Lalo'),
    ('Couffo', 'Toviklin'),

    -- Donga (4 communes)
    ('Donga', 'Bassila'),
    ('Donga', 'Copargo'),
    ('Donga', 'Djougou'),
    ('Donga', 'Ouaké'),

    -- Littoral (1 commune)
    ('Littoral', 'Cotonou'),

    -- Mono (6 communes)
    ('Mono', 'Athiémé'),
    ('Mono', 'Bopa'),
    ('Mono', 'Comè'),
    ('Mono', 'Grand-Popo'),
    ('Mono', 'Houéyogbé'),
    ('Mono', 'Lokossa'),

    -- Ouémé (9 communes)
    ('Ouémé', 'Adjarra'),
    ('Ouémé', 'Adjohoun'),
    ('Ouémé', 'Aguégués'),
    ('Ouémé', 'Akpro-Missérété'),
    ('Ouémé', 'Avrankou'),
    ('Ouémé', 'Bonou'),
    ('Ouémé', 'Dangbo'),
    ('Ouémé', 'Porto-Novo'),
    ('Ouémé', 'Sèmè-Podji'),

    -- Plateau (5 communes)
    ('Plateau', 'Adja-Ouèrè'),
    ('Plateau', 'Ifangni'),
    ('Plateau', 'Kétou'),
    ('Plateau', 'Pobè'),
    ('Plateau', 'Sakété'),

    -- Zou (9 communes)
    ('Zou', 'Abomey'),
    ('Zou', 'Agbangnizoun'),
    ('Zou', 'Bohicon'),
    ('Zou', 'Covè'),
    ('Zou', 'Djidja'),
    ('Zou', 'Ouinhi'),
    ('Zou', 'Za-Kpota'),
    ('Zou', 'Zagnanado'),
    ('Zou', 'Zogbodomey');