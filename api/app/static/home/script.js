$('.menu a[data-menu]').on('click', function () {
  var menu = $(this).data('menu');
  $('.menu a.active').removeClass('active');
  $(this).addClass('active');
  $('.active[data-page]').removeClass('active');
  $('[data-page="' + menu + '"]').addClass('active');
});

$('body').on('click', '[data-dialog]', function () {
  var action = $(this).data('dialog');
  switch (action) {
    case 'logout':
      $('.dialog').toggleClass('active');
      break;
  }
});

$('body').on('click', '[data-dialog-action]', function () {
  var action = $(this).data('dialog-action');
  switch (action) {
    case 'cancel':
      $(this).closest('.dialog.active').toggleClass('active');
      break;
  }
});

function addUserToTable(data) {
  var table = $('.users-table');
  var ele = '<div class="users-item"><div class="table-item">' + data['nome'] + '</div><div class="table-item">' + data['email'] + '</div><div class="table-item">' + data['privilegio'] + '</div><div class="table-item">' + data['turma'] + '<div class="user-edit-controls"><a href="#" class="table-edit-button">Edit</a></div></div></div>';
  table.append(ele);

  // Selecione o botão "Editar" dentro da linha recém-adicionada
  var editButton = table.find('.table-edit-button:last');

  // Adicione um evento de clique ao botão "Editar"
  editButton.on('click', function () {
    // Quando o botão "Editar" é clicado, obtenha o email do usuário da linha
    var email = data['email'];

    // Atualize o conteúdo do elemento "username" com o email do usuário
    $('#username').text(email);
  });
}

function atualizaContador(nun) {
  var usernameElement = document.getElementById("contador-usuarios");
  usernameElement.innerHTML = nun;
}

var tempData = {};

function carregarUsuariosParaTemp() {
  fetch('/buscarusuarios_turma_usuario')
    .then(response => {
      if (!response.ok) {
        throw new Error('Erro na requisição');
      }
      return response.json();
    })
    .then(data => {
      // Verifica se a resposta contém o array "usuarios"
      if (data.usuarios && Array.isArray(data.usuarios)) {
        // Atribui os dados de usuário à variável tempData
        tempData = data.usuarios;
        nunUsers = Object.keys(tempData).length;
        atualizaContador(nunUsers);
        // Adiciona usuários à tabela, se necessário
        $.each(tempData, function (i, item) {
          addUserToTable(tempData[i]);
        });
      } else {
        console.error('Os dados da resposta estão faltando o array "usuarios".');
      }
    })
    .catch(error => {
      // Lida com erros
      console.error(error);
    });
}

function definirNome(nome) {
  var usernameElement = document.getElementById("nome-logado");
  usernameElement.innerHTML = nome;
}

function definirPrivilegio(privilegio) {
  var usernameElement = document.getElementById("privilegio-logado");
  usernameElement.innerHTML = privilegio;
}

function definirTurma(turma) {
  var usernameElement = document.getElementById("turma-logado");
  usernameElement.innerHTML = turma;
}

function whoami() {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", '/whoami', true); // Send data to the same URL
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 401 || xhr.status === 200) {
        // Handle successful response
      } else {
        // Handle error response
        alert("Error submitting form data");
      }
    }
  };
  xhr.send();
  xhr.onload = function () {
    var jsonResult = JSON.parse(xhr.response);
    nome = jsonResult.usuario.nome
    definirNome(nome);
    turma = jsonResult.usuario.turma
    definirTurma(turma);
    privilegio = jsonResult.usuario.privilegio
    definirPrivilegio(privilegio);
  };
};

// Chama a função para carregar usuários quando a página é carregada
window.onload = function () {
  carregarUsuariosParaTemp();
  whoami();
};

$('body').on('click', '.users-item:not(.header)', function () {
  console.log('click')
  $(this).toggleClass('active')
});

$('body').on('click', '.users-item a.table-edit-button', function () {
  $(this).closest('.grid').toggleClass('edit-users');
  $(this).closest('.users-item').toggleClass('active');
  e.preventDefault();
});

$('body').on('click', '.user-edit .header .close', function () {
  $(this).closest('.grid').toggleClass('edit-users');
  $(this).closest('.users-item').toggleClass('active');
  e.preventDefault();
});

