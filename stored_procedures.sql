
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

DROP PROCEDURE IF EXISTS sp_createCompetitor;
DELIMITER $$
CREATE PROCEDURE `sp_createCompetitor`(
    IN p_tournament_name VARCHAR(50),
    IN p_competitor_name VARCHAR(50),
    IN p_entered_by VARCHAR(20)
)
BEGIN
    IF ( select exists (
      select 1
      from tournament_players tp
      left join users u
        on u.username = p_competitor_name
      left join tournaments t2
        on t2.description = p_tournament_name
      where t2.tournament_id = tp.tournament_id
      and u.user_id = tp.user_id) ) THEN

        select 'this player is already entered in the tournament';

        -- NEED TO CHECK IF PLAYER EXISTS
    ELSEIF ( select not exists (
      select 1 from users u where u.username=p_competitor_name) ) THEN

      select 'this player does not exist, try again, mate';

    ELSE

        insert into tournament_players
        (
            user_id,
            tournament_id,
            entered_by,
            added_at
        )

            select
              u.user_id,
              t2.tournament_id,
              u2.user_id,
              DATE(NOW())
            from users u

            left join users u2
              on u2.username = p_entered_by

            left join tournaments t2
              on t2.description = p_tournament_name

            where u.username = p_competitor_name
        ;

    END IF;
END$$
DELIMITER ;
