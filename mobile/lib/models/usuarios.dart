// To parse this JSON data, do
//
//     final usuarios = usuariosFromJson(jsonString);

import 'dart:convert';

Usuarios usuariosFromJson(String str) => Usuarios.fromJson(json.decode(str));

String usuariosToJson(Usuarios data) => json.encode(data.toJson());

class Usuarios {
  String? nome;
  String email;
  String password;

  Usuarios({
    required this.nome,
    required this.email,
    required this.password,
  });

  factory Usuarios.fromJson(Map<String, dynamic> json) => Usuarios(
        nome: json["nome"],
        email: json["email"],
        password: json["password"],
      );

  Map<String, dynamic> toJson() => {
        "nome": nome,
        "email": email,
        "password": password,
      };
}