function logout() {
  fetch('/logout')
    .then(response => {
      if (!response.ok) {
        throw new Error('Erro na requisição');
      }
      return response.json();
    })
    .then(data => {
      // Manipule os dados da resposta aqui
      console.log(data);
      location.reload(true); // Recarrega a página após o logout
    })
    .catch(error => {
      // Lida com erros
      console.error(error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  // Referências aos elementos HTML
  const deleteUserBtn = document.getElementById("deleteUserBtn");
  const checkProgressBtn = document.getElementById("checkProgressBtn");


  // Função para excluir o usuário
  function deleteUser() {
    const confirmDelete = confirm("Tem certeza de que deseja excluir este usuário?");
    if (confirmDelete) {
      var usernameElement = document.getElementById("username");
      email = usernameElement.textContent
      var formData = {
        email: email,
      };

      var xhr = new XMLHttpRequest();
      xhr.open("POST", '/deletar_usuario', true); // Send data to the same URL
      xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
      xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 401 || xhr.status === 200) {
            // Handle successful response
          } else {
            // Handle error response
            alert("Error submitting form data");
          }
        }
      };
      xhr.send(JSON.stringify(formData));
      xhr.onload = function () {
        var jsonResult = JSON.parse(xhr.response);
        if (jsonResult.delet) {
          alert("Deletado com sucesso")
          location.reload();
        }
        else {
          alert("Não excluido: " + jsonResult.mensagem)
        }
      };
    }
  }

 // Função para verificar o progresso do usuário
function checkProgress() {
  // Defina a variável 'email' aqui ou de onde quer que ela venha
  var usernameElement = document.getElementById("username");
  email = usernameElement.textContent

  function enviar_relatorio(formData) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/gerar_relatorio', true); // Envia dados para a mesma URL
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 401 || xhr.status === 200) {
          // Lida com a resposta de sucesso
        } else {
          // Lida com a resposta de erro
          alert("Erro ao gerar relatório");
        }
      }
    };
    xhr.send(JSON.stringify(formData));
    xhr.onload = function () {
      var jsonResult = JSON.parse(xhr.response);
      if (jsonResult.gen) {
        window.open(jsonResult.path, "_blank");
      }
      else {
        alert("Não enviado, erro: " + jsonResult.mensagem)
      }
    };
  }
 
  // Caixa de diálogo personalizada com botões personalizados
  Swal.fire({
    title: "Deseja enviar em um email?",
    icon: "question",
    backgrund:"black",
    showCancelButton: true,
    confirmButtonText: "Enviar por email",
    cancelButtonText: "Não enviar",
    customClass: {
      confirmButton: 'custom-confirm-button',
      cancelButton: 'custom-cancel-button'
    }
  }).then((result) => {
    if (result.value) {
      // Caixa de diálogo personalizada para escolher o destino do email
      Swal.fire({
        title: "Deseja receber no seu email? Se não, informar outro",
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Receber no meu email",
        cancelButtonText: "Informar outro email",
        customClass: {
          confirmButton: 'custom-confirm-button',
          cancelButton: 'custom-cancel-button'
        },

      }).then((result) => {
        if (result.value) {
          Swal.fire("Relatório enviado ao seu email pessoal.");
          var formData = { send: true, email_aluno: email };
          enviar_relatorio(formData);
        } else {
          // Caixa de diálogo personalizada para informar outro email
          Swal.fire({
            title: "Digite o endereço de email para o qual deseja enviar o email:",
            input: "text",
            confirmButtonText: "Enviar",
            showCancelButton: true,
            cancelButtonText: "Cancelar",
            customClass: {
              confirmButton: 'custom-confirm-button',
              cancelButton: 'custom-cancel-button'
            },
            inputValidator: (value) => {
              if (!value) {
                return "Você deve inserir um endereço de email válido.";
              }
            },
          }).then((result) => {
            if (result.value) {
              Swal.fire(`Relatório enviado para ${result.value}.`);
              var formData = { 'send': true, 'email_professor': result.value, 'email_aluno': email };
              enviar_relatorio(formData);
            } else {
              Swal.fire("Email não enviado.");
              var formData = { 'send': false, 'email_aluno': email };
              enviar_relatorio(formData);
            }
          });
        }
      });
    } else {
      Swal.fire("Email não enviado.");
      var formData = { 'send': false, 'email_aluno': email };
      enviar_relatorio(formData);
    }
  });
}

  // Adiciona ouvintes de eventos aos botões
  deleteUserBtn.addEventListener("click", deleteUser);
  checkProgressBtn.addEventListener("click", checkProgress);
});

