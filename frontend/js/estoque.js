let produtoSelecionado = null;
let tipoMovimentacao = null;

const modalMovimentacao = document.getElementById("modalMovimentacao");
const tituloMovimentacao = document.getElementById("tituloMovimentacao");

function abrirModalMovimentacao(id, tipo) {

    produtoSelecionado = id;
    tipoMovimentacao = tipo;

    tituloMovimentacao.textContent =
        tipo === "entrada"
            ? "Entrada de Estoque"
            : "Saída de Estoque";

    document.getElementById("quantidadeMovimentacao").value = "";
    document.getElementById("observacaoMovimentacao").value = "";

    modalMovimentacao.classList.remove("hidden");

}

function fecharModalMovimentacao() {

    modalMovimentacao.classList.add("hidden");

}

document
    .getElementById("cancelarMovimentacao")
    .addEventListener("click", fecharModalMovimentacao);

    const btnConfirmar = document.getElementById("confirmarMovimentacao");

btnConfirmar.addEventListener("click", salvarMovimentacao);

async function salvarMovimentacao() {

    const quantidade = Number(
        document.getElementById("quantidadeMovimentacao").value
    );

    const observacao = document
        .getElementById("observacaoMovimentacao")
        .value
        .trim();

    if (quantidade <= 0) {

        alert("Informe uma quantidade válida.");

        return;

    }

    try {

        if (tipoMovimentacao === "entrada") {

            await registrarEntrada(produtoSelecionado, {
                quantidade,
                observacao
            });

        } else {

            await registrarSaida(produtoSelecionado, {
                quantidade,
                observacao
            });

        }

        fecharModalMovimentacao();

        await carregarProdutos();

        alert(
            tipoMovimentacao === "entrada"
                ? "Entrada registrada com sucesso!"
                : "Saída registrada com sucesso!"
        );

    } catch (erro) {

        alert(erro.message);

    }

}

const btnFecharMovimentacao = document.getElementById("fecharMovimentacao");

btnFecharMovimentacao.addEventListener("click", () => {
    fecharModalMovimentacao();
});

modalMovimentacao.addEventListener("click", (e) => {

    if (e.target === modalMovimentacao) {

        fecharModalMovimentacao();

    }

});