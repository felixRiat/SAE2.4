DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS fait_de;
DROP TABLE IF EXISTS vend;
DROP TABLE IF EXISTS coloris;
DROP TABLE IF EXISTS PANIER;
DROP TABLE IF EXISTS COMMANDE;
DROP TABLE IF EXISTS UTILISATEURS;
DROP TABLE IF EXISTS ETAT;
DROP TABLE IF EXISTS IMAGES;
DROP TABLE IF EXISTS MEUBLE;
DROP TABLE IF EXISTS COULEUR;
DROP TABLE IF EXISTS MATIERE;
DROP TABLE IF EXISTS FOURNISSEUR;
DROP TABLE IF EXISTS TYPE_MEUBLE;
DROP TABLE IF EXISTS MARQUE;

-------------------------
-- CREATION DES TABLES --
-------------------------

CREATE TABLE IF NOT EXISTS MARQUE(
    id_marque INT AUTO_INCREMENT,
    libelle_marque VARCHAR(50),
    PRIMARY KEY(id_marque)
);

CREATE TABLE IF NOT EXISTS TYPE_MEUBLE(
    id_type_meuble INT AUTO_INCREMENT,
    libelle_type_meuble VARCHAR(50),
    PRIMARY KEY(id_type_meuble)
);

CREATE TABLE IF NOT EXISTS FOURNISSEUR(
    id_fournisseur INT AUTO_INCREMENT,
    libelle_fournisseur VARCHAR(50),
    PRIMARY KEY(id_fournisseur)
);

CREATE TABLE IF NOT EXISTS MATIERE(
    id_matiere INT AUTO_INCREMENT,
    libelle_matiere VARCHAR(50),
    PRIMARY KEY(id_matiere)
);

CREATE TABLE IF NOT EXISTS COULEUR(
    id_couleur INT AUTO_INCREMENT,
    libelle_couleur VARCHAR(50),
    PRIMARY KEY(id_couleur)
);

CREATE TABLE IF NOT EXISTS MEUBLE(
    id_meuble INT AUTO_INCREMENT,
    libelle_meuble VARCHAR(255),
    prix_meuble NUMERIC(15, 2),
    dimension_meuble VARCHAR(50),
    poids_meuble NUMERIC(5, 2),
    id_marque INT,
    id_type_meuble INT,
    PRIMARY KEY(id_meuble),
    CONSTRAINT fk_meuble_marque
                FOREIGN KEY (id_marque) REFERENCES MARQUE(id_marque),
    CONSTRAINT fk_meuble_type_meuble
                FOREIGN KEY (id_type_meuble) REFERENCES TYPE_MEUBLE(id_type_meuble)
);

CREATE TABLE IF NOT EXISTS IMAGES(
    id_image INT AUTO_INCREMENT,
    url_image VARCHAR(255),
    id_meuble INT,
    PRIMARY KEY(id_image),
    CONSTRAINT fk_image_meuble
                FOREIGN KEY (id_meuble) REFERENCES MEUBLE(id_meuble)
);

CREATE TABLE IF NOT EXISTS ETAT(
    id_etat INT AUTO_INCREMENT,
    libelle_etat VARCHAR(255),
    PRIMARY KEY(id_etat)
);

CREATE TABLE IF NOT EXISTS UTILISATEURS(
    id_user INT AUTO_INCREMENT,
    username VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),
    est_actif VARCHAR(255),
    email VARCHAR(255),
    PRIMARY KEY(id_user)
);

CREATE TABLE IF NOT EXISTS COMMANDE(
    id_commande INT AUTO_INCREMENT,
    date_achat DATE,
    id_user INT,
    id_etat INT,
    PRIMARY KEY(id_commande),
    CONSTRAINT fk_commande_utilisateur
                    FOREIGN KEY (id_user) REFERENCES UTILISATEURS(id_user),
    CONSTRAINT fk_commande_etat
                    FOREIGN KEY (id_etat) REFERENCES ETAT(id_etat)
);

