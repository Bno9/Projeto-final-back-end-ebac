const botao_all_pokeapi = document.getElementById("btn1");
const botao_pokeapi_id = document.getElementById("btn2");
const info_pokemons = document.getElementById("info-pokemons");
const infopokeapi = document.getElementById("infopokeapi");
const id_pokeapi = document.getElementById("id_poke");
const front = document.getElementById("front_img_pokemon");
const back = document.getElementById("back_img_pokemon");
const botao_tema = document.getElementById("botao-tema");
const body = document.body;
const botao_ver_pokemons_criados_pelo_usuario = document.getElementById("get-all-pokemons");
const botao_ver_pokemons_por_nome = document.getElementById("get-pokemon-per-name");
const botao_deletar = document.getElementById("botao-deletar");
const resposta_api = document.getElementById("resposta-api");
const form = document.getElementById("form-pokemon");
const form_att = document.getElementById("form-atualizar-pokemon");

//botão pra alterar tema do navegador
botao_tema.addEventListener("click", () => {
    body.classList.toggle("dark-mode");
})

//botão que pesquisa um pokemon por id na pokeapi
botao_pokeapi_id.addEventListener("click", async () => {
    try {
        const id = Number(id_pokeapi.value);

        if (id <= 0) {
            throw new Error("ID inválido");
        }

        const response = await fetch(
            `https://projeto-final-back-end-ebac.onrender.com/pokeapi/${id}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Erro ao buscar Pokémon");
        }

        infopokeapi.textContent = JSON.stringify(data, null, 2);
        infopokeapi.classList.add("info-visible");
        infopokeapi.classList.remove("error-message")

        front.src = data.sprites.front_default;
        back.src = data.sprites.back_default;

        front.style.display = "block";
        back.style.display = "block";

    } catch (error) {
        infopokeapi.textContent = error.message;
        infopokeapi.classList.add("error-message");
    }
});

//botão que pesquisa toda pokeapi utilizando limit e offset
botao_all_pokeapi.addEventListener("click", async () => {
    try {
        const limit = document.getElementById("limit");
        const offset = document.getElementById("offset");

        if (Number(limit.value) <= 0 || Number(offset.value) < 0) {
            throw new Error("Limite ou offset inválidos");
        }

        const response = await fetch(
            `https://projeto-final-back-end-ebac.onrender.com/pokeapi/all?limit=${limit.value}&offset=${offset.value}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Erro na API");
        }

        infopokeapi.textContent = JSON.stringify(data, null, 2);
        infopokeapi.classList.add("info-visible");
        infopokeapi.classList.remove("error-message")
        front.style.display = "none";
        back.style.display = "none";

    } catch (error) {
        infopokeapi.textContent = error.message;
        infopokeapi.classList.add("error-message")
    }
});

//formulario de criação de pokemon
form.addEventListener("submit", async (event) => {
    event.preventDefault();
    try{
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

        if(!response.ok){
            throw new Error(data.detail)
        }

        resposta_api.textContent = data.message;
        resposta_api.classList.remove("error-message")
        
    } catch(error) {
        resposta_api.textContent = error.message;
        resposta_api.classList.add("error-message")
    }
});


//formulario de atualização de pokemons
form_att.addEventListener("submit", async (event) => {
    event.preventDefault();

    try {
        const old_name = document
            .getElementById("nome-pokemon-att")
            .value
            .trim();

        if (!old_name) {
            throw new Error("Digite o nome do Pokémon que deseja atualizar");
        }

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

        const response = await fetch(
            `https://projeto-final-back-end-ebac.onrender.com/atualizar-pokemon/${old_name}`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(pokemon)
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Erro ao atualizar Pokémon");
        }

        resposta_api.textContent = data.message;
        resposta_api.className = "success-message";

    } catch (error) {
        resposta_api.textContent = error.message;
        resposta_api.className = "error-message";
    }
});

//botão para deletar um pokemon
botao_deletar.addEventListener("click", async (event) => {
    event.preventDefault();

    try {
        const name = document.getElementById("nome-pokemon-delete")
        const response = await fetch(`https://projeto-final-back-end-ebac.onrender.com/deletar-pokemon/${name.value}`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }
        });

        const data = await response.json();

    if (!response.ok) {
            throw new Error(data.detail || "Erro ao deletar Pokémon");
        }

        resposta_api.textContent = data.message;
        resposta_api.style.color = "green";

    } catch (error) {
        resposta_api.textContent = error.message;
        resposta_api.style.color = "red";
    }
});

//botão para ver pokemons criados pelo usuario
botao_ver_pokemons_criados_pelo_usuario.addEventListener("click", async () => {
    try {
        const response = await fetch(
            "https://projeto-final-back-end-ebac.onrender.com/pokemons"
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Erro ao buscar pokémons");
        }

        info_pokemons.textContent = JSON.stringify(data, null, 2);
        info_pokemons.classList.add("info-visible");

    } catch (error) {
        info_pokemons.textContent = error.message;
        info_pokemons.classList.add("error-message");
    }
}); 

// botão para ver pokémons criados através do nome
botao_ver_pokemons_por_nome.addEventListener("click", async () => {
    try {
        const name = document.getElementById("name-get");

        console.log(name.value)

        if(!name.value){
            throw new Error("Digite o nome do pokemon que deseja ver")
        }

        const response = await fetch(
            `https://projeto-final-back-end-ebac.onrender.com/pokemon/${name.value}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Erro ao buscar Pokémon");
        }

        info_pokemons.innerHTML = `
            <h2>${data.name}</h2>
            <p><strong>Altura:</strong> ${data.height}</p>
            <p><strong>Peso:</strong> ${data.weight}</p>
            <p><strong>Level:</strong> ${data.level}</p>
            <p><strong>Tipos:</strong> ${data.types.join(", ")}</p>
        `;

        info_pokemons.classList.add("info-visible");
        info_pokemons.classList.remove("error-message");

    } catch (error) {
        info_pokemons.textContent = error.message;
        info_pokemons.classList.add("error-message");
    }
});