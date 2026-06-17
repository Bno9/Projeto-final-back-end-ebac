const botao_all_pokeapi = document.getElementById("btn1");
const botao_pokeapi_id = document.getElementById("btn2");
const info_pokemons = document.getElementById("info-pokemons")
const infopokeapi = document.getElementById("infopokeapi");
const id_pokeapi = document.getElementById("id_poke");
const front = document.getElementById("front_img_pokemon");
const back = document.getElementById("back_img_pokemon");
const botao_tema = document.getElementById("botao-tema");
const body = document.body;
const botao_ver_pokemons_criados_pelo_usuario = document.getElementById("get-all-pokemons")
const botao_ver_pokemons_por_nome = document.getElementById("get-pokemon-per-name")
const botao_deletar = document.getElementById("botao-deletar")

botao_tema.addEventListener("click", () => {
    body.classList.toggle("dark-mode")
})

botao_pokeapi_id.addEventListener("click", () => {
    const id = Number(id_pokeapi.value);

    if(id <= 0){
        return;
        }

    fetch(`https://projeto-final-back-end-ebac.onrender.com/pokeapi/${id}`)
        .then(response => response.json())
        .then(data => {
            infopokeapi.textContent = JSON.stringify(data, null, 2);
            infopokeapi.classList.add("info-visible");
            front.src = data.sprites.front_default;
            back.src = data.sprites.back_default;
            front.style.display = "block";
            back.style.display = "block";
        });
});

botao_all_pokeapi.addEventListener("click", () => {

    const limit = document.getElementById("limit");
    const offset = document.getElementById("offset");

    if(limit.value <= 0 || offset < 0){
        infopokeapi.textContent = "Insira um valor maior que 0 para limite e offset"
        return
    }

    fetch(`https://projeto-final-back-end-ebac.onrender.com/pokeapi/all?limit=${limit.value}&offset=${offset.value}`)
        .then(response => response.json())
        .then(data => { 
            infopokeapi.textContent = JSON.stringify(data, null, 2);
            infopokeapi.classList.add("info-visible");
            front.style.display = "none";
            back.style.display = "none";

        });
});

const form = document.getElementById("form-pokemon");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const pokemon = {
        name: document.getElementById("nome").value,
        height: Number(document.getElementById("altura").value),
        weight: Number(document.getElementById("peso").value),
        types: document
            .getElementById("tipos")
            .value
            .split(",")
            .map(tipo => tipo.trim()),
        level: Number(document.getElementById("level").value)
    };

    const response = await fetch("https://projeto-final-back-end-ebac.onrender.com/criar-pokemon", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(pokemon)
    });

    const data = await response.json();

    console.log(data);
});

botao_ver_pokemons_criados_pelo_usuario.addEventListener("click", () => {

    fetch(`https://projeto-final-back-end-ebac.onrender.com/pokemons`)
        .then(response => response.json())
        .then(data => {
            info_pokemons.textContent = JSON.stringify(data, null, 2);
            info_pokemons.classList.add("info-visible")
        });
})

botao_ver_pokemons_por_nome.addEventListener("click", () => {

    const name = document.getElementById("name-get")

    fetch(`https://projeto-final-back-end-ebac.onrender.com/pokemon/${name.value}`)
        .then(response => response.json())
        .then(data => {
            info_pokemons.innerHTML = `<h2>${data.name}</h2>
                <p><strong>Altura:</strong> ${data.height}</p>
                <p><strong>Peso:</strong> ${data.weight}</p>
                <p><strong>Level:</strong> ${data.level}</p>
                <p><strong>Tipos:</strong> ${data.types.join(", ")}</p>
            `;
            info_pokemons.classList.add("info-visible");
        });
})

form_att = document.getElementById("form-atualizar-pokemon")

form_att.addEventListener("submit", async (event) => {
    event.preventDefault();

    const old_name = document.getElementById("nome-pokemon-att")

    const pokemon = {
        name: document.getElementById("nome-att").value,
        height: Number(document.getElementById("altura-att").value),
        weight: Number(document.getElementById("peso-att").value),
        types: document
            .getElementById("tipos-att")
            .value
            .split(",")
            .map(tipo => tipo.trim()),
        level: Number(document.getElementById("level-att").value)
    };

    const response = await fetch(`https://projeto-final-back-end-ebac.onrender.com/atualizar-pokemon/${old_name.value}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(pokemon)
    });

    const data = await response.json();

    console.log(data);
});

botao_deletar.addEventListener("click", async (event) => {
    event.preventDefault();

    const name = document.getElementById("nome-pokemon-delete")

    const response = await fetch(`https://projeto-final-back-end-ebac.onrender.com/deletar-pokemon/${name.value}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        }
    });

    const data = await response.json();

    console.log(data);
});
