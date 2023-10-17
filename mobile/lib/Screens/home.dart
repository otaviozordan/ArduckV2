import 'package:arduck/Screens/ar_screen.dart';
import 'package:arduck/Screens/chat.dart';
import 'package:arduck/Screens/dynamic/colecoes/Home_colecoes.dart';
import 'package:arduck/Screens/dynamic/colecoes/models/model_colecao.dart';
import 'package:arduck/Screens/perfil.dart';
import 'package:flutter/material.dart';
import 'package:google_nav_bar/google_nav_bar.dart';
import 'package:line_icons/line_icons.dart';

class MyWidget extends StatefulWidget {
  const MyWidget({super.key, required this.cookie, required this.request});
  final RequestModel request;

  final String cookie;
  @override
  State<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  int _selectedIndex = 0;
  int badge = 0;

  void _navigateBottomBar(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  List<Color> colors = [
    Colors.purple,
    Colors.pink,
    Colors.amber[600]!,
    Colors.teal,
    Colors.lightBlue
  ];

  late List<Widget> _pages;

  @override
  void initState() {
    super.initState();

    _pages = [
      ColecoesScreen(
        cookie: widget.cookie,
        request: widget.request,
      ),
      const ARWidget(),
      const ChatWidget(),
      const PerfilWidget(),
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      bottomNavigationBar: AnimatedContainer(
        duration: const Duration(milliseconds: 800),
        color: colors[_selectedIndex],
        child: Container(
          decoration: const BoxDecoration(color: Colors.white),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 22.0, vertical: 14),
            child: GNav(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
              duration: const Duration(milliseconds: 800),
              gap: 8.5,
              tabs: [
                GButton(
                  iconActiveColor: Colors.purple,
                  iconColor: Colors.black,
                  textColor: Colors.purple,
                  backgroundColor: Colors.purple.withOpacity(.2),
                  iconSize: 24,
                  icon: LineIcons.home,
                  text: 'Home',
                ),
                GButton(
                  iconActiveColor: Colors.pink,
                  iconColor: Colors.black,
                  textColor: Colors.pink,
                  backgroundColor: Colors.pink.withOpacity(.2),
                  iconSize: 24,
                  icon: LineIcons.heart,
                  text: 'Likes',
                ),
                GButton(
                  iconActiveColor: Colors.amber[600],
                  iconColor: Colors.black,
                  textColor: Colors.amber[600],
                  backgroundColor: Colors.amber[600]!.withOpacity(.2),
                  iconSize: 24,
                  icon: LineIcons.search,
                  text: 'Search',
                ),
                GButton(
                  iconActiveColor: Colors.teal,
                  iconColor: Colors.black,
                  textColor: Colors.teal,
                  backgroundColor: Colors.teal.withOpacity(.2),
                  iconSize: 24,
                  icon: LineIcons.user,
                  text: 'Profile',
                )
              ],
              selectedIndex: _selectedIndex,
              onTabChange: (indexes) {
                _navigateBottomBar(indexes);
                print(widget.cookie);
              },
            ),
          ),
        ),
      ),
      body: _pages[_selectedIndex],
    );
  }
}
