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

function updateGraph(data) {
  $('.graph .bar[data-day]').each(function () {
    var day = $(this).data('day');
    var barH = $(this).height();
    switch (day) {
      case 'sunday':
        $(this).find('.bar-content').css('height', (barH / 100) * data[day] + 'px');
        break;
      case 'monday':
        $(this).find('.bar-content').css('height', (barH / 100) * data[day] + 'px');
        break;
      case 'tuesday':
        $(this).find('.bar-content').css('height', (barH / 100) * data[day] + 'px');
        break;
      case 'wednesday':
        $(this).find('.bar-content').css('height', (barH / 100) * data[day] + 'px');
        break;
      case 'thursday':
        $(this).find('.bar-content').css('height', (barH / 100) * data[day] + 'px');
        break;
      case 'friday':
        $(this).find('.bar-content').css('height', (barH / 100) * data[day] + 'px');
        break;
      case 'saturday':
        $(this).find('.bar-content').css('height', (barH / 100) * data[day] + 'px');
        break;
    }
  });
}

function addUserToTable(data) {
  var table = $('.users-table');
  var ele = '<div class="users-item"><div class="table-item noflex">' + data['nome'] + '</div><div class="table-item">' + data['email'] + '</div><div class="table-item">' + data['privilegio'] + '</div><div class="table-item">' + data['turma'] + '<div class="user-edit-controls"><a href="#" class="table-edit-button">Edit</a></div></div></div>';
  table.append(ele);
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
        // Atualiza o gráfico ou realiza outras operações com os dados, se necessário
        updateGraph(tempData);
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

// Chama a função para carregar usuários quando a página é carregada
window.onload = function () {
  carregarUsuariosParaTemp();
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
