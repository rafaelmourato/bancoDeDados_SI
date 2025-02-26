const express = require("express");
const mysql = require("mysql2");
const dotenv = require("dotenv");

dotenv.config();

const app = express();
app.use(express.json());

const db = mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    port: process.env.DB_PORT
});

db.connect((err) => {
    if (err) {
        console.error("Erro ao conectar ao MySQL:", err);
    } else {
        console.log("Conectado ao MySQL!");
    }
});

//Funcionário
// Create - Criar o Funcionários
app.post("/funcionarios", (req, res) => {
    const { CPF, Nome, Idade, Cargo, Salario } = req.body;
    db.query(
        "INSERT INTO Funcionario (CPF, Nome, Idade, Cargo, Salario) VALUES (?, ?, ?, ?, ?)",
        [CPF, Nome, Idade, Cargo, Salario],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            res.status(201).json({ mensagem: "Funcionário criado!", id: result.insertId });
        }
    );
});
// Read - Listar todos os Funcionários
app.get("/funcionarios", (req, res) => {
    db.query("SELECT * FROM Funcionario", (err, results) => {
        if (err) return res.status(500).json({ erro: err.message });
        res.status(200).json(results);
    });
});
// Update - Atualizar Funcionário
app.put("/funcionarios/:CPF", (req, res) => {
    const { CPF } = req.params;
    const { Nome, Idade, Cargo, Salario } = req.body;
    db.query(
        "UPDATE Funcionario SET Nome = ?, Idade = ?, Cargo = ?, Salario = ? WHERE CPF = ?",
        [Nome, Idade, Cargo, Salario, CPF],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            if (result.affectedRows === 0) return res.status(404).json({ mensagem: "Funcionário não encontrado" });
            res.status(200).json({ mensagem: "Funcionário atualizado!" });
        }
    );
});
// Delete - Excluir Funcionário
app.delete("/funcionarios/:CPF", (req, res) => {
    const { CPF } = req.params;
    db.query("DELETE FROM Funcionario WHERE CPF = ?", [CPF], (err, result) => {
        if (err) return res.status(500).json({ erro: err.message });
        if (result.affectedRows === 0) return res.status(404).json({ mensagem: "Funcionário não encontrado" });
        res.status(200).json({ mensagem: "Funcionário excluído!" });
    });
});

//Designer
// Post
app.post("/designers", (req, res) => {
    const { CPF, Biblioteca_Designs } = req.body;
    db.query(
        "INSERT INTO Designer (CPF, Biblioteca_Designs) VALUES (?, ?)",
        [CPF, Biblioteca_Designs],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            res.status(201).json({ mensagem: "Designer criado!", id: result.insertId });
        }
    );
});
// Read 
app.get("/designers", (req, res) => {
    db.query("SELECT * FROM Designer", (err, results) => {
        if (err) return res.status(500).json({ erro: err.message });
        res.status(200).json(results);
    });
});
// Update 
app.put("/designers/:CPF", (req, res) => {
    const { CPF } = req.params;
    const { Biblioteca_Designs } = req.body;
    db.query(
        "UPDATE Funcionario SET Biblioteca_Designs = ? WHERE CPF = ?",
        [Biblioteca_Designs, CPF],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            if (result.affectedRows === 0) return res.status(404).json({ mensagem: "Designer não encontrado" });
            res.status(200).json({ mensagem: "Designer atualizado!" });
        }
    );
});
// Delete 
app.delete("/designers/:CPF", (req, res) => {
    const { CPF } = req.params;
    db.query("DELETE FROM Designer WHERE CPF = ?", [CPF], (err, result) => {
        if (err) return res.status(500).json({ erro: err.message });
        if (result.affectedRows === 0) return res.status(404).json({ mensagem: "Designer não encontrado" });
        res.status(200).json({ mensagem: "Designer excluído!" });
    });
});

// Desenvolvedor
// Post
app.post("/desenvolvedores", (req, res) => {
    const { CPF, Stack } = req.body;
    db.query(
        "INSERT INTO DesenvolvedorSoftware (CPF, Stack) VALUES (?, ?)",
        [CPF, Stack],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            res.status(201).json({ mensagem: "Desenvolvedor criado!", id: result.insertId });
        }
    );
});
// Read 
app.get("/desenvolvedores", (req, res) => {
    db.query("SELECT * FROM DesenvolvedorSoftware", (err, results) => {
        if (err) return res.status(500).json({ erro: err.message });
        res.status(200).json(results);
    });
});
// Update 
app.put("/desenvolvedores/:CPF", (req, res) => {
    const { CPF } = req.params;
    const { Stack } = req.body;
    db.query(
        "UPDATE DesenvolvedorSoftware SET Biblioteca_Designs = ? WHERE CPF = ?",
        [Stack, CPF],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            if (result.affectedRows === 0) return res.status(404).json({ mensagem: "Designer não encontrado" });
            res.status(200).json({ mensagem: "Designer atualizado!" });
        }
    );
});
// Delete 
app.delete("/desenvolvedores/:CPF", (req, res) => {
    const { CPF } = req.params;
    db.query("DELETE FROM DesenvolvedorSoftware WHERE CPF = ?", [CPF], (err, result) => {
        if (err) return res.status(500).json({ erro: err.message });
        if (result.affectedRows === 0) return res.status(404).json({ mensagem: "Designer não encontrado" });
        res.status(200).json({ mensagem: "Designer excluído!" });
    });
});

