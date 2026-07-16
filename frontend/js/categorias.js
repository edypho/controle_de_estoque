// =========================
// Inicializacao
// =========================

document.addEventListener("DOMContentLoaded", () => {
    carregarListaCategorias();
});

// =========================
// Elementos da pagina
// =========================

const modalCategoria = document.getElementById("modalCategoria");

const btnNovaCategoria = document.getElementById("btnNovaCategoria");
const btnCancelarCategoria = document.getElementById("cancelarCategoria");
const btnFecharCategoria = document.getElementById("fecharModalCategoria");
const btnSalvarCategoria = document.getElementById("salvarCategoria");

const pesquisaCategoria = document.getElementById("pesquisaCategoria");

// =========================
// Eventos
// =========================

btnNovaCategoria.addEventListener("click", abrirModalCategoria);
btnCancelarCategoria.addEventListener("click", fecharModalCategoria);
btnFecharCategoria.addEventListener("click", fecharModalCategoria);
btnSalvarCategoria.addEventListener("click", salvarNovaCategoria);

pesquisaCategoria.addEventListener("input", pesquisarCategorias);

modalCategoria.addEventListener("click", (e) => {

    if (e.target === modalCategoria) {

        fecharModalCategoria();

    }

});

// =========================
// Categorias
// =========================

async function carregarListaCategorias() {

    const tbody = document.getElementById("categorias");

    tbody.innerHTML = "";

    try {

        const categorias = await listarCategorias();

        if (categorias.length === 0) {

            tbody.innerHTML = `
                <tr>
                    <td colspan="3" style="text-align:center;">
                        Nenhuma categoria cadastrada.
                    </td>
                </tr>
            `;

            return;

        }

        categorias.forEach(categoria => {

            tbody.innerHTML += `
                <tr>
                    <td>${categoria.id}</td>
                    <td>${categoria.nome}</td>
                    <td>${categoria.descricao || "-"}</td>
                </tr>
            `;

        });

    } catch (erro) {

        console.error(erro);

    }

}

// =========================
// Modal
// =========================

function abrirModalCategoria() {

    modalCategoria.classList.remove("hidden");

}

function fecharModalCategoria() {

    modalCategoria.classList.add("hidden");

}

// =========================
// Cadastro
// =========================

async function salvarNovaCategoria() {

    const categoria = {

        nome: document.getElementById("nomeCategoria").value.trim(),

        descricao: document.getElementById("descricaoCategoria").value.trim()

    };

    if (!categoria.nome) {

        alert("Informe o nome da categoria.");

        return;

    }

    try {

        await cadastrarCategoria(categoria);

        fecharModalCategoria();

        limparFormularioCategoria();

        await carregarListaCategorias();

        alert("Categoria cadastrada com sucesso!");

    } catch (erro) {

        alert(erro.message);

    }

}

// =========================
// Pesquisa
// =========================

function pesquisarCategorias() {

    const texto = pesquisaCategoria.value.toLowerCase();

    document.querySelectorAll("#categorias tr").forEach(linha => {

        const nome = linha.children[1].textContent.toLowerCase();

        linha.style.display = nome.includes(texto)
            ? ""
            : "none";

    });

}

// =========================
// Utilidades
// =========================

function limparFormularioCategoria() {

    document.getElementById("nomeCategoria").value = "";

    document.getElementById("descricaoCategoria").value = "";

}
