-- Drop the users table if it already exists
DROP TABLE IF EXISTS users;

-- Create the users table
CREATE TABLE users
(
    id         SERIAL PRIMARY KEY,            -- Unique identifier for each user (auto-incrementing)
    username   TEXT    NOT NULL,              -- Username for the user
    email      TEXT    NOT NULL UNIQUE,       -- Email must be unique
    is_active  BOOLEAN NOT NULL DEFAULT TRUE, -- Active status (TRUE for active, FALSE for inactive)
    created_at TIMESTAMP        DEFAULT NOW() -- Timestamp when the user was created
);

-- Insert sample data into the users table
INSERT INTO users (username, email, is_active)
VALUES ('alice_smith', 'alice.smith@example.com', TRUE),
       ('bob_johnson', 'bob.johnson@example.com', TRUE),
       ('carol_white', 'carol.white@example.com', FALSE),
       ('david_brown', 'david.brown@example.com', TRUE),
       ('eve_davis', 'eve.davis@example.com', TRUE),
       ('frank_miller', 'frank.miller@example.com', FALSE),
       ('grace_wilson', 'grace.wilson@example.com', TRUE),
       ('hank_moore', 'hank.moore@example.com', TRUE),
       ('iris_taylor', 'iris.taylor@example.com', FALSE),
       ('jack_anderson', 'jack.anderson@example.com', TRUE),
       ('kelly_jones', 'kelly.jones@example.com', TRUE),
       ('larry_garcia', 'larry.garcia@example.com', FALSE),
       ('mona_rodriguez', 'mona.rodriguez@example.com', TRUE),
       ('nina_martinez', 'nina.martinez@example.com', TRUE),
       ('oliver_hernandez', 'oliver.hernandez@example.com', FALSE),
       ('pamela_clark', 'pamela.clark@example.com', TRUE),
       ('quincy_lewis', 'quincy.lewis@example.com', TRUE),
       ('rachel_walker', 'rachel.walker@example.com', FALSE),
       ('samuel_hall', 'samuel.hall@example.com', TRUE),
       ('tina_young', 'tina.young@example.com', TRUE),
       ('ursula_king', 'ursula.king@example.com', FALSE),
       ('victor_scott', 'victor.scott@example.com', TRUE),
       ('wendy_adams', 'wendy.adams@example.com', TRUE),
       ('xander_baker', 'xander.baker@example.com', FALSE),
       ('yasmine_nelson', 'yasmine.nelson@example.com', TRUE),
       ('zachary_morris', 'zachary.morris@example.com', TRUE);
