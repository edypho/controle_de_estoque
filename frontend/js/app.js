// =========================
// Inicialização
// =========================

document.addEventListener("DOMContentLoaded", async () => {

    await carregarDashboard();

    await carregarProdutos();

});

// =========================
// Produtos Recentes
// =========================

async function carregarProdutos() {

    const produtos = await listarProdutos();
    const categorias = await listarCategorias();

    const mapaCategorias = {};

    categorias.forEach(categoria => {

        mapaCategorias[categoria.id] = categoria.nome;

    });

    const tbody = document.getElementById("ultimosProdutos");

    tbody.innerHTML = "";

    if (produtos.length === 0) {

        tbody.innerHTML = `
            <tr>
                <td colspan="4" style="text-align:center;">
                    Nenhum produto cadastrado.
                </td>
            </tr>
        `;

        return;

    }

    produtos.slice(0, 5).forEach(produto => {

        tbody.innerHTML += `
            <tr>
                <td>${produto.nome}</td>
                <td>${mapaCategorias[produto.categoria_id] || "Sem categoria"}</td>
                <td>${produto.quantidade}</td>
                <td>R$ ${Number(produto.preco).toFixed(2)}</td>
            </tr>
        `;

    });

}

// =========================
// Dashboard
// =========================

async function carregarDashboard() {

    try {

        const produtos = await listarProdutos();
        document.getElementById("totalProdutos").textContent = produtos.length;

        const estoqueBaixo = await listarEstoqueBaixo();
        document.getElementById("estoqueBaixo").textContent = estoqueBaixo.length;

        const dashboard = await listarDashboard();

        document.getElementById("totalEntradas").textContent = dashboard.entradas;
        document.getElementById("totalSaidas").textContent = dashboard.saidas;

    } catch (erro) {

        console.error("Erro ao carregar dashboard:", erro);

    }

}