CREATE TABLE IF NOT EXISTS PANIER(
    id_panier INT AUTO_INCREMENT,
    id_user INT,
    PRIMARY KEY(id_panier),
    CONSTRAINT fk_panier_utilisateur
                FOREIGN KEY (id_user) REFERENCES UTILISATEURS(id_user)
);

CREATE TABLE IF NOT EXISTS coloris(
    id_couleur INT,
    id_meuble INT,
    stock INT,
    PRIMARY KEY(id_couleur, id_meuble),
    CONSTRAINT fk_coloris_couleur
                FOREIGN KEY (id_couleur) REFERENCES COULEUR(id_couleur),
    CONSTRAINT fk_coloris_meuble
                FOREIGN KEY (id_meuble) REFERENCES MEUBLE(id_meuble)
);

CREATE TABLE IF NOT EXISTS vend(
    id_fournisseur INT,
    id_meuble INT,
    PRIMARY KEY(id_fournisseur, id_meuble),
    CONSTRAINT fk_vend_fournisseur
                FOREIGN KEY (id_fournisseur) REFERENCES FOURNISSEUR(id_fournisseur),
    CONSTRAINT fk_vend_meuble
                FOREIGN KEY (id_meuble) REFERENCES MEUBLE(id_meuble)
);

CREATE TABLE IF NOT EXISTS fait_de(
    id_matiere INT,
    id_meuble INT,
    PRIMARY KEY(id_matiere, id_meuble),
    CONSTRAINT fk_fait_de_matiere
                FOREIGN KEY (id_matiere) REFERENCES MATIERE(id_matiere),
    CONSTRAINT fk_fait_de_meuble
                FOREIGN KEY (id_meuble) REFERENCES MEUBLE(id_meuble)
);

CREATE TABLE IF NOT EXISTS ligne_panier(
    id_panier INT,
    id_meuble INT,
    id_couleur INT,
    quantite INT,
    PRIMARY KEY(id_panier, id_meuble, id_couleur),
    CONSTRAINT fk_ligne_panier_matiere
                FOREIGN KEY (id_panier) REFERENCES PANIER(id_panier),
    CONSTRAINT fk_ligne_panier_couleur
                FOREIGN KEY (id_couleur) REFERENCES COULEUR(id_couleur),
    CONSTRAINT fk_ligne_panier_meuble
                FOREIGN KEY (id_meuble) REFERENCES MEUBLE(id_meuble)
);

CREATE TABLE IF NOT EXISTS ligne_commande(
    id_commande INT,
    id_meuble INT,
    id_couleur INT,
    quantite INT,
    PRIMARY KEY(id_commande, id_meuble, id_couleur),
    CONSTRAINT fk_ligne_commande_matiere
                FOREIGN KEY (id_commande) REFERENCES COMMANDE(id_commande),
    CONSTRAINT fk_ligne_commande_couleur
                FOREIGN KEY (id_couleur) REFERENCES COULEUR(id_couleur),
    CONSTRAINT fk_ligne_commande_meuble
                FOREIGN KEY (id_meuble) REFERENCES MEUBLE(id_meuble)
);

-- --------------------------
-- REPRISE DES FOREIGN KEY --
-- --------------------------

ALTER TABLE MEUBLE DROP FOREIGN KEY fk_meuble_marque;
ALTER TABLE MEUBLE ADD CONSTRAINT fk_meuble_marque
                FOREIGN KEY (id_marque) REFERENCES MARQUE(id_marque);
ALTER TABLE MEUBLE DROP FOREIGN KEY fk_meuble_type_meuble;
ALTER TABLE MEUBLE ADD CONSTRAINT fk_meuble_type_meuble
                FOREIGN KEY (id_type_meuble) REFERENCES TYPE_MEUBLE(id_type_meuble);

ALTER TABLE IMAGES DROP FOREIGN KEY fk_image_meuble;
ALTER TABLE IMAGES ADD CONSTRAINT fk_image_meuble
                FOREIGN KEY (id_meuble) REFERENCES MEUBLE(id_meuble);

