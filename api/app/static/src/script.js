
/* Fim data Criação e Edição Tópicos */
 /*Código do Athos*/
/* Inicio data Criação e Edição Trilhas */
var trilhas = [
    {
        id: 0,
        nome: 'Eletrônica'
    }
]

/*Mostra ou atualiza os Elementos da Barra*/
var indexValo=0;
var indiceGlobTri;
var opa = 0;
valoe = (id) => {
    regu = "/NumTrilha\(\d+)/g";
    while ((match = id.exec(id)) !== null) {
        opa = match[1]
        console.log(opa);
        /*opa = id.slice(10,11);*/
    }
    indiceGlobTri = opa;/*Opa pega os números a partir de do carac 10 até o 12 de 'NumTrilha'+k, com k podendo ter dois caracteres */
}


responseJson=[]
function buscar_colecoes() {
    console.log("Regu",opa);
    fetch('/listar_colecoes')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na requisição');
            }
            return response.json();
        })
        .then(data => {
            // Manipule os dados da resposta aqui
            responseJson = [];
            for (const chave in data.colecoes) {
                if (data.colecoes.hasOwnProperty(chave)) {
                    responseJson.push(chave);
                }
            }
            console.log('As coleções são:');
            iniLeftBar();
        })
        .catch(error => {
            // Lida com erros
            console.error(error);
        });
}

function iniLeftBar() {
    console.log(responseJson)
    var containerPo = document.getElementById("trilha_bar");
    console.log(containerPo)
        if(containerPo === `<div id="trilha_bar"></div>`){
            indexValo +=1;
            var k=0;
            for(p=0;p<responseJson.length;p++){
                containerPo.innerHTML += `
                <button id="NumTrilha`+k+`" class="leftButton" onclick="valoe(id)">  
                <a class="elements_bottom_left_bar">`+responseJson[k]+`</a>
                </button>
                `;
                k++;
            }
        }
        if(containerPo != `<div id="trilha_bar"></div>`){
            containerPo.innerHTML = ``;
            var k=0;
            for(p=0;p<responseJson.length;p++){
                containerPo.innerHTML += `
                <button id="NumTrilha`+k+`" class="leftButton" onclick="valoe(id)>  
                <a class="elements_bottom_left_bar">`+responseJson[k]+`</a>
                </button>
                `;
                k++;
            }
        }
}
/*Fim Barra Esquerda*/

console.log("wdiwqnd",responseJson);





/*Inicio Edição Tópicos*/
    /*Mostra Tópicos já adicionados e agora atualiza os tópicos editados*/
    var whichJson;
addTopicos = () => {
    whichJson = responseJson[opa];/*O nome da coleção que vc entrou, muda o nome de acordod com a coleção clicada atraves de um índice*/
    console.log("whi",whichJson);
    var trailsJson=[];
    var passa = '/listartrilha_por_colecao/'+whichJson;
        fetch(passa)
          .then(function (response) {
            console.log(response);
            var lido = response.json();
          })
          .then(function(data) {
            trailsJson = data.trilhas;
            console.log("Trains",trailsJson)
          })
          .catch(function (error) {
            console.error('Erro Request:', error);
          });    
          var qui,arom,pra;
    if (trailsJson.ar!=null){
        arom = 'sim';
    }
    if (trailsJson.pratica!=null){
        pra = 'sim';
    }
    qui = trailsJson.quiz.length;
    var indTri =1;
    var containerProdutors = document.getElementById("itens_area_maior_index");
    if(containerProdutors === `<div id="itens_area_maior_index" class="box_config4">           
    <div>
    <a >#</a>
    <a class="str_list_topics_first01">Nome</a>
    <a class="str_list_topics_first01">Quiz</a>
    <a class="str_list_topics_first01">Prática</a>
    <a class="str_list_topics_first01">AR</a>
    </div></div>`){
        console.log(5);
        trailsJson.map((val)=>{
            qui = val.quiz.length;
            if (val.ar!=null){
                arom = 'sim';
            }
            if (val.pratica!=null){
                pra = 'sim';
            }
            containerProdutors.innerHTML += `
            <div id="Topic`+indTri+`" class="GB">
            <div class="cot">
                    <a  class="relative_positionI">`+indTri+`</a>
                    <a key="`+indTri+`" class="relative_position1">`+val+`</a>
                    <a class="relative_position">`+val.qui+`</a>
                    <a class="relative_position">`+val.pra+`</a>
                    <a class="relative_position">`+val.arom+`</a>
                    </div>
            </div>
            `;
            indTri++;
        })
    }
    if(containerProdutors != `<div id="itens_area_maior_index" class="box_config4">           
    </div>`){
        trailsJson.map((val)=>{
            containerProdutors.innerHTML += `
            <div id="Topic`+indTri+`" class="GB">
                <div class="cot">
                    <a class="relative_positionI">`+indTri+`</a>
                    <a key="`+indTri+`" class="relative_position1">`+val+`</a>
                    <a class="relative_position">`+val.qui+`</a>
                    <a class="relative_position">`+val.pra+`</a>
                    <a class="relative_position">`+val.arom+`</a>
                </div>
            </div>
            `;
            indTri++;
        })
    }
}
    /*Adicionar Quizes*/
