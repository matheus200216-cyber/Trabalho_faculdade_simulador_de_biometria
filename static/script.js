async function cadastrarFuncionario(){

    const nome =
        document.getElementById("nome").value;

    const digital =
        document.getElementById("digital").value;

    const resposta = await fetch("/cadastrar", {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body: JSON.stringify({
            nome: nome,
            digital: digital
        })
    });

    const dados = await resposta.json();

    mostrarResultado(
        dados.mensagem,
        dados.status
    );

    carregarRegistros();
}



async function baterPonto(){

    const digital =
        document.getElementById("digital").value;

    const resposta = await fetch("/bater_ponto", {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body: JSON.stringify({
            digital: digital
        })
    });

    const dados = await resposta.json();

    mostrarResultado(
        dados.mensagem,
        dados.status
    );

    carregarRegistros();
}



function mostrarResultado(mensagem, status){

    const resultado =
        document.getElementById("resultado");

    resultado.innerHTML = mensagem;

    if(status == "sucesso"){

        resultado.style.color = "#22c55e";

    }else{

        resultado.style.color = "red";
    }
}



async function carregarRegistros(){

    const resposta =
        await fetch("/listar_registros");

    const registros =
        await resposta.json();

    const lista =
        document.getElementById(
            "lista-registros"
        );

    lista.innerHTML = "";

    registros.reverse().forEach(registro => {

        lista.innerHTML += `

            <div class="registro">

                <strong>${registro.nome}</strong>
                <br>

                Digital: ${registro.digital}
                <br>

                ${registro.horario}

            </div>

        `;
    });
}



carregarRegistros();