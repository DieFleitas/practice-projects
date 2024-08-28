//Connect db to server
const Pool = require("pg").Pool;

const pool = new Pool({
  user: "Tu user",
  password: "Tu clave",
  host: "localhost",
  port: 5432,
  database: "Tu db",
});

module.exports = pool;