var buffer = 0;
var buffos = 0;
var buffo = [];
var beffe = [];

AddParts = (n) => {
    buffer++;
    if(n==1){}
    nombre = "comple"+n;
    var containerProdutors = document.getElementById(nombre);
    console.log("perg"+n+buffer);
    containerProdutors.innerHTML += `
    <div id="comple`+n+buffer+`" class="gerals3">
        <div>
        <p>Pergunta</p>
        <input class="inputsTri" type="text" id="perg`+n+buffer+`">
        <p >Alternativa(A ou a,) correta</p>
        <input type="text" id="resp`+n+buffer+`">
        <p class="strCo">Imagem(URL) da questão</p>
        <input class="inputsTri" type="text" id="img_quiz`+n+buffer+`">
        </div>

        <div class="classG">
        <p >Alternativas</p>
        <div class="geralsin">
            <p class="ques">A</p>
            <input class="inputsTri" type="text" class="alte" id="alt1`+n+buffer+`">
        </div>
        <div class="geralsin">
                
            <p class="ques">B</p>
            <input class="inputsTri" type="text" class="alte" id="alt2`+n+buffer+`">
        </div>
        <div class="geralsin">
            <p class="ques">C</p>
            <input class="inputsTri" type="text" class="alte" id="alt3`+n+buffer+`">
        </div>        
        <div class="geralsin">
            <p class="ques">D</p>
            <input class="inputsTri" type="text" class="alte" id="alt4`+n+buffer+`">
        </div>
        </div>
    </div>
        `;
        console.log(buffer)
        ito = `item`+buffer;
        buffo.push(ito);
        console.log("an",buffo)

}
    /*Apagar Quizes adicionados*/
var boolPra = false;
RemoveParts = (n) => {
    if (buffer===0){
    }
    else{
        var namo = "comple"+n+buffer;    
        var containerProdutors = document.getElementById(namo);
        containerProdutors.remove();
        buffer= buffer-1;
        console.log(buffer)
    }
}
var buffos=0;
AddSub = (o) => {
    buffos++;
    if(buffos<5){
    nombre = "Su"+o;
    console.log(nombre);
    var containerProdutors = document.getElementById(nombre);
    containerProdutors.innerHTML += `
    <div class="gerals" id="Su`+o+buffos+`">
                    <div>
                    <p class="strCo">`+buffos+` Título</p>
                    <input id="Ti`+o+buffos+`" class="inputsTri" type="Legenda">
                    </div>
                    <div>
                        <p class="strCo">`+buffos+` Teoria</p>
                        <form>
                            <textarea class="inputsTriDe" wrap="hard" type="text" id="descTi`+o+buffos+`"></textarea>
                        </form>
                    </div>
                </div>
        `;
        console.log(buffos)
        ito = `item`+buffos;
        beffe.push(ito);
    }
    else{alert("São permitidos até 4 subtópicos por trilha")}
}
    /*Apagar Quizes adicionados*/
