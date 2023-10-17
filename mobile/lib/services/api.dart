import 'dart:convert';

import 'package:arduck/models/colecoes/trilha/cadastrar_progresso.dart';
import 'package:arduck/models/usuarios.dart';
import 'package:http/http.dart' as http;

Future<Usuarios?> criarUsuario(
    String nome, String email, String password) async {
  final response = await http.post(
      Uri.parse('http://172.174.254.221/signup'), //http://10.0.2.2:80/signup
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: usuariosToJson(
          Usuarios(nome: nome, email: email, password: password)));

  if (response.statusCode == 200) {
    print('Resposta: ${response.body}');
    return Usuarios.fromJson(jsonDecode(response.body));
  } else {
    // Caso contrário, imprima o código de status e a razão do erro.
    print('Erro de requisição - Código: ${response.statusCode}');
    print('Erro de requisição - Razão: ${response.reasonPhrase}');
    print("PRINTANDO O ERRO: $response");
    throw response.body;
  }
}

Future<String> carregarColecoes(String cookies) async {
  try {
    final response = await http.get(
      Uri.parse('http://172.174.254.221/listar_colecoes'),
      headers: {
        'Cookie': cookies, // Adiciona o cookie nos headers
      },
    );

    if (response.statusCode == 200) {
      print(response.body);
      return response.body; // Retorna a resposta do servidor
    } else {
      throw 'Erro na requisição - Código: ${response.statusCode}';
    }
  } catch (error) {
    throw 'Erro na requisição: $error';
  }
}

Future<CadastrarProgresso?> cadastrarProgresso(
    String cookie, String colecao, String trilha, String elemento) async {
  final response = await http.post(
      Uri.parse(
          'http://172.174.254.221/cadastrarprogresso'), //http://10.0.2.2:80/cadastrarprogresso
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Cookie': '$cookie'
      },
      body: cadastrarProgressoToJson(CadastrarProgresso(
          colecao: colecao, trilha: trilha, elemento: elemento)));

  if (response.statusCode == 200) {
    print('Resposta: ${response.body}');
    return CadastrarProgresso.fromJson(jsonDecode(response.body));
  } else {
    print('Erro de requisição - Código: ${response.statusCode}');
    print('Erro de requisição - Razão: ${response.reasonPhrase}');
    print("PRINTANDO O ERRO: $response");
    throw response.body;
  }
}

Future<String> carregarTrilhas(String cookies, String colecao) async {
  try {
    final response = await http.get(
      Uri.parse('http://172.174.254.221/listartrilha_por_colecao/$colecao'),
      headers: {
        'Content-Type': 'application/json; charset=UTF-8',
        'Cookie': cookies, // Adiciona o cookie nos headers
      },
    );

    if (response.statusCode == 200) {
      print(response.body);
      return response.body; // Retorna a resposta do servidor
    } else {
      throw 'Erro na requisição - Código: ${response.statusCode}';
    }
  } catch (error) {
    throw 'Erro na requisição: $error';
  }
}

Future<void> enviarPostParaServidor() async {
  const String apiUrl = 'http://172.174.254.221/cadastrartrilha';
  final Map<String, dynamic> jsonData = {
    "colecao": "eletronica",
    "trilha": "led",
    "ordem": 1,
    "img_path": "a/",
    "descricao": "arduck",
    "teoria": "arduck",
    "ar": "sasa",
    "progressivo": false,
    "validacao_pratica": {},
    "quiz": {}
  };

  try {
    final response = await http.post(
      Uri.parse(apiUrl),
      headers: <String, String>{
        'Content-Type': 'application/json',
        'Cookie':
            'session=.eJwlzjEOwjAMAMC_ZEbIae3YZeInlWM7UEGFaOmAEH-nEvMt90ljW2K9ptNr2eKQxsnTKZHXzILQFAt0wVWk1RpOEgw9CUXRjB221oQ1KKwADTa4oTpwEaDcq2MIDcE7CFQSt8oVUI1IxYsLgOXMfetKFXZzAPJikTHtkW2N5b-56fu5xfky63Q_2mNO3x_mfzXF.ZQ8E_w.gAfNNzeKzA8QLkkm5QCy305I8F8; HttpOnly; Path=/',
      },
      body: jsonEncode(jsonData),
    );

    if (response.statusCode == 200) {
      print('POST request enviado com sucesso');
      print('Resposta do servidor: ${response.body}');
    } else {
      print('Falha ao enviar o POST request');
      print('Código de status: ${response.statusCode}');
      print('Mensagem de erro: ${response.reasonPhrase}');
    }
  } catch (e) {
    print('Erro durante o envio do POST request: $e');
  }
}

