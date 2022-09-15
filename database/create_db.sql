create database business_db;

use business_db;

create table owners(
	email varchar(255) primary key,
    categories varchar(255),
    info varchar(255)
);

create table users(
	id int not null primary key auto_increment,
    owner varchar(255),
    name varchar(255),
    email varchar(255) unique,
    city varchar(255),
    zip_code varchar(255),
    phone varchar(50),
    img_url Text,
    pass_hash varchar(255),
    type BIT,
    foreign key (owner) references owners(email)
);


create table items(
	id int not null primary key auto_increment,
	img_url Text,
    owner varchar(255),
    name varchar(255),
    price int,
    info varchar(255),
    foreign key (owner) references owners(email)
);

create table likes(
    id int primary key auto_increment,
    customer_email varchar(255),
    business_email varchar(255),
    foreign key (customer_email) references users(email),
    foreign key (business_email) references owners(email)
);

create table gallery(
    id int primary key auto_increment,
    owner_email  varchar(255),
    img varchar(255),
    description varchar(255),
    foreign key (owner_email) references owners(email)
);

create table comment(
    id int primary key auto_increment,
    business_email  varchar(255),
    customer_email varchar(255),
    comment varchar(255),
    foreign key (business_email) references owners(email),
    foreign key (customer_email) references users(email)
);