ALTER TABLE COMMANDE DROP FOREIGN KEY fk_commande_utilisateur;
ALTER TABLE COMMANDE ADD CONSTRAINT fk_commande_utilisateur
                    FOREIGN KEY (id_user) REFERENCES UTILISATEURS(id_user);
ALTER TABLE COMMANDE DROP FOREIGN KEY fk_commande_etat;
ALTER TABLE COMMANDE ADD CONSTRAINT fk_commande_etat
                    FOREIGN KEY (id_etat) REFERENCES ETAT(id_etat);

ALTER TABLE PANIER DROP FOREIGN KEY fk_panier_utilisateur;
ALTER TABLE PANIER ADD CONSTRAINT fk_panier_utilisateur
                FOREIGN KEY (id_user) REFERENCES UTILISATEURS(id_user);

ALTER TABLE coloris DROP FOREIGN KEY fk_coloris_couleur;
ALTER TABLE coloris ADD CONSTRAINT fk_coloris_couleur
                FOREIGN KEY (id_couleur) REFERENCES COULEUR(id_couleur);
ALTER TABLE coloris DROP FOREIGN KEY fk_coloris_meuble;
ALTER TABLE coloris ADD CONSTRAINT fk_coloris_meuble
                FOREIGN KEY (id_meuble) REFERENCES MEUBLE(id_meuble);

ALTER TABLE vend DROP FOREIGN KEY fk_vend_fournisseur;
ALTER TABLE vend ADD CONSTRAINT fk_vend_fournisseur
                FOREIGN KEY (id_fournisseur) REFERENCES FOURNISSEUR(id_fournisseur);
ALTER TABLE vend DROP FOREIGN KEY fk_vend_meuble;
ALTER TABLE vend ADD CONSTRAINT fk_vend_meuble
                FOREIGN KEY (id_meuble) REFERENCES MEUBLE(id_meuble);

ALTER TABLE fait_de DROP FOREIGN KEY fk_fait_de_matiere;
ALTER TABLE fait_de ADD CONSTRAINT fk_fait_de_matiere
                FOREIGN KEY (id_matiere) REFERENCES MATIERE(id_matiere);
ALTER TABLE fait_de DROP FOREIGN KEY fk_fait_de_meuble;
ALTER TABLE fait_de ADD CONSTRAINT fk_fait_de_meuble
                FOREIGN KEY (id_meuble) REFERENCES MEUBLE(id_meuble);

ALTER TABLE ligne_panier DROP FOREIGN KEY fk_ligne_panier_matiere;
ALTER TABLE ligne_panier ADD CONSTRAINT fk_ligne_panier_matiere
                FOREIGN KEY (id_panier) REFERENCES PANIER(id_panier);
ALTER TABLE ligne_panier DROP FOREIGN KEY fk_ligne_panier_meuble;
ALTER TABLE ligne_panier ADD CONSTRAINT fk_ligne_panier_meuble
                FOREIGN KEY (id_meuble) REFERENCES MEUBLE(id_meuble);
ALTER TABLE ligne_panier DROP FOREIGN KEY fk_ligne_panier_couleur;
ALTER TABLE ligne_panier ADD CONSTRAINT fk_ligne_panier_couleur
                FOREIGN KEY (id_couleur) REFERENCES COULEUR(id_couleur);

ALTER TABLE ligne_commande DROP FOREIGN KEY fk_ligne_commande_matiere;
ALTER TABLE ligne_commande ADD CONSTRAINT fk_ligne_commande_matiere
                FOREIGN KEY (id_commande) REFERENCES COMMANDE(id_commande);
ALTER TABLE ligne_commande DROP FOREIGN KEY fk_ligne_commande_meuble;
ALTER TABLE ligne_commande ADD CONSTRAINT fk_ligne_commande_meuble
                FOREIGN KEY (id_meuble) REFERENCES MEUBLE(id_meuble);
