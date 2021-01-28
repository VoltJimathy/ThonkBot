CREATE TABLE IF NOT EXISTS exp(
    UserId integer PRIMARY KEY,
    XP integer DEFAULT 0,
    Level integer DEFAULT 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Mod(
	UserId integer PRIMARY KEY,
	Warns integer DEFAULT 0
);

CREATE  TABLE IF NOT EXISTS Guilds(
    GuildId integer PRIMARY KEY,
    Prefix text DEFAULT "+"
)