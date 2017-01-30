
DELIMITER $$
CREATE PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(45),
    IN p_username VARCHAR(20),
    IN p_password VARCHAR(45)
)
BEGIN
    if ( select exists (select 1 from users where username = p_username) ) THEN

        select 'Username Exists !!';

    ELSE

        insert into users
        (
            name,
            username,
            password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );

    END IF;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE `sp_validateLogin`(
IN p_username VARCHAR(20)
)
BEGIN
    select * from users where username = p_username;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE `sp_createTournament`(
    IN p_tournament_name VARCHAR(50),
    IN p_username VARCHAR(20)
)
BEGIN
    if ( select exists (select 1 from tournaments where description = p_tournament_name) ) THEN

        select 'there is already a tournament with that name';

    ELSE

        insert into tournaments
        (
            description,
            creation_date,
            created_by
        )
        values
        (
            p_tournament_name,
            DATE(NOW()),
            p_username
        );

    END IF;
END$$
DELIMITER ;


DROP PROCEDURE IF EXISTS`sp_GetAllUsers`;
DELIMITER $$
CREATE PROCEDURE `sp_GetAllUsers` ()
BEGIN
    select username from users;
END$$
DELIMITER ;
