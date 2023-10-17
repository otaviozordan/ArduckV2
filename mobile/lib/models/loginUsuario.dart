// To parse this JSON data, do
//
//     final usuarios = usuariosFromJson(jsonString);

import 'dart:convert';

UsuariosLogin usuariosLoginFromJson(String str) =>
    UsuariosLogin.fromJson(json.decode(str));

String usuariosLoginToJson(UsuariosLogin data) => json.encode(data.toJson());

class UsuariosLogin {
  String email;
  String password;
  String? cookie;

  UsuariosLogin({required this.email, required this.password, this.cookie});

  factory UsuariosLogin.fromJson(Map<String, dynamic> json) {
    return UsuariosLogin(
      email: json["email"],
      password: json["password"],
      cookie: json["cookie"] ?? "", // Se for nulo, atribui uma string vazia
    );
  }

  Map<String, dynamic> toJson() => {
        "email": email,
        "password": password,
        "cookie": cookie,
      };
}
