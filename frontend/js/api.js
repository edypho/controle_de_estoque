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