//Comerciais
// Post
app.post("/comerciais", (req, res) => {
    const { CPF, Nivel_Persuasao } = req.body;
    db.query(
        "INSERT INTO Comercial (CPF, Nivel_Persuasao) VALUES (?, ?)",
        [CPF, Nivel_Persuasao],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            res.status(201).json({ mensagem: "Comercial criado!", id: result.insertId });
        }
    );
});
// Read 
app.get("/comerciais", (req, res) => {
    db.query("SELECT * FROM Comercial", (err, results) => {
        if (err) return res.status(500).json({ erro: err.message });
        res.status(200).json(results);
    });
});
// Update 
app.put("/comerciais/:CPF", (req, res) => {
    const { CPF } = req.params;
    const { Nivel_Persuasao } = req.body;
    db.query(
        "UPDATE Comercial SET Nivel_Persuasao = ? WHERE CPF = ?",
        [Nivel_Persuasao, CPF],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            if (result.affectedRows === 0) return res.status(404).json({ mensagem: "Comercial não encontrado" });
            res.status(200).json({ mensagem: "Comercial atualizado!" });
        }
    );
});
// Delete 
app.delete("/comerciais/:CPF", (req, res) => {
    const { CPF } = req.params;
    db.query("DELETE FROM Comercial WHERE CPF = ?", [CPF], (err, result) => {
        if (err) return res.status(500).json({ erro: err.message });
        if (result.affectedRows === 0) return res.status(404).json({ mensagem: "Designer não encontrado" });
        res.status(200).json({ mensagem: "Comercial excluído!" });
    });
});

// Clientes
// Post
app.post("/clientes", (req, res) => {
    const { CNPJ, Nome, Setor_Atuacao } = req.body;
    db.query(
        "INSERT INTO Cliente (CNPJ, Nome, Setor_Atuacao) VALUES (?, ?, ?)",
        [CNPJ, Nome, Setor_Atuacao],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            res.status(201).json({ mensagem: "Cliente criado!", id: result.insertId });
        }
    );
});
// Read 
app.get("/clientes", (req, res) => {
    db.query("SELECT * FROM Cliente", (err, results) => {
        if (err) return res.status(500).json({ erro: err.message });
        res.status(200).json(results);
    });
});
// Update 
app.put("/clientes/:CNPJ", (req, res) => {
    const { CNPJ } = req.params;
    const { Nome, Setor_Atuacao } = req.body;
    db.query(
        "UPDATE Cliente SET Biblioteca_Designs = ? WHERE CNPJ = ?",
        [Nome, Setor_Atuacao, CNPJ],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            if (result.affectedRows === 0) return res.status(404).json({ mensagem: "Cliente não encontrado" });
            res.status(200).json({ mensagem: "Cliente atualizado!" });
        }
    );
});
// Delete 
app.delete("/clientes/:CNPJ", (req, res) => {
    const { CNPJ } = req.params;
    db.query("DELETE FROM Cliente WHERE CNPJ = ?", [CNPJ], (err, result) => {
        if (err) return res.status(500).json({ erro: err.message });
        if (result.affectedRows === 0) return res.status(404).json({ mensagem: "Cliente não encontrado" });
        res.status(200).json({ mensagem: "Cliente excluído!" });
    });
});

//Software
// Post
app.post("/softwares", (req, res) => {
    const { Nome, Stack_Tecnologias, Data_Inicio, Data_Entrega, Funcionalidades, Comercial_CPF, Cliente_CNPJ } = req.body;
    db.query(
        "INSERT INTO Software (Nome, Stack_Tecnologias, Data_Inicio, Data_Entrega, Funcionalidades, Comercial_CPF, Cliente_CNPJ) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [Nome, Stack_Tecnologias, Data_Inicio, Data_Entrega, Funcionalidades, Comercial_CPF, Cliente_CNPJ],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            res.status(201).json({ mensagem: "Software criado!", id: result.insertId });
        }
    );
});
// Read 
app.get("/softwares", (req, res) => {
    db.query("SELECT * FROM Software", (err, results) => {
        if (err) return res.status(500).json({ erro: err.message });
        res.status(200).json(results);
    });
});
// Update 
app.put("/softwares/:Codigo", (req, res) => {
    const { Codigo } = req.params;
    const { Nome, Stack_Tecnologias, Data_Inicio, Data_Entrega, Funcionalidades } = req.body;
    db.query(
        "UPDATE Software SET Nome = ?, Stack_Tecnologias = ?, Data_Inicio = ?, Data_Entrega = ?, Funcionalidades = ? WHERE Codigo = ?",
        [Nome, Stack_Tecnologias, Data_Inicio, Data_Entrega, Funcionalidades, Codigo],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            if (result.affectedRows === 0) return res.status(404).json({ mensagem: "Software não encontrado" });
            res.status(200).json({ mensagem: "Software atualizado!" });
        }
    );
});
// Delete 
app.delete("/softwares/:Codigo", (req, res) => {
    const { Codigo } = req.params;
    db.query("DELETE FROM Software WHERE Codigo = ?", [Codigo], (err, result) => {
        if (err) return res.status(500).json({ erro: err.message });
        if (result.affectedRows === 0) return res.status(404).json({ mensagem: "Software não encontrado" });
        res.status(200).json({ mensagem: "Software excluído!" });
    });
});

