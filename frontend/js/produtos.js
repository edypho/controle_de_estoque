document.addEventListener("DOMContentLoaded", carregarProdutos);

async function carregarProdutos() {

    const tbody = document.getElementById("produtos");

    tbody.innerHTML = "";

    try {

        const produtos = await listarProdutos();

        if (produtos.length === 0) {

            tbody.innerHTML = `
                <tr>
                    <td colspan="5" style="text-align:center;">
                        Nenhum produto cadastrado.
                    </td>
                </tr>
            `;

            return;

        }

        produtos.forEach(produto => {

            tbody.innerHTML += `
                <tr>
                    <td>${produto.id}</td>
                    <td>${produto.nome}</td>
                    <td>${produto.categoria_id}</td>
                    <td>${produto.quantidade}</td>
                    <td>R$ ${Number(produto.preco).toFixed(2)}</td>

                    <td>

                        <button class="btnExcluir" data-id="${produto.id}">
                            <i class="fa-solid fa-trash"></i>
                        </button>

                    </td>
                </tr>
            `;

        });

    } catch (erro) {

        console.error(erro);

        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align:center;color:red;">
                    Erro ao carregar os produtos.
                </td>
            </tr>
        `;

    }

}

const btnNovoProduto = document.getElementById("btnNovoProduto");

btnNovoProduto.addEventListener("click", () => {
    const modal = document.getElementById("modalProduto");

    const btnNovoProduto = document.getElementById("btnNovoProduto");

    const btnCancelar = document.getElementById("cancelarProduto");

    btnNovoProduto.addEventListener("click", async () => {

        await carregarCategorias();
    
        modal.classList.remove("hidden");
    
    });

    btnCancelar.addEventListener("click", () => {

        modal.classList.add("hidden");

    });
});

async function carregarCategorias() {

    const select = document.getElementById("categoriaProduto");

    try {

        const categorias = await listarCategorias();

        select.innerHTML = "";

        categorias.forEach(categoria => {

            select.innerHTML += `
                <option value="${categoria.id}">
                    ${categoria.nome}
                </option>
            `;

        });

    } catch (erro) {

        console.error(erro);

    }

}