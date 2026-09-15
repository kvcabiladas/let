class Question {
  final int id;
  final String questionText;
  final List<String> options;
  final int correctAnswerIndex; // 0 for A, 1 for B, 2 for C, 3 for D

  const Question({
    required this.id,
    required this.questionText,
    required this.options,
    required this.correctAnswerIndex,
  });

  String get correctAnswerLetter {
    switch (correctAnswerIndex) {
      case 0:
        return 'A';
      case 1:
        return 'B';
      case 2:
        return 'C';
      case 3:
        return 'D';
      default:
        return '';
    }
  }
}
