import 'package:flutter/material.dart';
import 'theme/app_theme.dart';
import 'screens/home_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const LetGeneralEducationApp());
}

class LetGeneralEducationApp extends StatelessWidget {
  const LetGeneralEducationApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LET General Education Practice Drills',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.navyTheme,
      home: const HomeScreen(),
    );
  }
}
