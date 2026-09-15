import 'package:flutter_test/flutter_test.dart';
import 'package:koniks/main.dart';

void main() {
  testWidgets('App initializes correctly', (WidgetTester tester) async {
    await tester.pumpWidget(const LetGeneralEducationApp());
    expect(find.byType(LetGeneralEducationApp), findsOneWidget);
  });
}