// Desenvolvimento de Software
// Post (Relação N:N)
app.post("/desenvolvimento-software", (req, res) => {
    const { Desenvolvedor_CPF, Software_Codigo } = req.body;
    db.query(
        "INSERT INTO DesenvolvimentoSoftware (Desenvolvedor_CPF, Software_Codigo) VALUES (?, ?)",
        [Desenvolvedor_CPF, Software_Codigo],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            res.status(201).json({ mensagem: "Relação de desenvolvimento criada!" });
        }
    );
});
// Read 
app.get("/desenvolvimento-software", (req, res) => {
    db.query("SELECT * FROM DesenvolvimentoSoftware", (err, results) => {
        if (err) return res.status(500).json({ erro: err.message });
        res.status(200).json(results);
    });
});
// Update 
app.put("/desenvolvimento-software", (req, res) => {
    const { Desenvolvedor_CPF_Antigo, Software_Codigo_Antigo, Desenvolvedor_CPF_Novo, Software_Codigo_Novo } = req.body;
    db.query(
        "UPDATE DesenvolvimentoSoftware SET Desenvolvedor_CPF = ?, Software_Codigo = ? WHERE Desenvolvedor_CPF = ? AND Software_Codigo = ?",
        [Desenvolvedor_CPF_Novo, Software_Codigo_Novo, Desenvolvedor_CPF_Antigo, Software_Codigo_Antigo],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            if (result.affectedRows === 0) return res.status(404).json({ mensagem: "Relação não encontrada" });
            res.status(200).json({ mensagem: "Relação de desenvolvimento atualizada!" });
        }
    );
});
// Delete 
app.delete("/desenvolvimento-software", (req, res) => {
    const { Desenvolvedor_CPF, Software_Codigo } = req.body;
    db.query(
        "DELETE FROM DesenvolvimentoSoftware WHERE Desenvolvedor_CPF = ? AND Software_Codigo = ?",
        [Desenvolvedor_CPF, Software_Codigo],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            if (result.affectedRows === 0) return res.status(404).json({ mensagem: "Relação não encontrada" });
            res.status(200).json({ mensagem: "Relação removida!" });
        }
    );
});

// Idealização de Software
// Post (Relação N:N)
app.post("/idealizacao-software", (req, res) => {
    const { Designer_CPF, Software_Codigo } = req.body;
    db.query(
        "INSERT INTO IdealizacaoSoftware (Designer_CPF, Software_Codigo) VALUES (?, ?)",
        [Designer_CPF, Software_Codigo],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            res.status(201).json({ mensagem: "Relação de idealização criada!" });
        }
    );
});
// Read 
app.get("/idealizacao-software", (req, res) => {
    db.query("SELECT * FROM IdealizacaoSoftware", (err, results) => {
        if (err) return res.status(500).json({ erro: err.message });
        res.status(200).json(results);
    });
});
// Update 
app.put("/idealizacao-software", (req, res) => {
    const { Designer_CPF_Antigo, Software_Codigo_Antigo, Designer_CPF_Novo, Software_Codigo_Novo } = req.body;
    db.query(
        "UPDATE IdealizacaoSoftware SET Designer_CPF = ?, Software_Codigo = ? WHERE Designer_CPF = ? AND Software_Codigo = ?",
        [Designer_CPF_Novo, Software_Codigo_Novo, Designer_CPF_Antigo, Software_Codigo_Antigo],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            if (result.affectedRows === 0) return res.status(404).json({ mensagem: "Relação não encontrada" });
            res.status(200).json({ mensagem: "Relação de idealização atualizada!" });
        }
    );
});
// Delete 
app.delete("/idealizacao-software", (req, res) => {
    const { Designer_CPF, Software_Codigo } = req.body;

    db.query(
        "DELETE FROM IdealizacaoSoftware WHERE Designer_CPF = ? AND Software_Codigo = ?",
        [Designer_CPF, Software_Codigo],
        (err, result) => {
            if (err) return res.status(500).json({ erro: err.message });
            if (result.affectedRows === 0) return res.status(404).json({ mensagem: "Relação não encontrada" });
            res.status(200).json({ mensagem: "Relação de idealização removida!" });
        }
    );
});

// Inicia o servidor
const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`🚀 Servidor rodando em http://localhost:${port}`);
});
