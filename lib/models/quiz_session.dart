import 'question.dart';

enum QuizMode {
  instantCheck,
  checkAtEnd,
}

class QuizSection {
  final int id;
  final String title;
  final List<Question> questions;

  const QuizSection({
    required this.id,
    required this.title,
    required this.questions,
  });
}

class QuizSession {
  final String subjectId;
  final int sectionId;
  final String sectionTitle;
  final QuizMode mode;
  final List<Question> questions;
  final Map<int, int> userAnswers; // questionIndex -> selectedOptionIndex
  final Set<int> bookmarkedIndices;
  int currentIndex;
  bool isSubmitted;
  int elapsedSeconds;

  QuizSession({
    this.subjectId = 'gen_ed',
    required this.sectionId,
    required this.sectionTitle,
    required this.mode,
    required this.questions,
    Map<int, int>? userAnswers,
    Set<int>? bookmarkedIndices,
    this.currentIndex = 0,
    this.isSubmitted = false,
    this.elapsedSeconds = 0,
  })  : userAnswers = userAnswers ?? {},
        bookmarkedIndices = bookmarkedIndices ?? {};

  Question get currentQuestion => questions[currentIndex];

  int get totalQuestions => questions.length;

  int get answeredCount => userAnswers.length;

  int get correctCount {
    int count = 0;
    userAnswers.forEach((qIndex, selectedIndex) {
      if (qIndex < questions.length &&
          questions[qIndex].correctAnswerIndex == selectedIndex) {
        count++;
      }
    });
    return count;
  }

  int get incorrectCount {
    int count = 0;
    userAnswers.forEach((qIndex, selectedIndex) {
      if (qIndex < questions.length &&
          questions[qIndex].correctAnswerIndex != selectedIndex) {
        count++;
      }
    });
    return count;
  }

  int get unansweredCount => totalQuestions - answeredCount;

  double get scorePercentage {
    if (totalQuestions == 0) return 0;
    return (correctCount / totalQuestions) * 100;
  }

  bool isCorrect(int index) {
    if (!userAnswers.containsKey(index)) return false;
    return questions[index].correctAnswerIndex == userAnswers[index];
  }
}