var boolPra = false;
RemoveSub = (o) => {
    if (buffos===0){
    }
    else{
        var namo = "Su"+o+buffos;    
        var containerProdutors = document.getElementById(namo);
        containerProdutors.remove();
        buffos= buffos-1;
        console.log(buffos)
    }
}

    /*Habilida e Desabilita Prá Criar ou Editar*/
desabilitaOpcaoPr = (n) => {
    var state = document.getElementById('StateQuiz'+n);
    var elementos = document.getElementById('com'+n);
    if (state.checked){ 
        elementos.innerHTML = `
        <div class="ladin">
        <div id="content">
            <h4>Questão</h4>
            <input class="inputsTri" type="text" class="alte" id="cont`+n+`">
        </div>
        <div id="com">
            <h4>Valor medido esperado</h4>
            <input class="inputsTri" type="text" class="alte" id="pra`+n+`">
        </div>
        </div>
    `;
    boolPra = true;
    } 
    else{
        if(elementos===null){        
            console.log("Passou")
            return
        }
        if(elementos != `<div id="com`+n+`"></div>`){
            elementos.innerHTML = ``
        }
    }   
}
    /*Habilida e Desabilita AR Criar ou Editar*/
desabilitaOpcaoAR = (n) => {
    console.log(n);
    var stateAR = document.getElementById('StateQuizAR'+n);
    nombre = 'comAR'+n;
    var elementosAR = document.getElementById(nombre);
    if (stateAR.checked){ 
        elementosAR.innerHTML = `
        <p>Entre com o modelo AR</p>
        <input type="file">`;
    } 
    else{
        if(elementosAR===null){        
            return
        }
        if(elementosAR != `<div id="comAR`+n+`"></div>`){
            elementosAR.innerHTML = ``
        }
    }   
}
/*Fim Edição Tópicos*/






/* Inicio Mostra Dados Tópico */
incializate_topicos = () => {
    var containerProdutors = document.getElementById("itens_area_maior_index");
    trailsJson.map((val)=>{
        qui = val.quiz.length;
        if (val.ar!=null){
            arom = 'sim';
        }
        if (val.pratica!=null){
            pra = 'sim';
        }
       containerProdutors.innerHTML += `
        <div id="`+indTri+`" class="left_Bar">
        <button class="str_list_topics_first">
                <a >`+indTri+`</a>
                <a key="`+indTri+`" href="model_data.html" class="relative_position">`+val+`</a>
                <a class="relative_position">`+qui+`</a>
                <a class="relative_position">`+pra+`</a>
                <a class="relative_position">`+arom+`</a>
            </button>
        </div>
        `;
        indTri++;
    })
}
/* Fim Criação Tópico */


/* Inicio Criação Trilha */
    /*Variaveis */
var nameTri;
var imgTri;
readVal = () => {/*Já Direciona os dados*/ 
    nameTri = document.getElementById("nameTri").value;
    trilhas.push(
        {
            id: 82,
            nome: nameTri,
            img: imgTri
        }
    );
    buscar_colecoes();
    console.log("Trilhas",trilhas)
}
/* Fim Criação Trilha */


/*Inicio Envio de dados para outro code*/
    /*Vars gerais antes n declaradas*/
 var trilha, ordem, descricao, tipos, valor_esperado, img_path, defaultpath, teo1, teo2;
 teoria = [];
 var ti0,des1;
 var biffi=[];
 var ext = [];
 ans=[];
 quiz = [];
 var quizin= {};
 Theory = {};
 TheSonOfJson = {};
 validacao_pratica = {};

