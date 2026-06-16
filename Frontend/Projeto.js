const botao_all_pokeapi = document.getElementById("btn1");
const botao_pokeapi_id = document.getElementById("btn2");
const infopokeapi = document.getElementById("infopokeapi");
const id_pokeapi = document.getElementById("id_poke");
const front = document.getElementById("front_img_pokemon");
const back = document.getElementById("back_img_pokemon");
const botao_tema = document.getElementById("botao-tema");
const body = document.body;


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

    const response = await fetch("http://127.0.0.1:8000/criar-pokemon", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(pokemon)
    });

    const data = await response.json();

    console.log(data);
});