Future<List<Map<String, dynamic>>> carregarQuiz(
    String colecao, String trilha, String cookie) async {
  const String apiUrl =
      'http://172.174.254.221/carregarquiz'; // Replace with your actual URL
  final Map<String, dynamic> jsonData = {
    "colecao": colecao,
    "trilha": trilha,
  };

  try {
    final response = await http.post(
      Uri.parse(apiUrl),
      headers: <String, String>{
        'Content-Type': 'application/json',
        'Cookie': cookie,
      },
      body: jsonEncode(jsonData),
    );

    if (response.statusCode == 200) {
      print('POST request sent successfully');
      print('Server response: ${response.body}');

      final Map<String, dynamic> responseBody = jsonDecode(response.body);
      final List<Map<String, dynamic>> quizList =
          List<Map<String, dynamic>>.from(
        responseBody['quiz'] as List<dynamic>,
      );

      return quizList;
    } else {
      print('Failed to send the POST request');
      print('Status code: ${response.statusCode}');
      print('Error message: ${response.reasonPhrase}');
      throw 'Failed to load quiz';
    }
  } catch (e) {
    print('Error while sending the POST request: $e');
    throw 'Failed to load quiz';
  }
}

void main() {
  //loginUsuario("usuario@gmil.com", "usuario");
  //criarUsuario("kayque1", "kayque1@gmail.com", "kayque1");
  //carregarColecoes(
  //  'session=.eJwlzksKwjAQANC7ZC0yaTOZqStvUuYXLVgKrVmJd7fg-m3eJ81tj-OZbu-9xyXNi6dbQtdMXKBJqTAEKXNTDUcOghEZo0ouQ2mtMUlgWAWcbHIr4kCVAfMoXoJxCjqBQZHdlBSKGKKwV2cAy5nGNlRlcnMA9GqRSzoj_Yj9v-lHl33Z7o9VltfVtjV9fx5pNj0.ZQuP1w.zX5DILUpjJ0mKQmwpKYHfmWw4Bg; HttpOnly; Path=/');
  cadastrarProgresso(
      "session=.eJwlzksKwjAQANC7ZC0yaTOZqStvUuYXLVgKrVmJd7fg-m3eJ81tj-OZbu-9xyXNi6dbQtdMXKBJqTAEKXNTDUcOghEZo0ouQ2mtMUlgWAWcbHIr4kCVAfMoXoJxCjqBQZHdlBSKGKKwV2cAy5nGNlRlcnMA9GqRSzoj_Yj9v-lHl33Z7o9VltfVtjV9fx5pNj0.ZQuP1w.zX5DILUpjJ0mKQmwpKYHfmWw4Bg; HttpOnly; Path=/",
      "SD",
      "Eletronica",
      "teoria/true");
  //enviarPostParaServidor();
  //carregarTrilhas(
  //    'session=.eJwlzjEOwjAMAMC_ZEbIae3YZeInlWM7UEGFaOmAEH-nEvMt90ljW2K9ptNr2eKQxsnTKZHXzILQFAt0wVWk1RpOEgw9CUXRjB221oQ1KKwADTa4oTpwEaDcq2MIDcE7CFQSt8oVUI1IxYsLgOXMfetKFXZzAPJikTHtkW2N5b-56fu5xfky63Q_2mNO3x_mfzXF.ZQ8E_w.gAfNNzeKzA8QLkkm5QCy305I8F8; HttpOnly; Path=/',
  //    'eletronica');
  //carregarQuiz('eletronica', 'Resistores',
  //   'session=.eJwlzjEOwjAMAMC_ZEbIae3YZeInlWM7UEGFaOmAEH-nEvMt90ljW2K9ptNr2eKQxsnTKZHXzILQFAt0wVWk1RpOEgw9CUXRjB221oQ1KKwADTa4oTpwEaDcq2MIDcE7CFQSt8oVUI1IxYsLgOXMfetKFXZzAPJikTHtkW2N5b-56fu5xfky63Q_2mNO3x_mfzXF.ZQ8E_w.gAfNNzeKzA8QLkkm5QCy305I8F8; HttpOnly; Path=/');
}
