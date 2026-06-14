const botao1 = document.getElementById("btn1");
const botao2 = document.getElementById("btn2");
const titulo = document.getElementById("titulo");
const id_pokeapi = document.getElementById("id_poke")


botao2.addEventListener("click", () => {
    const id = Number(id_pokeapi.value);

    if(id <= 0){
        return;
        }

    fetch(`http://0.0.0.0:8000/pokeapi/${id}`)  
        .then(response => response.json())
        .then(data => {
            titulo.textContent = JSON.stringify(data, null, 2);
            document.getElementById("front_img_pokemon").src = data.sprites.front_default;
            document.getElementById("back_img_pokemon").src = data.sprites.back_default;

        });
});

botao1.addEventListener("click", () => {
    fetch(`http://0.0.0.0:8000/pokeapi/all`)
        .then(response => response.json())
        .then(data => {
            titulo.textContent = JSON.stringify(data, null, 2);
            document.getElementById("front_img_pokemon").src = null;
            document.getElementById("back_img_pokemon").src = null;
        });
});