gettingFunctions = (n) =>{
    if(document.getElementById('namecoc').value === null || document.getElementById('namecoc').value === undefined){
        colecao = whichJson;/*São as ultimas atualizações!*/
    }
    else{
        colecao = document.getElementById('namecoc').value;/*São as ultimas atualizações!*/
    }
    /*colecao =  "HEllo";*/
    trilha = document.getElementById('nameTo'+n).value;
    ordem = document.getElementById('NumCol'+n).value;
    img_path = document.getElementById('img_path'+n).value;
    descricao = document.getElementById('descTri'+n).value;
    /*Theorys*/
    /*Img and theory initial*/
    var teo1 = document.getElementById('teoria1'+n).value;
    var pah1 = document.getElementById('img_paths1'+n).value;
    /*Img and theory final*/
    var teo2 = document.getElementById('teoria2'+n).value;
    var pah2 = document.getElementById('img_paths2'+n).value;
    var lng = document.getElementById('Legendo'+n).value;
    var inde = 1;

/*Extensões*/
        console.log("RestanteS");
        if(pah1 === 0){
            pah1="$path";
        }
        else{
            /*filep1 = "$"+pah1.files[0].name;*/
        }
        if(pah2 === 0){
            pah2="$path";
        }
        else{
           /* filep2 = "$"+pah2.files[0].name;*/
        }

        console.log("beffe",beffe);
        /*Empacotando Theory em {}*/
        beffe.map((vol)=>{
            console.log("INde",inde)
            console.log("Ti",`Ti`+n+inde);
            Ti = document.getElementById(`Ti`+n+inde+``);
            descTi = document.getElementById(`descTi`+n+inde+``);
            if(Ti.value===null || Ti.value===undefined || Ti.value===""){
                Ti="";
            }
            else{
                Ti = inde+". "+Ti.value;
            }
            if(descTi.value===null || descTi.value===undefined || descTi.value===""){
                descTi="";
            }
            else{
                descTi = descTi.value;
            }
            teoria.push(Ti);
            teoria.push(descTi);
            inde++;
            console.log("teoria",teoria);
        })

        Theory[teo1]="";
        Theory[pah1]="";

        for (i = 0; (i<buffos*2); i++){

            var pathon = teoria[i];
            Theory[pathon] ="";
        }
        console.log("Theory",Theory);
        Theory[teo2]="";
        Theory[pah2]="";
        Theory[lng]="";
        for (io = 0; (io<buffer); io++){
            if(io/2%0){var pathoni = teoria[buffer];}
            else{var pathoni = buffer+". "+teoria[buffer];}
            Theory.pathoni ="";
        }

        Theory[teo2]="";
        Theory[pah2]="";
        console.log("Theory quiz",Theory);
        /*Fim theorys*/

        console.log("depois",buffo);
        /*Inicio Quiz*/
        var ui = 1;
        buffo.map((val)=>{/*Númeor de quizes*/
            console.log("Passou pelo quiz!");
            console.log("na time", "perg"+n+ui);
            perg = document.getElementById(`perg`+n+buffer+``).value;
            resp = document.getElementById(`resp`+n+buffer+``).value;
            img_quiz = document.getElementById(`img_quiz`+n+buffer+``).value;
            
            var lito=[];
            var conts=[];
            a = document.getElementById(`alt1`+n+buffer+``).value;
            lito.push("a");
            conts.push(a);
            b = document.getElementById(`alt2`+n+buffer+``).value;
            lito.push("b");
            conts.push(b);
            c = document.getElementById(`alt3`+n+buffer+``).value;
            lito.push("c");
            conts.push(c);
            d = document.getElementById(`alt4`+n+buffer+``).value;
            lito.push("d");
            conts.push(d);
            ui++;
            for(var io=0;io<4;io++){
            if(resp.toLowerCase()===lito[io]){
                ans.push({
                    "text":conts[io],
                    "isCorrect":true,
                    "url":"lib/assets/images/"+lito[io]+"quiz.png"
                    });

            }
            else{
                ans.push({
                    "text":conts[io],
                    "isCorrect":false,
                    "url":"lib/assets/images/"+lito[io]+"quiz.png"
                    });
            }
            }
            var item = {
                "questionText": perg,
                "isImagem":img_quiz,
                "answers":biffi
            }
            console.log("item",item);
            quiz.push(item);
            biffi.push(ans);
            ans = [];
            item = {};
            biffi = [];
        })
        buffo.map((val)=>{
        console.log("Buffos",buffo);
        });

        
        console.log("Quiz",quiz);
        /*Fim Quiz*/
        

        /*Inicio Validação prática*/
        if(document.getElementById("StateQuiz"+n).value===true){
            tipos = document.getElementById("cont"+n).value;
            valor_esperados = document.getElementById("pra"+n).value;
            validacao_pratica = {
                tipo: tips,
                valor_esperado: valor_esperados
            }
        }
        else{
            validacao_pratica = {};
            /*validacao_pratica = {
                tipo: "multimetro",
                valor_esperado: 0
            }*/
        }
        /*Fim Validação prática*/
        /*inicio AR*/
        ar = document.getElementById("StateQuiz"+n).value;
        img_col = document.getElementById("img_col").value;
        /*Fim AR*/



        /*Atribuições finais Json*/
        console.log("Trilha",trilha);

        
        TheSonOfJson = {
            "colecao": colecao,
            "img": img_col,
            "trilha": trilha,
            "ordem": ordem,
            "img_path": img_path,
            "descricao": descricao,
            "teoria": Theory,
            "ar": ar,
            "progressivo": true,
            "validacao_pratica": validacao_pratica,
            "quiz": quiz
            
        }
        
        console.log("TheSonOfJson",TheSonOfJson)
    
    /*Fim Envio de dados para outro code*/
    
    var email = "athomos@gmail.com.br";
    var pass = "12345";
    var nome = "TheBiggest";
    var pri = "administrador";
    var turma = "demo";

    jsontolog = {
        "email": "athomos18@gmail.br",
	    "password": "12345",
	    "nome": "TheBiggest",
	    "privilegio":"professor"
    }
    console.log(JSON.stringify(TheSonOfJson));
    var opcoes = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(TheSonOfJson)
    };

    /*data for login*/

