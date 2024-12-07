const { Client } = require("pg");
console.log(process.env.POSTGRES_HOST);
console.log(process.env.POSTGRES_PORT);
const pgclient = new Client({
  host: process.env.POSTGRES_HOST,
  port: process.env.POSTGRES_PORT,
  user: "postgres",
  password: "huiyang@2013",
  database: "postgres",
});

pgclient.connect();

const table =
  "CREATE TABLE student(id SERIAL PRIMARY KEY, firstName VARCHAR(40) NOT NULL, lastName VARCHAR(40) NOT NULL, age INT, address VARCHAR(80), email VARCHAR(40))";
const text =
  "INSERT INTO student(firstname, lastname, age, address, email) VALUES($1, $2, $3, $4, $5) RETURNING *";
const values = [
  "Mona the",
  "Octocat",
  9,
  "88 Colin P Kelly Jr St, San Francisco, CA 94107, United States",
  "octocat@github.com",
];

pgclient.query(table, (err, res) => {
  if (err) throw err;
});

pgclient.query(text, values, (err, res) => {
  if (err) throw err;
});

pgclient.query("SELECT * FROM student", (err, res) => {
  if (err) throw err;
  console.log(err, res.rows); // Print the data in student table
  pgclient.end();
});
