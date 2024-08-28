import mysql from 'mysql'

export const db = mysql.createConnection({
    host:'localhost',
    user:'root',
    password:'admin',
    database:'blog',
})

/* recordatorio* agregar columna categoria a tabla posts */ 
/*
    ALTER TABLE `blog`.`posts`
    ADD COLUMN `cat` VARCHAR(45) NULL AFTER `uid`;
*/ 