/*
 var opcoes2 = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(jsontolog)
  };

    /*Login usuário*//*
    fetch('http://localhost/login', opcoes2)
    .then(function (response) {
      console.log("Logado!")
        o =true;
        return o;
    })
    .catch(function (error) {
      console.error("Ocorreu um erro na postagem dos dados: ",error)
    });
    */
    
    /*Cadastro da trilha*/

    fetch('/cadastrartrilha', opcoes)
      .then(function (response) {
        console.log("Funfou!")
    })
      .catch(function (error) {
        console.error("Ocorreu um erro na postagem dos dados",error)
    });
    conc = document.getElementById("con"+n);
    conc.innerHTML = `<p>Criação completa!</div>`;
    buffer=0;
    inde= 1;
    buffo = [];
    quiz = [];    
    Theory = {};
    buffos = 0;
    beffe= [];
    teoria = [];
}

 

    /*Ending Request to Server*/
/*Starting Request to Server*/
sending = () =>{
    fetch('/cadastrartrilha')
      .then(function (response) {
        console.log(response);
        return response.json();
      })
      .catch(function (error) {
        console.error('Erro Request:', error);
      });    }
    

/*Starting Post to Server*/
/*Aqui o login e o post para cadastrartrilha*/

/*Inicio Login*/
submitForm = () => {
    var email = document.getElementById("emailInput").value;
    var password = document.getElementById("passwordInput").value;
    var formData = {
        email: email,
        password: password
    };
    console.log(formData);
    var jsonFormData = JSON.stringify(formData);
    console.log(jsonFormData);

    // You can use this JSON string (jsonFormData) to send to a server or perform other actions
    //console.log(jsonFormData);

    var currentURL = "/login"; // Substitua pela URL apropriada
var requestOptions = {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(formData) // Substitua jsonFormData pelos seus dados
};

fetch(currentURL, requestOptions)
    .then(function(response) {
        if (response.status === 401 || response.status === 200) {
            // Handle successful response
            console.log("It's working");
        } else {
            // Handle error response
            alert("Error submitting form data");
        }
        return response.json(); // Retorna os dados JSON da resposta
    })
    .then(function(jsonResult) {
        if (jsonResult.login) {
            wm = "/home";
            console.log("logado");
        } else {
            alert("Não logado: " + jsonResult.mensagem);
        }
    })
    .catch(function(error) {
    });
} 




