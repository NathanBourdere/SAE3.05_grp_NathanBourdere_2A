-- -- trigger 1
-- INSERT INTO UTILISATEUR VALUES ("V5",'JEAN', 'PAUL', '0654789502', '2003-09-01','mail','12345');
-- INSERT INTO VACATAIRE VALUES ("V5","Spontané",TRUE);
-- INSERT INTO GERERDOSSIER VALUES ("A4","V5","Validé","2022-01-01",13);
-- INSERT INTO AFFECTABLE VALUES ("2", 'CM', 'V5');

-- INSERT INTO ASSIGNER VALUES ("2","CM","V5","I203","2A2B","2023-01-02",10);

-- DELETE FROM AFFECTABLE WHERE IDCours = "2" and TypeCours = "CM" and IDvacataire = "V5";
-- DELETE FROM GERERDOSSIER WHERE IDpersAdmin = "A4" and IDvacataire = "V5";
-- DELETE FROM VACATAIRE WHERE IDvacataire = "V5";
-- DELETE FROM UTILISATEUR WHERE IDuser = "V5";

-- -- trigger 2
-- INSERT INTO AFFECTABLE VALUES ("2", 'CM', 'V3');

-- INSERT INTO ASSIGNER VALUES ("2","CM","V3","I203","2A2A","2023-01-02",10);

-- DELETE FROM AFFECTABLE WHERE IDCours = "2" and TypeCours = "CM" and IDvacataire = "V3";

-- -- trigger 3
-- INSERT INTO ASSIGNER VALUES ("1","TP","V2","I203","2A2A","2023-01-02",10);

-- trigger 4
-- INSERT INTO ASSIGNER VALUES ("1","TP","V1","I203","2A2A","2010-01-02",10);

-- -- trigger 5
-- INSERT INTO COURS VALUES ("4", 'TD', 'Probabilité','Math',25, 75);

-- -- trigger 6
-- INSERT INTO UTILISATEUR VALUES ("V5",'JEAN', 'PAUL', '0654789502', '2003-09-01','mail','12345');
-- INSERT INTO VACATAIRE VALUES ("V5","Spontané",FALSE);
-- INSERT INTO GERERDOSSIER VALUES ("A4","V5","Validé","2022-01-01",13);
-- INSERT INTO AFFECTABLE VALUES ("2", "CM", "V5");

-- INSERT INTO ASSIGNER VALUES ("2","CM","V5","I201","2A2A","2023-01-02",10);

-- DELETE FROM AFFECTABLE WHERE IDCours = "2" and TypeCours = "CM" and IDvacataire = "V5";
-- DELETE FROM GERERDOSSIER WHERE IDpersAdmin = "A4" and IDvacataire = "V5";
-- DELETE FROM VACATAIRE WHERE IDvacataire = "V5";
-- DELETE FROM UTILISATEUR WHERE IDuser = "V5";

-- trigger 7
INSERT INTO UTILISATEUR VALUES ("V5",'JEAN', 'PAUL', '0654789502', '2003-09-01','mail','12345');
INSERT INTO VACATAIRE VALUES ("V5","Spontané",FALSE);
INSERT INTO GERERDOSSIER VALUES ("A4","V5","Validé","2022-01-01",13);
INSERT INTO AFFECTABLE VALUES ("2", 'CM', 'V5');

INSERT INTO ASSIGNER VALUES ("2","CM","V5","I203","2A2A","2023-01-02",10);

DELETE FROM AFFECTABLE WHERE IDCours = "2" and TypeCours = "CM" and IDvacataire = "V5";
DELETE FROM GERERDOSSIER WHERE IDpersAdmin = "A4" and IDvacataire = "V5";
DELETE FROM VACATAIRE WHERE IDvacataire = "V5";
DELETE FROM UTILISATEUR WHERE IDuser = "V5";