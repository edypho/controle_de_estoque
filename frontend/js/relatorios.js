// =========================
// Inicializacao
// =========================

document.addEventListener("DOMContentLoaded", async () => {

    await carregarRelatorioEstoque();

    await carregarRelatorioMovimentacoes();

});

// =========================
// Relatorio de estoque
// =========================

async function carregarRelatorioEstoque() {

    const tbody = document.getElementById("relatorioEstoque");

    tbody.innerHTML = "";

    try {

        const estoque = await listarRelatorioEstoque();

        if (estoque.length === 0) {

            tbody.innerHTML = `
                <tr>
                    <td colspan="5" style="text-align:center;">
                        Nenhum produto cadastrado.
                    </td>
                </tr>
            `;

            return;

        }

        estoque.forEach(produto => {

            tbody.innerHTML += `
                <tr>
                    <td>${produto.nome}</td>
                    <td>${produto.quantidade}</td>
                    <td>R$ ${Number(produto.preco).toFixed(2)}</td>
                    <td>R$ ${Number(produto.valor_total).toFixed(2)}</td>
                    <td class="${produto.abaixo_do_minimo ? "estoque-baixo" : ""}">
                        ${produto.abaixo_do_minimo ? "Estoque baixo" : "Normal"}
                    </td>
                </tr>
            `;

        });

    } catch (erro) {

        console.error(erro);

    }

}

// =========================
// Relatorio de movimentacoes
// =========================

async function carregarRelatorioMovimentacoes() {

    const tbody = document.getElementById("relatorioMovimentacoes");

    tbody.innerHTML = "";

    try {

        const produtos = await listarProdutos();
        const movimentacoes = await listarRelatorioMovimentacoes();

        const mapaProdutos = {};

        produtos.forEach(produto => {

            mapaProdutos[produto.id] = produto.nome;

        });

        if (movimentacoes.length === 0) {

            tbody.innerHTML = `
                <tr>
                    <td colspan="7" style="text-align:center;">
                        Nenhuma movimentacao registrada.
                    </td>
                </tr>
            `;

            return;

        }

        movimentacoes.forEach(movimentacao => {

            tbody.innerHTML += `
                <tr>
                    <td>${mapaProdutos[movimentacao.produto_id] || "Produto nao encontrado"}</td>
                    <td>${movimentacao.tipo}</td>
                    <td>${movimentacao.quantidade}</td>
                    <td>${movimentacao.saldo_anterior}</td>
                    <td>${movimentacao.saldo_atual}</td>
                    <td>${movimentacao.observacao || "-"}</td>
                    <td>${movimentacao.data_hora}</td>
                </tr>
            `;

        });

    } catch (erro) {

        console.error(erro);

    }

}