var indexColection;

/*Funções precisam rodar quando abre a página*/
document.addEventListener("DOMContentLoaded", function () {
    buscar_colecoes();
    /*addTopicos();*/
    var tx0 = document.getElementById("tx0");
    var tx1 = document.getElementById("tx1");
    var qu0 = document.getElementById("qu0");
    var qu1 = document.getElementById("qu1");

    var du = document.getElementById("duvida1");
    var dul = document.getElementById("duvida2");
    
    /*Página Inicial*/
    var IniTri = document.getElementById("InitialPageL");
    var Init = document.getElementById("FormToLogin");

    /*Botão Trilha*/
    var MakeTri = document.getElementById("MakeTriL");
    var Make = document.getElementById("formlario");

    /*Botão Tópicos*/
    var escrit = "NumTrilha"+indexValo;
    console.log(escrit);
    t=0;
    for(u=0;u<responseJson.length;u++){
    no = "NumTrilha"+t;
    var SeeTri = document.getElementById(no);
    var See = document.getElementById("forms01");
    t++;
    }
    /*Criar Tópicos*/
    var MakeTopic = document.getElementById("MakeTopic");
    var Topic = document.getElementById("forms02");


    tx0.addEventListener("click", function() {
        if (du.style.visibility === "hidden" || du.style.visibility === "") {
            du.style.visibility = "visible";
        }
        else{
            du.style.visibility = "hidden";
        }

    });
    tx1.addEventListener("click", function() {
        if (du.style.visibility === "hidden" || du.style.visibility === "") {
            du.style.visibility = "visible";
        }
        else{
            du.style.visibility = "hidden";
        }

    });
    qu1.addEventListener("click", function() {
        if (dul.style.visibility === "hidden" || dul.style.visibility === "") {
            dul.style.visibility = "visible";
        }
        else{
            dul.style.visibility = "hidden";
        }

    });
    qu0.addEventListener("click", function() {
        if (dul.style.visibility === "hidden" || dul.style.visibility === "") {
            dul.style.visibility = "visible";
        }
        else{
            dul.style.visibility = "hidden";
        }

    });

/*
    IniTri.addEventListener("click", function() {
        console.log("ini")
        if (Init.style.visibility === "hidden" || Init.style.visibility === ""){
            // Se estiver oculta, mostre-a
            See.style.visibility = "hidden";
            Make.style.visibility = "hidden";
            Topic.style.visibility = "hidden";
            Init.style.visibility = "visible";
          } 
    });*/
    
    MakeTri.addEventListener("click", function() {
        console.log("Fazer")
        if (Make.style.visibility === "hidden" || Make.style.visibility === "") {
            // Se estiver oculta, mostre-a
            /*See.style.visibility = "hidden";*/
            /*Init.style.visibility = "hidden";*/
            Topic.style.visibility = "hidden";
            Make.style.visibility = "visible";
          } 
    });

    SeeTri.addEventListener("click", function() {
        console.log("Ver")
        if (See.style.visibility === "hidden" || See.style.visibility === "") {
            // Se estiver oculta, mostre-a
            /*Init.style.visibility = "hidden";*/
            Make.style.visibility = "hidden";
            Topic.style.visibility = "hidden";
            See.style.visibility = "visible";
          } 
    });

    MakeTopic.addEventListener("click", function() {
        console.log("Tópico");
        if (Topic.style.visibility === "hidden" || Topic.style.visibility === ""){
            // Se estiver oculta, mostre-a
            See.style.visibility = "hidden";
            Make.style.visibility = "hidden";
            /*Init.style.visibility = "hidden";*/
            Topic.style.visibility = "visible";
          } 
    });
});
/*dddddddddddddd*/