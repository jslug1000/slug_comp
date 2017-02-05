
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



DROP PROCEDURE IF EXISTS sp_createGame;
DELIMITER $$
CREATE PROCEDURE `sp_createGame`(
    IN p_tournament_name VARCHAR(50),
    IN p_game_name VARCHAR(50),
    IN p_entered_by VARCHAR(20),
    IN p_first_place_points INT,
    IN p_second_place_points INT,
    IN p_third_place_points INT,
    IN p_fourth_place_points INT
)
BEGIN
    IF (select exists (
      select 1
      from games g

      left join tournaments t2
        on t2.description = p_tournament_name
      where t2.tournament_id = g.tournament_id
      and g.description = p_game_name) ) THEN

        select 'this game already exists for this tournament';

    ELSEIF ( select not exists (
      select 1 from tournaments t where t.description=p_tournament_name) ) THEN

      select 'this tournament does not exist';

    ELSE

        insert into games
        (
            tournament_id,
            description,
            create_date,
            created_by
        )

            select
              t.tournament_id,
              p_game_name,
              NOW(),
              u.user_id

            from users u

            left join tournaments t
              on t.description = p_tournament_name

            where u.username = p_entered_by
        ;

        insert into game_points
          (
            game_id,
            position,
            points
          )
          select
          g.game_id,
          1,
          p_first_place_points

          from games g

          where g.description = p_game_name
          ;

        insert into game_points
          (
            game_id,
            position,
            points
          )
          select
          g.game_id,
          2,
          p_second_place_points

          from games g

          where g.description = p_game_name
          ;

        insert into game_points
          (
            game_id,
            position,
            points
          )
          select
          g.game_id,
          3,
          p_third_place_points

          from games g

          where g.description = p_game_name
          ;

        insert into game_points
          (
            game_id,
            position,
            points
          )
          select
          g.game_id,
          4,
          p_fourth_place_points

          from games g

          where g.description = p_game_name
          ;

    END IF;
END$$
DELIMITER ;




DROP PROCEDURE IF EXISTS sp_setupGame;
DELIMITER $$
CREATE PROCEDURE `sp_setupGame`(
    IN p_tournament_name VARCHAR(50),
    IN p_game_name VARCHAR(50),
    IN p_entered_by VARCHAR(20),
    IN p_competitor1 VARCHAR(20),
    IN p_competitor2 VARCHAR(20),
    IN p_competitor3 VARCHAR(20),
    IN p_competitor4 VARCHAR(20),
    IN p_competitor5 VARCHAR(20),
    IN p_competitor6 VARCHAR(20),
    IN p_competitor7 VARCHAR(20),
    IN p_competitor8 VARCHAR(20),
    IN p_competitor9 VARCHAR(20),
    IN p_competitor10 VARCHAR(20)

)
BEGIN
    IF (select not exists (
      select 1 from tournaments t where t.description=p_tournament_name)) THEN
      select 'this tournament does not exist';

    ELSEIF (select not exists (
      select 1 from games g where g.description=p_game_name) ) THEN
      select 'this game does not exist';

    ELSEIF (select not exists (
      select 1 from tournament_players tp

      LEFT JOIN users u
      on u.username = p_competitor1

      LEFT JOIN tournaments t
      on t.description=p_tournament_name

      where u.user_id=tp.user_id
      and t.tournament_id=tp.tournament_id 
    )
-- check if null
    AND char_length(p_competitor1)>0) THEN
      select concat('competitor 1 is not registered with this tournament');


    ELSE

        insert into game_sessions
        (
            game_id,
            tournament_id,
            created_by
        )

            select
              t.tournament_id,
              g.game_id,
              u.user_id

            from users u

            left join tournaments t
              on t.description = p_tournament_name
            left join games g
              on g.description = p_game_name

            where u.username = p_entered_by
        ;



    END IF;
END$$
DELIMITER ;