ALTER TABLE ligne_commande DROP FOREIGN KEY fk_ligne_commande_couleur;
ALTER TABLE ligne_commande ADD CONSTRAINT fk_ligne_commande_couleur
                FOREIGN KEY (id_couleur) REFERENCES COULEUR(id_couleur);

-- --------------------------
--  INSERTION DES DONNÉES  --
-- --------------------------

INSERT INTO MARQUE (libelle_marque) VALUES
    ('Roche Bobois'),
    ('BUT'),
    ('IKEA'),
    ('Conforama'),
    ('Boconcept'),
    ('Poltronesofa'),
    ('Ligne Roset'),
    ('Kartell');

INSERT INTO TYPE_MEUBLE (libelle_type_meuble) VALUES
    ('table'),
    ('chaise'),
    ('canape'),
    ('lit'),
    ('fauteuil'),
    ('bureau');

INSERT INTO FOURNISSEUR (libelle_fournisseur) VALUES
    ('Petite Friture'),
    ('Leroy Merlin'),
    ('Maisons du Monde'),
    ('TIPTOE'),
    ('IKEA'),
    ('Selency'),
    ('The Cool Republic');

INSERT INTO MATIERE (libelle_matiere) VALUES
    ('metal'),
    ('verre'),
    ('chene'),
    ('inox'),
    ('bois massif'),
    ('ceramique'),
    ('acier'),
    ('plastique'),
    ('tissu'),
    ('cuir');

INSERT INTO COULEUR (libelle_couleur) VALUES
    ('FFFFFF'),
    ('0000FF'),
    ('DEB887'), -- bois
    ('DE00FF'), -- metal
    ('E6FEFF'), -- transparent
    ('FFFF00'),
    ('000000'),
    ('FFEBC9'),
    ('AAAAAA'),
    ('FFAD00'),
    ('FF0000');

INSERT INTO MEUBLE (libelle_meuble, prix_meuble, dimension_meuble, poids_meuble, Id_marque, Id_type_meuble) VALUES
    ('Leifarne', 49.99, '53x46', 2, 3, 2),
    ('Kivik', 649, '228x83', 52, 3, 3),
    ('Utespelare', 179, '160x78', 29, 3, 6),
    ('Scenario', 10250, '445x85x115', 56, 1, 3),
    ('Pulp', 3290, '89x113x82', 8, 1, 5),
    ('Crociale', 8290, '314*97*217', 59, 6, 3),
    ('Zoe', 399.99, '210*173.5*118.5', 39, 2, 4),
    ('Hawai', 545.40, '100x77x280', 135, 4, 1),
    ('Ottawa', 199.00, '50*56*86', 7, 5, 2),
    ('Clyde', 2310.00, '84.5*130*57.1', 44, 7, 6),
    ('Cara', 919.00, '69*68*67', 12, 8, 5),
    ('Invisible Table', 797.00, '72*100*100', 42, 8, 1),
    ('Table Madrid', 1486.65, '75x127', 48, 5, 1);

