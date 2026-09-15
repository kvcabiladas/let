import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/question.dart';
import '../models/quiz_session.dart';
import '../theme/app_theme.dart';

enum ReviewFilter { all, correct, incorrect, unanswered }

class ReviewScreen extends StatefulWidget {
  final QuizSession session;

  const ReviewScreen({super.key, required this.session});

  @override
  State<ReviewScreen> createState() => _ReviewScreenState();
}

class _ReviewScreenState extends State<ReviewScreen> {
  ReviewFilter _selectedFilter = ReviewFilter.all;

  List<int> get _filteredIndices {
    final List<int> indices = [];
    for (int i = 0; i < widget.session.totalQuestions; i++) {
      final hasAnswered = widget.session.userAnswers.containsKey(i);
      final isCorrect = widget.session.isCorrect(i);

      switch (_selectedFilter) {
        case ReviewFilter.all:
          indices.add(i);
          break;
        case ReviewFilter.correct:
          if (hasAnswered && isCorrect) indices.add(i);
          break;
        case ReviewFilter.incorrect:
          if (hasAnswered && !isCorrect) indices.add(i);
          break;
        case ReviewFilter.unanswered:
          if (!hasAnswered) indices.add(i);
          break;
      }
    }
    return indices;
  }

  @override
  Widget build(BuildContext context) {
    final filteredIndices = _filteredIndices;

    return Scaffold(
      backgroundColor: AppTheme.backgroundNavy,
      appBar: AppBar(
        title: Text(
          'Answer Review',
          style: GoogleFonts.outfit(fontWeight: FontWeight.bold),
        ),
      ),
      body: Column(
        children: [
          // Filter Tabs
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            color: AppTheme.primaryNavy,
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  _buildFilterChip(ReviewFilter.all, 'All (${widget.session.totalQuestions})'),
                  const SizedBox(width: 8),
                  _buildFilterChip(
                      ReviewFilter.correct, 'Correct (${widget.session.correctCount})'),
                  const SizedBox(width: 8),
                  _buildFilterChip(
                      ReviewFilter.incorrect, 'Incorrect (${widget.session.incorrectCount})'),
                  const SizedBox(width: 8),
                  _buildFilterChip(ReviewFilter.unanswered,
                      'Unanswered (${widget.session.unansweredCount})'),
                ],
              ),
            ),
          ),

          // Items List
          Expanded(
            child: filteredIndices.isEmpty
                ? Center(
                    child: Text(
                      'No items match the selected filter.',
                      style: GoogleFonts.inter(color: AppTheme.textMuted),
                    ),
                  )
                : ListView.builder(
                    padding: const EdgeInsets.all(16),
                    itemCount: filteredIndices.length,
                    itemBuilder: (context, idx) {
                      final qIndex = filteredIndices[idx];
                      final question = widget.session.questions[qIndex];
                      final userChoice = widget.session.userAnswers[qIndex];
                      final isCorrect = widget.session.isCorrect(qIndex);
                      final hasAnswered = widget.session.userAnswers.containsKey(qIndex);

                      return _buildReviewCard(
                        qIndex: qIndex,
                        question: question,
                        userChoice: userChoice,
                        isCorrect: isCorrect,
                        hasAnswered: hasAnswered,
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }

  Widget _buildFilterChip(ReviewFilter filter, String label) {
    final isSelected = _selectedFilter == filter;
    return ChoiceChip(
      label: Text(
        label,
        style: GoogleFonts.outfit(
          fontSize: 12,
          fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
          color: isSelected ? Colors.black : AppTheme.textWhite,
        ),
      ),
      selected: isSelected,
      selectedColor: AppTheme.accentGold,
      backgroundColor: AppTheme.cardNavy,
      side: BorderSide(
        color: isSelected ? AppTheme.accentGold : AppTheme.borderNavy,
      ),
      onSelected: (selected) {
        if (selected) {
          setState(() {
            _selectedFilter = filter;
          });
        }
      },
    );
  }

  Widget _buildReviewCard({
    required int qIndex,
    required Question question,
    required int? userChoice,
    required bool isCorrect,
    required bool hasAnswered,
  }) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppTheme.cardNavy,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: !hasAnswered
              ? AppTheme.warningOrange
              : (isCorrect ? AppTheme.successGreen : AppTheme.errorRed),
          width: 1.5,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header Item Number & Status
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Item #${question.id} (Q${qIndex + 1})',
                style: GoogleFonts.outfit(
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  color: AppTheme.accentCyan,
                ),
              ),
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
                decoration: BoxDecoration(
                  color: !hasAnswered
                      ? AppTheme.warningOrange.withOpacity(0.2)
                      : (isCorrect
                          ? AppTheme.successGreenBg
                          : AppTheme.errorRedBg),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  !hasAnswered
                      ? 'UNANSWERED'
                      : (isCorrect ? 'CORRECT' : 'INCORRECT'),
                  style: GoogleFonts.outfit(
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                    color: !hasAnswered
                        ? AppTheme.warningOrange
                        : (isCorrect
                            ? AppTheme.successGreen
                            : AppTheme.errorRed),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),

          // Question Text
          Text(
            question.questionText,
            style: GoogleFonts.inter(
              fontSize: 14,
              fontWeight: FontWeight.w600,
              color: AppTheme.textWhite,
            ),
          ),
          const SizedBox(height: 14),

          // Options Breakdown
          ...List.generate(question.options.length, (optIdx) {
            final optLetter = String.fromCharCode(65 + optIdx);
            final optText = question.options[optIdx];
            final isAnswerKey = question.correctAnswerIndex == optIdx;
            final isUserChoice = userChoice == optIdx;

            Color optionBg = AppTheme.backgroundNavy;
            Color optionBorder = AppTheme.borderNavy;
            Color optionTextColor = AppTheme.textMuted;

            if (isAnswerKey) {
              optionBg = AppTheme.successGreenBg.withOpacity(0.4);
              optionBorder = AppTheme.successGreen;
              optionTextColor = AppTheme.textWhite;
            } else if (isUserChoice && !isAnswerKey) {
              optionBg = AppTheme.errorRedBg.withOpacity(0.4);
              optionBorder = AppTheme.errorRed;
              optionTextColor = AppTheme.textWhite;
            }

            return Container(
              margin: const EdgeInsets.only(bottom: 8),
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
              decoration: BoxDecoration(
                color: optionBg,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: optionBorder),
              ),
              child: Row(
                children: [
                  Text(
                    '$optLetter.',
                    style: GoogleFonts.outfit(
                      fontSize: 13,
                      fontWeight: FontWeight.bold,
                      color: isAnswerKey
                          ? AppTheme.successGreen
                          : (isUserChoice ? AppTheme.errorRed : AppTheme.textMuted),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      optText,
                      style: GoogleFonts.inter(
                        fontSize: 13,
                        color: optionTextColor,
                        fontWeight:
                            (isAnswerKey || isUserChoice) ? FontWeight.bold : FontWeight.normal,
                      ),
                    ),
                  ),
                  if (isAnswerKey)
                    const Icon(Icons.check_circle_rounded,
                        color: AppTheme.successGreen, size: 18),
                  if (isUserChoice && !isAnswerKey)
                    const Icon(Icons.cancel_rounded,
                        color: AppTheme.errorRed, size: 18),
                ],
              ),
            );
          }),
        ],
      ),
    );
  }
}
