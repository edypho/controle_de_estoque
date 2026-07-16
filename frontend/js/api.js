const API_URL = "http://127.0.0.1:5000";

async function listarProdutos() {

    const resposta = await fetch(`${API_URL}/produtos`);

    if (!resposta.ok) {
        throw new Error("Erro ao buscar produtos.");
    }

    return await resposta.json();

}

async function listarCategorias() {

    const resposta = await fetch(`${API_URL}/categorias`);

    if (!resposta.ok) {

        throw new Error("Erro ao buscar categorias.");

    }

    return await resposta.json();

}

async function cadastrarProduto(produto) {

    const resposta = await fetch(`${API_URL}/produtos`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(produto)

    });

    const dados = await resposta.json();

    if (!resposta.ok) {

        throw new Error(dados.erro || "Erro ao cadastrar produto.");

    }

    return dados;

}

async function excluirProduto(id) {

    const resposta = await fetch(`${API_URL}/produtos/${id}`, {
        method: "DELETE"
    });

    const dados = await resposta.json();

    if (!resposta.ok) {
        throw new Error(dados.erro || "Erro ao excluir produto.");
    }

    return dados;

}

async function registrarEntrada(id, dados) {

    const resposta = await fetch(`${API_URL}/produtos/${id}/entrada`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(dados)

    });

    const retorno = await resposta.json();

    if (!resposta.ok) {
        throw new Error(retorno.erro || "Erro ao registrar entrada.");
    }

    return retorno;

}

async function registrarSaida(id, dados) {

    const resposta = await fetch(`${API_URL}/produtos/${id}/saida`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(dados)

    });

    const retorno = await resposta.json();

    if (!resposta.ok) {
        throw new Error(retorno.erro || "Erro ao registrar saída.");
    }

    return retorno;

}

async function listarEstoqueBaixo() {

    const resposta = await fetch(`${API_URL}/produtos-estoque-baixo`);

    if (!resposta.ok) {
        throw new Error("Erro ao buscar produtos com estoque baixo.");
    }

    return await resposta.json();

}

async function listarDashboard() {

    const resposta = await fetch(`${API_URL}/dashboard`);

    if (!resposta.ok) {
        throw new Error("Erro ao carregar dashboard.");
    }

    return await resposta.json();

}