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

    fetch(`https://projeto-final-back-end-ebac.onrender.com/pokeapi/${id}`)  //atualmente busco no local, mas preciso mudar pra buscar no render
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
    fetch(`https://projeto-final-back-end-ebac.onrender.com/pokeapi/all`)
        .then(response => response.json())
        .then(data => { 
            infopokeapi.textContent = JSON.stringify(data, null, 2);
            infopokeapi.classList.add("info-visible");
            front.style.display = "none";
            back.style.display = "none";

        });
});