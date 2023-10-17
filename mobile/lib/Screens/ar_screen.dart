import 'package:flutter/material.dart';

class ARWidget extends StatefulWidget {
  const ARWidget({super.key});

  @override
  State<ARWidget> createState() => _ARWidgetState();
}

class _ARWidgetState extends State<ARWidget> {
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: Text(
          "AR Screen",
          style: TextStyle(fontSize: 50),
        ),
      ),
    );
  }
}
