''' TABELAS CRIADAS NO MYSQL ''

create table if not exists user_sensors(
	id int(11) primary key not null auto_increment,
	sensor_name varchar(50) not null,
    temperature varchar(50) not null,
    humidity varchar(50) not null,
    date_column DATE not null,
    hour_column varchar(50) not null,
    fk_users int,
	CONSTRAINT fk_users FOREIGN KEY (fk_users) REFERENCES usuarios (id_users)
	)engine=innodb


create table if not exists usuarios(
	id_users int(11) primary key not null auto_increment,
    login varchar(50) UNIQUE not null,
	senha varchar(50) UNIQUE not null
	)engine=innodb;