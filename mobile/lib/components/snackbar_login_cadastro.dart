import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';

class FlashMessageDeuScreen extends StatefulWidget {
  const FlashMessageDeuScreen({super.key});

  @override
  State<FlashMessageDeuScreen> createState() => _FlashMessageScreenDeuState();
}

class _FlashMessageScreenDeuState extends State<FlashMessageDeuScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
          child: ElevatedButton(
        onPressed: () {
          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
            content: CustomSnackBarDeu(
              errorText: "E-mail já está em uso, informe outro!",
            ),
            behavior: SnackBarBehavior.floating,
            backgroundColor: Colors.transparent,
            elevation: 0,
          ));
        },
        child: const Text("Show Message"),
      )),
    );
  }
}

class CustomSnackBarDeu extends StatefulWidget {
  const CustomSnackBarDeu({
    super.key,
    required this.errorText,
  });

  final String errorText;

  @override
  State<CustomSnackBarDeu> createState() => _CustomSnackBarDeuState();
}

class _CustomSnackBarDeuState extends State<CustomSnackBarDeu> {
  @override
  Widget build(BuildContext context) {
    return Stack(
      clipBehavior: Clip.none,
      children: [
        Container(
          padding: const EdgeInsets.all(16),
          height: 90,
          decoration: const BoxDecoration(
            color: Color(0xFF38b000),
            borderRadius: BorderRadius.all(Radius.circular(20)),
          ),
          child: Row(
            children: [
              const SizedBox(width: 48),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      "Perfeito!",
                      style: TextStyle(fontSize: 16, color: Colors.white),
                    ),
                    const Spacer(),
                    Text(
                      widget.errorText,
                      style: const TextStyle(color: Colors.white, fontSize: 14),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        Positioned(
          bottom: 0,
          child: ClipRRect(
            borderRadius:
                const BorderRadius.only(bottomLeft: Radius.circular(20)),
            child: SvgPicture.asset(
              "lib/assets/images/snackbar/bubbles.svg",
              height: 48,
              width: 40,
              color: const Color(0xFF008000),
            ),
          ),
        ),
        Positioned(
          top: -20,
          left: 0,
          child: Padding(
            padding: const EdgeInsets.all(8.0),
            child: Stack(alignment: Alignment.center, children: [
              SvgPicture.asset(
                "lib/assets/images/snackbar/fail.svg",
                color: Color(0xFF008000),
                height: 40,
              ),
              Positioned(
                top: 10,
                child: SvgPicture.asset(
                  "lib/assets/images/snackbar/close.svg",
                  color: Color(0xFF008000),
                  height: 16,
                ),
              ),
            ]),
          ),
        )
      ],
    );
  }
}
