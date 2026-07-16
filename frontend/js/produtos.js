// =========================
// Inicialização
// =========================

document.addEventListener("DOMContentLoaded", () => {
    carregarProdutos();
});

// =========================
// Elementos da página
// =========================

const modal = document.getElementById("modalProduto");

const btnNovoProduto = document.getElementById("btnNovoProduto");
const btnCancelar = document.getElementById("cancelarProduto");
const btnFechar = document.getElementById("fecharModal");
const btnSalvar = document.getElementById("salvarProduto");

const campoPesquisa = document.getElementById("pesquisa");

// =========================
// Eventos
// =========================

btnNovoProduto.addEventListener("click", abrirModal);
btnCancelar.addEventListener("click", fecharModal);
btnFechar.addEventListener("click", fecharModal);
btnSalvar.addEventListener("click", salvarProduto);

campoPesquisa.addEventListener("input", pesquisarProdutos);

modal.addEventListener("click", (e) => {
    if (e.target === modal) {
        fecharModal();
    }
});

// =========================
// Produtos
// =========================

async function carregarProdutos() {

    const tbody = document.getElementById("produtos");
    tbody.innerHTML = "";

    try {

        const categorias = await listarCategorias();
        const produtos = await listarProdutos();

        if (produtos.length === 0) {

            tbody.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align:center;">
                        Nenhum produto cadastrado.
                    </td>
                </tr>
            `;

            return;
        }

        const mapaCategorias = {};

        categorias.forEach(categoria => {
            mapaCategorias[categoria.id] = categoria.nome;
        });

        produtos.forEach(produto => {

            tbody.innerHTML += `
                <tr>

                    <td>${produto.id}</td>

                    <td>${produto.nome}</td>

                    <td>${mapaCategorias[produto.categoria_id] || "Sem categoria"}</td>

                    <td class="${
                        produto.quantidade <= produto.estoque_minimo
                            ? "estoque-baixo"
                            : ""
                    }">
                        ${
                            produto.quantidade <= produto.estoque_minimo
                                ? "⚠ " + produto.quantidade
                                : produto.quantidade
                        }
                    </td>

                    <td>R$ ${Number(produto.preco).toFixed(2)}</td>

                    <td>

                        <button class="btnEntrada"
                            data-id="${produto.id}"
                            title="Entrada">

                            <i class="fa-solid fa-plus"></i>

                        </button>

                        <button class="btnSaida"
                            data-id="${produto.id}"
                            title="Saída">

                            <i class="fa-solid fa-minus"></i>

                        </button>

                        <button class="btnHistorico"
                            data-id="${produto.id}"
                            title="Historico">

                            <i class="fa-solid fa-clock-rotate-left"></i>

                        </button>

                        <button class="btnExcluir"
                            data-id="${produto.id}"
                            title="Excluir">

                            <i class="fa-solid fa-trash"></i>

                        </button>

                    </td>

                </tr>
            `;

        });

        adicionarEventos();

    } catch (erro) {

        console.error(erro);

    }

}

// =========================
// Eventos dos botões
// =========================

function adicionarEventos() {

    document.querySelectorAll(".btnExcluir").forEach(botao => {

        botao.addEventListener("click", () => {

            confirmarExclusao(botao.dataset.id);

        });

    });

    document.querySelectorAll(".btnEntrada").forEach(botao => {

        botao.addEventListener("click", () => {

            abrirModalMovimentacao(botao.dataset.id, "entrada");

        });

    });

    document.querySelectorAll(".btnSaida").forEach(botao => {

        botao.addEventListener("click", () => {

            abrirModalMovimentacao(botao.dataset.id, "saida");

        });

    });

    document.querySelectorAll(".btnHistorico").forEach(botao => {

        botao.addEventListener("click", () => {

            abrirHistorico(botao.dataset.id);

        });

    });

}

// =========================
// Historico
// =========================

const modalHistorico = document.getElementById("modalHistorico");
const btnFecharHistorico = document.getElementById("fecharHistorico");

async function abrirHistorico(id) {

    const tbody = document.getElementById("historicoProduto");

    tbody.innerHTML = "";

    try {

        const movimentacoes = await listarHistoricoProduto(id);

        if (movimentacoes.length === 0) {

            tbody.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align:center;">
                        Nenhuma movimentacao registrada.
                    </td>
                </tr>
            `;

        } else {

            movimentacoes.forEach(movimentacao => {

                tbody.innerHTML += `
                    <tr>
                        <td>${movimentacao.tipo}</td>
                        <td>${movimentacao.quantidade}</td>
                        <td>${movimentacao.saldo_anterior}</td>
                        <td>${movimentacao.saldo_atual}</td>
                        <td>${movimentacao.observacao || "-"}</td>
                        <td>${movimentacao.data_hora}</td>
                    </tr>
                `;

            });

        }

        modalHistorico.classList.remove("hidden");

    } catch (erro) {

        alert(erro.message);

    }

}

function fecharHistorico() {

    modalHistorico.classList.add("hidden");

}

btnFecharHistorico.addEventListener("click", fecharHistorico);

modalHistorico.addEventListener("click", (e) => {

    if (e.target === modalHistorico) {

        fecharHistorico();

    }

});

// =========================
// Categorias
// =========================

async function carregarCategorias() {

    const select = document.getElementById("categoriaProduto");

    try {

        select.innerHTML = "<option>Carregando...</option>";

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

// =========================
// Modal
// =========================

function abrirModal() {

    modal.classList.remove("hidden");

    carregarCategorias();

}

function fecharModal() {

    modal.classList.add("hidden");

}

// =========================
// Cadastro
// =========================

async function salvarProduto() {

    const produto = {

        nome: document.getElementById("nomeProduto").value.trim(),

        categoria_id: Number(document.getElementById("categoriaProduto").value),

        preco: Number(document.getElementById("precoProduto").value),

        quantidade: Number(document.getElementById("quantidadeProduto").value),

        estoque_minimo: Number(document.getElementById("estoqueMinimo").value)

    };

    if (!produto.nome) {

        alert("Informe o nome do produto.");

        return;

    }

    try {

        await cadastrarProduto(produto);

        fecharModal();

        limparFormulario();

        await carregarProdutos();

        alert("Produto cadastrado com sucesso!");

    } catch (erro) {

        alert(erro.message);

    }

}

// =========================
// Exclusão
// =========================

async function confirmarExclusao(id) {

    if (!window.confirm("Deseja realmente excluir este produto?")) {
        return;
    }

    try {

        await excluirProduto(id);

        await carregarProdutos();

        alert("Produto removido com sucesso!");

    } catch (erro) {

        console.error(erro);

        alert(erro.message);

    }

}

// =========================
// Pesquisa
// =========================

function pesquisarProdutos() {

    const texto = campoPesquisa.value.toLowerCase();

    document.querySelectorAll("#produtos tr").forEach(linha => {

        const nome = linha.children[1].textContent.toLowerCase();

        linha.style.display = nome.includes(texto)
            ? ""
            : "none";

    });

}

// =========================
// Utilidades
// =========================

function limparFormulario() {

    document.getElementById("nomeProduto").value = "";

    document.getElementById("categoriaProduto").selectedIndex = 0;

    document.getElementById("precoProduto").value = "";

    document.getElementById("quantidadeProduto").value = "";

    document.getElementById("estoqueMinimo").value = "";

}
