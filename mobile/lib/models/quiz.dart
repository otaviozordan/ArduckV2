class Question {
  final String text;
  final List<Option> options;
  bool isLocked;
  Option? selectedOption;

  Question({
    required this.text,
    required this.options,
    this.isLocked = false,
    this.selectedOption,
  });
}

class Option {
  final String text;
  final bool isCorrect;
  const Option({required this.isCorrect, required this.text});
}

final questions = [
  Question(
      text:
          "Em certo projeto envolvendo a conexão entre um dispositivo de transmissão, em cima de uma montanha, e uma central tv , próxima ao pé da montanha, existe a dúvida de usar um meio guiado ou não para levar os dados da central para transmissão no topo da montanha. Considerando que a central precisa manter os custos de operação mais baixo possível, para se manter dentro do orçamento, qual a melhor escolha a ser feita para o meio usado?",
      options: [
        const Option(
            isCorrect: false,
            text:
                "Cabos de cobre com alta atenuação para grandes distâncias, como acontece no projeto"),
        const Option(
            isCorrect: false,
            text: "Transmissor de alta potência e consequente alto consumo"),
        const Option(
            isCorrect: false,
            text:
                "Fibras ópticas de alta pureza e baixa atenuação, para longas e curtas distâncias "),
        const Option(
            isCorrect: true,
            text:
                "Transmissor com baixo consumo, mas frequentes perdas de dados")
      ])
];
