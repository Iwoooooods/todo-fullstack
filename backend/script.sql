USE todo_app;
create table tasks
(
    id           bigint unsigned auto_increment
        primary key,
    created_at   timestamp  default CURRENT_TIMESTAMP null,
    updated_at   timestamp                            null on update CURRENT_TIMESTAMP,
    title        varchar(255)                         not null,
    brief        varchar(255)                         null,
    content      text                                 null,
    is_completed tinyint(1) default 0                 null,
    deadline     datetime(6)                          null,
    user_id      bigint                               not null,
    parent_id    bigint                               null
);

create index idx_user_id
    on tasks (user_id);

create table users
(
    id              int auto_increment
        primary key,
    created_at      datetime(6) default CURRENT_TIMESTAMP(6) null,
    updated_at      datetime(6)                              null on update CURRENT_TIMESTAMP(6),
    username        varchar(50)                              not null,
    email           varchar(50)                              null,
    hashed_password varchar(512)                             not null,
    disabled        tinyint(1)  default 1                    not null,
    constraint email
        unique (email),
    constraint username
        unique (username),
    constraint users_pk
        unique (email)
);