INSERT INTO IMAGES(url_image, id_meuble) VALUES
        ('https://www.ikea.com/fr/fr/images/products/leifarne-chaise-jaune-fonce-ernfrid-bouleau__0745133_pe743594_s5.jpg?f=l', 1),
        ('https://www.ikea.com/fr/fr/images/products/leifarne-chaise-orange-ernfrid-bouleau__0745143_pe743602_s5.jpg?f=l', 1),
        ('https://www.ikea.com/fr/fr/images/products/leifarne-chaise-blanc-ernfrid-bouleau__0729771_pe737141_s5.jpg?f=l', 1),
        ('https://www.ikea.com/fr/fr/images/products/leifarne-chaise-blanc-ernfrid-bouleau__0874903_pe595425_s5.jpg?f=l', 1),
        ('https://www.ikea.com/fr/fr/images/products/kivik-canape-3-places-orrsta-gris-clair__0249491_pe387762_s5.jpg?f=l', 2),
        ('https://www.ikea.com/fr/fr/images/products/kivik-canape-3-places-hillared-bleu-fonce__0504261_pe633252_s5.jpg?f=l', 2),
        ('https://www.ikea.com/fr/fr/images/products/kivik-canape-3-places-hillared-beige__0788747_pe763719_s5.jpg?f=l', 2),
        ('https://www.ikea.com/fr/fr/images/products/kivik-canape-3-places-hillared-beige__0479989_pe618870_s5.jpg?f=l', 2),
        ('https://www.ikea.com/fr/fr/images/products/utespelare-bureau-gamer-noir__0985179_pe816538_s5.jpg?f=l', 3),
        ('https://www.ikea.com/fr/fr/images/products/utespelare-bureau-gamer-gris-clair__0998214_pe822969_s5.jpg?f=l', 3),
        ('https://www.ikea.com/fr/fr/images/products/utespelare-bureau-gamer-gris-clair__0997779_pe822756_s5.jpg?f=l', 3),
        ('https://media.roche-bobois.com/ir/render/rocheboboisRender/scenario_comp-angle_soave_pers2_2016?wid=1250&fmt=pjpeg&resMode=sharp2&qlt=80&obj=revp&color=72,73,77', 4),
        ('https://media.roche-bobois.com/ir/render/rocheboboisRender/scenario_comp-angle_soave_pers2_2016?wid=1250&fmt=pjpeg&resMode=sharp2&qlt=80&obj=revp&color=70,70,70', 4),
        ('https://media.roche-bobois.com/ir/render/rocheboboisRender/scenario_comp-angle_soave_pers2_2016?wid=1250&fmt=pjpeg&resMode=sharp2&qlt=80&obj=revp&color=211,206,193', 4),
        ('https://img.edilportale.com/product-thumbs/2b_SCENARIO-Roche-Bobois-389801-rel12975fc0.jpg', 4),
        ('https://media.roche-bobois.com/ir/render/rocheboboisRender/pulp_fauteuil_riviera_pers1?wid=1250&fmt=pjpeg&resMode=sharp2&qlt=80&obj=revp&color=50,50,50', 5),
        ('https://media.roche-bobois.com/ir/render/rocheboboisRender/pulp_fauteuil_riviera_pers1?wid=1250&fmt=pjpeg&resMode=sharp2&qlt=80&obj=revp&color=43,54,75', 5),
        ('https://media.roche-bobois.com/ir/render/rocheboboisRender/pulp_fauteuil_riviera_pers1?wid=1250&fmt=pjpeg&resMode=sharp2&qlt=80&obj=revp&color=131,24,24', 5),
        ('https://media.roche-bobois.com/ir/render/rocheboboisRender/pulp_fauteuil_riviera_pers1?wid=1250&fmt=pjpeg&resMode=sharp2&qlt=80&obj=revp&color=227,224,221', 5),
        ('https://www.poltronesofa.com/images/FotoModelli/CROCIALE/dett/3.jpg', 6),
        ('https://www.poltronesofa.com/images/FotoModelli/CROCIALE/dett/1.jpg', 6),
        ('https://media.but.fr/images_produits/produit-zoom/5945827039930_Q.jpg', 7),
        ('https://media.but.fr/images_produits/produit-zoom/5945827039930_D.jpg', 7),
        ('https://media.but.fr/images_produits/produit-zoom/5945827039930_A.jpg', 7),
        ('https://media.conforama.fr/m/export/Medias/700000/00000/5000/000/90/G_705096_Y.jpg', 8),
        ('https://media.conforama.fr/m/export/Medias/700000/00000/5000/000/90/G_705096_A.jpg', 8),
        ('https://images.demandware.net/dw/image/v2/BBBV_PRD/on/demandware.static/-/Sites-master-catalog/default/dw78956cc5/images/300000/308299.jpg?sw=1600', 9),
        ('https://images.demandware.net/dw/image/v2/BBBV_PRD/on/demandware.static/-/Sites-master-catalog/default/dw0578ddf5/images/300000/308274.jpg?sw=1600', 9),
        ('https://image.architonic.com/pro2-3/20171101/clyde-00bsax10-210119-pro-b-arcit18.jpg', 10),
        ('https://images.ligne-roset.com/cache/models/2613/iambiance1/1/0/1003uq_2000x2000.jpg', 10),
        ('https://www.kartellshowroom.com/26306-large_default/cara.jpg', 11),
        ('https://www.kartellshowroom.com/4470-large_default/cara.jpg', 11),
        ('https://www.kartellshowroom.com/4469-large_default/cara.jpg', 11),
        ('https://cdn.ambientedirect.com/chameleon/mediapool/thumbs/e/e0/Kartell_Invisible-Table-Tisch_1871x1871-ID548456-572793098233b7e24b8e1dee16b78fcc.jpg', 12),
        ('https://cdn.ambientedirect.com/chameleon/mediapool/thumbs/c/1b/Kartell_Invisible-Table-Tisch_885x885-ID338543-acf211e93baccb9aee33e68a07e415b9.jpg', 12),
        ('https://images.demandware.net/dw/image/v2/BBBV_PRD/on/demandware.static/-/Sites-master-catalog/default/dw309eeaed/images/660000/667405.jpg?sw=1600', 13),
        ('https://images.demandware.net/dw/image/v2/BBBV_PRD/on/demandware.static/-/Sites-master-catalog/default/dwe8ca9952/images/660000/667407.jpg?sw=1600', 13),
        ('https://images.demandware.net/dw/image/v2/BBBV_PRD/on/demandware.static/-/Sites-master-catalog/default/dw3abe345f/images/800000/802162.jpg?sw=1600', 13);

