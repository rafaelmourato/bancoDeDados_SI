import express from 'express';
import mysql from 'mysql2/promise';
import dotenv from 'dotenv';

dotenv.config();
const app = express();
app.use(express.json());

// Conexão com o banco de dados
const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: process.env.DB_PORT
});

// CRUD para Funcionário
app.post('/funcionarios', async (req, res) => {
  const { CPF, Nome, Idade, Cargo, Salario } = req.body;
  const [result] = await pool.query(
    'INSERT INTO Funcionario (CPF, Nome, Idade, Cargo, Salario) VALUES (?, ?, ?, ?, ?)',
    [CPF, Nome, Idade, Cargo, Salario]
  );
  res.status(201).json({ message: 'Funcionário cadastrado!', CPF });
});

app.get('/funcionarios', async (req, res) => {
  const [rows] = await pool.query('SELECT * FROM Funcionario');
  res.json(rows);
});

app.put('/funcionarios/:cpf', async (req, res) => {
  const { Nome, Idade, Cargo, Salario } = req.body;
  const { cpf } = req.params;
  await pool.query(
    'UPDATE Funcionario SET Nome = ?, Idade = ?, Cargo = ?, Salario = ? WHERE CPF = ?',
    [Nome, Idade, Cargo, Salario, cpf]
  );
  res.json({ message: 'Funcionário atualizado!' });
});

app.delete('/funcionarios/:cpf', async (req, res) => {
  const { cpf } = req.params;
  await pool.query('DELETE FROM Funcionario WHERE CPF = ?', [cpf]);
  res.json({ message: 'Funcionário deletado!' });
});

// CRUD para Cliente
app.post('/clientes', async (req, res) => {
  const { CNPJ, Nome, Setor_Atuacao } = req.body;
  await pool.query(
    'INSERT INTO Cliente (CNPJ, Nome, Setor_Atuacao) VALUES (?, ?, ?)',
    [CNPJ, Nome, Setor_Atuacao]
  );
  res.status(201).json({ message: 'Cliente cadastrado!', CNPJ });
});

app.get('/clientes', async (req, res) => {
  const [rows] = await pool.query('SELECT * FROM Cliente');
  res.json(rows);
});

app.put('/clientes/:cnpj', async (req, res) => {
  const { Nome, Setor_Atuacao } = req.body;
  const { cnpj } = req.params;
  await pool.query(
    'UPDATE Cliente SET Nome = ?, Setor_Atuacao = ? WHERE CNPJ = ?',
    [Nome, Setor_Atuacao, cnpj]
  );
  res.json({ message: 'Cliente atualizado!' });
});

app.delete('/clientes/:cnpj', async (req, res) => {
  const { cnpj } = req.params;
  await pool.query('DELETE FROM Cliente WHERE CNPJ = ?', [cnpj]);
  res.json({ message: 'Cliente deletado!' });
});

// CRUD para Software
app.post('/softwares', async (req, res) => {
  const { Nome, Stack_Tecnologias, Data_Inicio, Data_Entrega, Funcionalidades, Comercial_CPF, Cliente_CNPJ } = req.body;
  const [result] = await pool.query(
    'INSERT INTO Software (Nome, Stack_Tecnologias, Data_Inicio, Data_Entrega, Funcionalidades, Comercial_CPF, Cliente_CNPJ) VALUES (?, ?, ?, ?, ?, ?, ?)',
    [Nome, Stack_Tecnologias, Data_Inicio, Data_Entrega, Funcionalidades, Comercial_CPF, Cliente_CNPJ]
  );
  res.status(201).json({ message: 'Software cadastrado!', Codigo: result.insertId });
});

app.get('/softwares', async (req, res) => {
  const [rows] = await pool.query('SELECT * FROM Software');
  res.json(rows);
});

app.put('/softwares/:codigo', async (req, res) => {
  const { Nome, Stack_Tecnologias, Data_Inicio, Data_Entrega, Funcionalidades } = req.body;
  const { codigo } = req.params;
  await pool.query(
    'UPDATE Software SET Nome = ?, Stack_Tecnologias = ?, Data_Inicio = ?, Data_Entrega = ?, Funcionalidades = ? WHERE Codigo = ?',
    [Nome, Stack_Tecnologias, Data_Inicio, Data_Entrega, Funcionalidades, codigo]
  );
  res.json({ message: 'Software atualizado!' });
});

app.delete('/softwares/:codigo', async (req, res) => {
  const { codigo } = req.params;
  await pool.query('DELETE FROM Software WHERE Codigo = ?', [codigo]);
  res.json({ message: 'Software deletado!' });
});

// Iniciar o servidor
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor rodando em http://localhost:${PORT}`);
});
