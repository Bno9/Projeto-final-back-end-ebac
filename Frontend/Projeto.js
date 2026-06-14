const botao_all_pokeapi = document.getElementById("btn1");
const botao_pokeapi_id = document.getElementById("btn2");
const infopokeapi = document.getElementById("infopokeapi");
const id_pokeapi = document.getElementById("id_poke");
const front = document.getElementById("front_img_pokemon");
const back = document.getElementById("back_img_pokemon");

botao_pokeapi_id.addEventListener("click", () => {
    const id = Number(id_pokeapi.value);

    if(id <= 0){
        return;
        }

    fetch(`http://0.0.0.0:8000/pokeapi/${id}`)  //atualmente busco no local, mas preciso mudar pra buscar no render
        .then(response => response.json())
        .then(data => {
            infopokeapi.textContent = JSON.stringify(data, null, 2);
            infopokeapi.style.border = "1px solid black";
            front.src = data.sprites.front_default;
            back.src = data.sprites.back_default;
            front.style.display = "block";
            back.style.display = "block";
        });
});

botao_all_pokeapi.addEventListener("click", () => {
    fetch(`http://0.0.0.0:8000/pokeapi/all`)
        .then(response => response.json())
        .then(data => {
            infopokeapi.textContent = JSON.stringify(data, null, 2);
            infopokeapi.style.border = "1px solid black";
            front.style.display = "none";
            back.style.display = "none";

        });
});