INSERT INTO UTILISATEURS (email, username, password, role,  est_actif) VALUES
('admin@admin.fr', 'admin', 'sha256$pBGlZy6UukyHBFDH$2f089c1d26f2741b68c9218a68bfe2e25dbb069c27868a027dad03bcb3d7f69a', 'ROLE_admin', 1),
('client@client.fr', 'client', 'sha256$Q1HFT4TKRqnMhlTj$cf3c84ea646430c98d4877769c7c5d2cce1edd10c7eccd2c1f9d6114b74b81c4', 'ROLE_client', 1),
('client2@client2.fr', 'client2', 'sha256$ayiON3nJITfetaS8$0e039802d6fac2222e264f5a1e2b94b347501d040d71cfa4264cad6067cf5cf3', 'ROLE_client',1);

INSERT INTO coloris(id_meuble, id_couleur, stock) VALUES
    (1, 1, 3),
    (1, 6, 3),
    (1, 10, 3),
    (2, 8, 3),
    (2, 9, 3),
    (2, 2, 3),
    (3, 7, 3),
    (3, 9, 3),
    (4, 8, 3),
    (4, 1, 3),
    (4, 7, 3),
    (5, 1, 3),
    (5, 7, 3),
    (5, 2, 3),
    (5, 11, 3),
    (6, 8, 3),
    (6, 1, 3),
    (6, 2, 3),
    (6, 11, 3),
    (7, 9, 3),
    (8, 3, 3),
    (9, 1, 3),
    (9, 7, 3),
    (10, 7, 3),
    (11, 7, 3),
    (11, 1, 3),
    (12, 5, 3),
    (12, 7, 3),
    (13, 1, 3),
    (13, 5, 3);

INSERT INTO vend(id_meuble, id_fournisseur)VALUES
    (1, 5),
    (2, 5),
    (3, 5),
    (4, 1),
    (5, 6),
    (6, 7),
    (7, 3),
    (8, 2),
    (9, 2),
    (10, 4),
    (11, 1),
    (12, 4),
    (13, 6);

INSERT INTO fait_de(id_meuble, id_matiere) VALUES
    (1, 8),
    (2, 9),
    (3, 7),
    (4, 10),
    (5, 10),
    (6, 9),
    (7, 5),
    (8, 3),
    (9, 8),
    (10, 7),
    (11, 9),
    (12, 8),
    (13, 2);

INSERT INTO ETAT(libelle_etat) VALUES
    ('En cour de traitement'),
    ('Expédié');
