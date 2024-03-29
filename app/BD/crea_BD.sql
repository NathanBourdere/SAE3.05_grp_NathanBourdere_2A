DROP TABLE ASSIGNER;
DROP TABLE AFFECTABLE;
DROP TABLE GERERDOSSIER;
DROP TABLE PERSONNELADMINISTRATIF;
DROP TABLE VACATAIRE;
DROP TABLE UTILISATEUR;
DROP TABLE COURS;

CREATE TABLE UTILISATEUR(
    IDuser varchar(20) NOT NULL,
    nomU varchar(30),
    prenomU varchar(30),
    telU int(14) UNIQUE,
    ddnU DATE,
    mail varchar(50) UNIQUE,
    mdpU varchar(50),
    PRIMARY KEY(IDuser)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE PERSONNELADMINISTRATIF(
    IDpersAdmin varchar(20) NOT NULL,
    PRIMARY KEY(IDpersAdmin)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE VACATAIRE(
    IDvacataire varchar(20) NOT NULL,
    candidature varchar(42),
    ancien boolean,
    PRIMARY KEY(IDvacataire)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE GERERDOSSIER(
    IDpersAdmin varchar(20) NOT NULL,
    IDvacataire varchar(20) NOT NULL,
    etat_dossier varchar(20),
    dateModif DATE,
    heureModif int(2) check (heureModif between 0 and 23),
    PRIMARY KEY(IDpersAdmin,IDvacataire)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

--dureeCours en minutes
CREATE TABLE COURS(
    IDCours varchar(6) NOT NULL,
    TypeCours varchar(2) NOT NULL,
    nomCours varchar(42) NOT NULL,
    domaine varchar(42) NOT NULL,
    heuresTotale int(3),
    dureeCours int(3),
    PRIMARY KEY(IDCours,TypeCours)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE AFFECTABLE(
    IDCours varchar(6) NOT NULL,
    TypeCours varchar(2) NOT NULL,
    IDvacataire varchar(20) NOT NULL,
    PRIMARY KEY(IDCours,TypeCours,IDvacataire)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
--salle ex: I201
--classe ex: 2A ou 2A2 ou 2A2A (en fonction du type de cours)
CREATE TABLE ASSIGNER(
    IDCours varchar(6) NOT NULL,
    TypeCours varchar(2) NOT NULL,
    IDvacataire varchar(20) NOT NULL,
    salle varchar(12),
    classe varchar(4),
    dateCours DATE,
    heureCours int(2) check (heureCours between 0 and 23),
    PRIMARY KEY (IDCours,TypeCours,IDvacataire)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

ALTER TABLE PERSONNELADMINISTRATIF ADD FOREIGN KEY(IDpersAdmin) REFERENCES UTILISATEUR(IDuser);
ALTER TABLE VACATAIRE ADD FOREIGN KEY(IDvacataire) REFERENCES UTILISATEUR(IDuser);  
ALTER TABLE GERERDOSSIER ADD FOREIGN KEY(IDpersAdmin) REFERENCES PERSONNELADMINISTRATIF(IDpersAdmin); 
ALTER TABLE GERERDOSSIER ADD FOREIGN KEY(IDvacataire) REFERENCES VACATAIRE(IDvacataire); 
ALTER TABLE AFFECTABLE ADD FOREIGN KEY(IDCours,TypeCours) REFERENCES COURS(IDCours,TypeCours);
ALTER TABLE AFFECTABLE ADD FOREIGN KEY(IDvacataire) REFERENCES VACATAIRE(IDvacataire); 
ALTER TABLE ASSIGNER ADD FOREIGN KEY(IDCours,TypeCours) REFERENCES COURS(IDCours,TypeCours);
ALTER TABLE ASSIGNER ADD FOREIGN KEY(IDvacataire) REFERENCES VACATAIRE(IDvacataire);

--TRIGGERS

-- trigger numéro 1 : on s'assure qu'un ancien vacataire n'est pas assigné à un cours
DELIMITER |
create or replace trigger ancienPasAssignable before insert on ASSIGNER for each row
BEGIN
    declare res varchar(500) DEFAULT '';
    declare est_ancien boolean DEFAULT FALSE;
    select ancien into est_ancien from VACATAIRE where IDvacataire = new.IDvacataire;
    if (est_ancien = TRUE) then
        set res = concat(res,"erreur : ",new.IDvacataire," est un ancien vacataire, il n'enseigne plus ici, assignation impossible");
        signal SQLSTATE '45000' set MESSAGE_TEXT = res;
    end if;
END |
DELIMITER ;

-- trigger numéro 2 : Un vacataire ne peut pas se faire assigner un cours tant que son dossier n'est pas validé
DELIMITER |
create or replace trigger vacataireNonAssignableTantQuePasValidee before insert on ASSIGNER for each row
BEGIN
    declare res varchar(500) DEFAULT '';
    declare etat_doc varchar(20) DEFAULT '';
    select etat_dossier into etat_doc from GERERDOSSIER where IDvacataire = new.IDvacataire;
    if (etat_doc != "Validé") then
        set res = concat(res,"erreur : ",new.IDvacataire," à son dossier laissé en l'état : ",etat_doc, ", son dossier doit être validé avant");
        signal SQLSTATE '45000' set MESSAGE_TEXT = res;
    end if;
END |
DELIMITER ;

-- trigger numéro 3 : Un vacataire ne peut pas se faire assigner un cours (et son type) dont il n'est pas affectable
DELIMITER |
create or replace trigger vacataireNonAffectable before insert on ASSIGNER for each row
BEGIN
    declare res varchar(500) DEFAULT '';
    declare idv_dans_affectable varchar(20) DEFAULT '';
    select IDvacataire into idv_dans_affectable from AFFECTABLE where IDvacataire = new.IDvacataire and IDCours = new.IDCours and TypeCours = new.TypeCours;
    if (idv_dans_affectable = '') then
        set res = concat(res,"erreur : ",idv_dans_affectable," n'est pas affectable au cours ",new.IDCours," (en ",new.TypeCours,")");
        signal SQLSTATE '45000' set MESSAGE_TEXT = res;
    end if;
END |
DELIMITER ;

-- trigger numéro 4 : Un vacataire ne peut pas se faire assigner un cours (et son type) si la date du cours est du passé
DELIMITER |
create or replace trigger dateAssignationPassee before insert on ASSIGNER for each row
BEGIN
    declare res varchar(500) DEFAULt '';
    declare idv_dans_affectable varchar(20) DEFAULT '';
    declare data_actulle DATE;
    select now() into data_actulle;
    if (new.dateCours < data_actulle) then
        set res = concat(res,"erreur : n'est pas affectable au cours car la date indiquée est passée");
        signal SQLSTATE '45000' set MESSAGE_TEXT = res;
    end if;
END |
DELIMITER ;

-- pour sqlAlchemy : Un vacataire doit avoir son etat_dossier passé de incomplet à complet si il n'y a aucun NULL
-- l'insertion de cours sera automatisé aussi par sqlAlchemy


-- trigger numéro 5 : Un cours ne doit pas avoir le même nom et le même type de cours avec un autre cours existant
DELIMITER |
create or replace trigger coursUnique before insert on COURS for each row
BEGIN
    declare res varchar(500) DEFAULT '';
    declare idcours_dans_cours varchar(6) DEFAULT '';
    select IDCours into idcours_dans_cours from COURS where TypeCours = new.TypeCours and nomCours = new.nomCours;
    if (idcours_dans_cours != '') then
        set res = concat(res,"erreur :Il y a un même cours déja existant");
        signal SQLSTATE '45000' set MESSAGE_TEXT = res;
    end if;
END |
DELIMITER ;


-- trigger numéro 6 : Deux cours différents ne peuvent pas se passer en même temps dans la même salle
DELIMITER |
create or replace trigger uneSalleUnCours before insert on ASSIGNER for each row
BEGIN
    declare res varchar(500) DEFAULT '';
    declare idcours_dans_cours varchar(6) DEFAULT '';
    select IDCours into idcours_dans_cours from ASSIGNER natural join COURS natural join VACATAIRE where dateCours = new.dateCours and heureCours = new.heureCours and salle = new.salle;
    if (idcours_dans_cours != '') then
        set res = concat(res,"erreur :Il y a un même cours déja existant à cette date et heure dans cette salle");
        signal SQLSTATE '45000' set MESSAGE_TEXT = res;
    end if;
END |
DELIMITER ;

-- trigger numéro 7 : Une classe ne peut pas avoir deux cours en même temps
DELIMITER |
create or replace trigger uneClasseUnCours before insert on ASSIGNER for each row
BEGIN
    declare res varchar(500) DEFAULT '';
    declare idcours_dans_cours varchar(6) DEFAULT '';
    select IDCours into idcours_dans_cours from ASSIGNER natural join COURS natural join VACATAIRE where dateCours = new.dateCours and heureCours = new.heureCours and classe = new.classe;
    if (idcours_dans_cours != '') then
        set res = concat(res,"erreur :Il y a un même cours déja existant à cette date et heure pour cette classe");
        signal SQLSTATE '45000' set MESSAGE_TEXT = res;
    end if;
END |
DELIMITER ;

