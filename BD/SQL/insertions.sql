-- Cours -> id , [TP/TD/CM] , domaine , heureTotal , duree
INSERT INTO COURS VALUES ("1", 'TP', 'Qualité de developpement','Programmation',21, 90);
INSERT INTO COURS VALUES ("2", 'CM', 'Qualité de developpement','Programmation',20, 75);
INSERT INTO COURS VALUES ("3", 'TD', 'Probabilité','Math',25, 75);

INSERT INTO UTILISATEUR VALUES ("V1",'Blin--Dorard','Bryan', "0783898400", '2003-06-01','bryanblindorard@gmail.com');
INSERT INTO UTILISATEUR VALUES ("V2",'Bourdere','Nathan', "0666554482", '2003-09-01','boudereandreounathan@gmail.com');
INSERT INTO UTILISATEUR VALUES ("V3",'Loszach','Constantin', "0617757221", '2003-02-02','constantinloszach@gmail.com');
INSERT INTO UTILISATEUR VALUES ("A4",'Viard','Théo', "0695347118", '2003-01-27','theoviard2701@gmail.com');

-- Vacataire -> id , [Spontanée/Recommandée/] , ancien
INSERT INTO VACATAIRE VALUES ("V1","Spontané",FALSE);
INSERT INTO VACATAIRE VALUES ("V2","Recommandé",FALSE);
INSERT INTO VACATAIRE VALUES ("V3","Sélectionné",TRUE);
INSERT INTO PERSONNELADMINISTRATIF VALUES ("A4");

-- GérerDossier -> idAdmin , idVacataire , [Distribué / Remis incomplet / Remis complet / Validé.] , date , heure

INSERT INTO GERERDOSSIER VALUES ("A4","V1","Validé","2022-01-01",10);
INSERT INTO GERERDOSSIER VALUES ("A4","V2","Remis Complet","2022-01-01",11);
INSERT INTO GERERDOSSIER VALUES ("A4","V3","Remis Incomplet","2022-01-01",12);


INSERT INTO AFFECTABLE VALUES ("1", 'TP', 'V1');

INSERT INTO ASSIGNER VALUES ("1","TP","V1","I201","2A2A","2023-01-02",10);