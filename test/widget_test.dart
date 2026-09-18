import 'package:flutter_test/flutter_test.dart';
import 'package:topnotcher_yarn/data/questions_repository.dart';
import 'package:topnotcher_yarn/models/quiz_subject.dart';

void main() {
  test('QuizSubject and QuestionsRepository initialize correctly', () {
    expect(QuizSubject.availableSubjects.isNotEmpty, isTrue);
  });

  test('gen_ed_qa has 10 sections with 500 total valid questions', () {
    final subject = QuizSubject.getById('gen_ed_qa');
    expect(subject.totalSections, 10);
    expect(subject.totalQuestions, 500);

    int totalCount = 0;
    for (int section = 1; section <= 10; section++) {
      final questions = QuestionsRepository.getQuestionsForSection('gen_ed_qa', section);
      expect(questions.length, 50);
      for (final q in questions) {
        expect(q.id, greaterThan(0));
        expect(q.questionText.trim().isNotEmpty, isTrue);
        expect(q.options.length, greaterThanOrEqualTo(3));
        expect(q.correctAnswerIndex, greaterThanOrEqualTo(0));
        expect(q.correctAnswerIndex, lessThan(q.options.length));
      }
      totalCount += questions.length;
    }
    expect(totalCount, 500);
  });

  test('prof_ed_qa has 10 sections with 499 total valid questions', () {
    final subject = QuizSubject.getById('prof_ed_qa');
    expect(subject.totalSections, 10);
    expect(subject.totalQuestions, 499);

    int totalCount = 0;
    for (int section = 1; section <= 10; section++) {
      final questions = QuestionsRepository.getQuestionsForSection('prof_ed_qa', section);
      if (section < 10) {
        expect(questions.length, 50);
      } else {
        expect(questions.length, 49);
      }
      for (final q in questions) {
        expect(q.id, greaterThan(0));
        expect(q.questionText.trim().isNotEmpty, isTrue);
        expect(q.options.length, greaterThanOrEqualTo(3));
        expect(q.correctAnswerIndex, greaterThanOrEqualTo(0));
        expect(q.correctAnswerIndex, lessThan(q.options.length));
      }
      totalCount += questions.length;
    }
    expect(totalCount, 499);
  });
}
