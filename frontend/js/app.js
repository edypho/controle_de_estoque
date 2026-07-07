document.addEventListener("DOMContentLoaded", async () => {
    carregarProdutos();
});

async function carregarProdutos() {

    const produtos = await listarProdutos();

    const tbody = document.getElementById("produtos");

    tbody.innerHTML = "";

    if(produtos.length === 0){

        tbody.innerHTML = `
            <tr>
                <td colspan="4" style="text-align:center;">
                    Nenhum produto cadastrado.
                </td>
            </tr>
        `;

        return;
    }

    produtos.forEach(produto => {

        tbody.innerHTML += `
            <tr>

                <td>${produto.nome}</td>

                <td>${produto.categoria}</td>

                <td>${produto.quantidade}</td>

                <td>R$ ${Number(produto.preco).toFixed(2)}</td>

            </tr>
        `;

    });

}