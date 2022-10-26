DROP TABLE ASSIGNER;
DROP TABLE AFFECTABLE;
DROP TABLE GERERDOSSIER;
DROP TABLE PERSONNELADMINISTRATIF;
DROP TABLE VACATAIRE;
DROP TABLE UTILISATEUR;
DROP TABLE COURS;

CREATE TABLE UTILISATEUR(
    IDuser varchar(20) NOT NULL,
    nomU varchar(20),
    prenomU varchar(20),
    telU int(14),
    ddnU DATE,
    mail varchar(20),
    PRIMARY KEY(IDuser)
);

CREATE TABLE PERSONNELADMINISTRATIF(
    IDpersAdmin varchar(20) NOT NULL,
    PRIMARY KEY(IDpersAdmin)
);

CREATE TABLE VACATAIRE(
    IDvacataire varchar(20) NOT NULL,
    candidature varchar(42),
    ancien boolean,
    PRIMARY KEY(IDvacataire)
);

CREATE TABLE GERERDOSSIER(
    IDpersAdmin varchar(20) NOT NULL,
    IDvacataire varchar(20) NOT NULL,
    etat_dossier varchar(20),
    dateModif DATE,
    heureModif int(2) check (heureModif between 0 and 23),
    PRIMARY KEY(IDpersAdmin,IDvacataire)
);

--dureeCours en minutes
CREATE TABLE COURS(
    IDCours varchar(6) NOT NULL,
    TypeCours varchar(2) NOT NULL,
    nomCours varchar(42),
    domaine varchar(42),
    heuresTotale int(3) check (heuresTotale between 0 and 23),
    dureeCours int(3),
    PRIMARY KEY(IDCours,TypeCours)
);

CREATE TABLE AFFECTABLE(
    IDCours varchar(6) NOT NULL,
    TypeCours varchar(2) NOT NULL,
    IDvacataire varchar(20) NOT NULL,
    PRIMARY KEY(IDCours,TypeCours,IDvacataire)
);
--salle ex: I201
--classe ex: 2A ou 2A2 ou 2A2A (en fonction du type de cours)
CREATE TABLE ASSIGNER(
    IDCours varchar(6) NOT NULL,
    TypeCours varchar(2) NOT NULL,
    IDvacataire varchar(20) NOT NULL,
    salle varchar(12),
    classe varchar(4),
    PRIMARY KEY (IDCours,TypeCours,IDvacataire)
);

ALTER TABLE PERSONNELADMINISTRATIF ADD FOREIGN KEY(IDpersAdmin) REFERENCES UTILISATEUR(IDuser);
ALTER TABLE VACATAIRE ADD FOREIGN KEY(IDvacataire) REFERENCES UTILISATEUR(IDuser);  
ALTER TABLE GERERDOSSIER ADD FOREIGN KEY(IDpersAdmin) REFERENCES PERSONNELADMINISTRATIF(IDpersAdmin); 
ALTER TABLE GERERDOSSIER ADD FOREIGN KEY(IDvacataire) REFERENCES VACATAIRE(IDvacataire); 
ALTER TABLE AFFECTABLE ADD FOREIGN KEY(IDCours,TypeCours) REFERENCES COURS(IDCours,TypeCours);
ALTER TABLE AFFECTABLE ADD FOREIGN KEY(IDvacataire) REFERENCES VACATAIRE(IDvacataire); 
ALTER TABLE ASSIGNER ADD FOREIGN KEY(IDCours,TypeCours) REFERENCES COURS(IDCours,TypeCours);
ALTER TABLE ASSIGNER ADD FOREIGN KEY(IDvacataire) REFERENCES VACATAIRE(IDvacataire);

--TRIGGERS

--trigger numéro 1 : on s'assure qu'un ancien vacataire n'est pas assigné à un cours
DELIMITER |
create or replace trigger ancienPasAssignable before insert on ASSIGNER for each row
BEGIN
    declare res varchar(500) DEFAULT '';
    declare est_ancien boolean DEFAULT FALSE;
    select ancien into est_ancien from ASSIGNER NATURAL JOIN VACATAIRE where IDvacataire = new.IDvacataire;
    if (ancien = TRUE) then
        set res = concat(res,"erreur :",new.IDvacataire," est un ancien vacataire, il n'enseigne plus ici, assignation impossible");
        signal SQLSTATE '45000' set MESSAGE_TEXT = res;
    end if;
END |
DELIMITER ;