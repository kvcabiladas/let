import 'dart:async';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../data/questions_repository.dart';
import '../models/question.dart';
import '../models/quiz_session.dart';
import '../models/quiz_subject.dart';
import '../services/storage_service.dart';
import '../theme/app_theme.dart';
import 'results_screen.dart';

class QuizScreen extends StatefulWidget {
  final String subjectId;
  final int sectionId;
  final QuizMode mode;
  final bool randomize;
  final SavedSessionData? restoredSession;

  const QuizScreen({
    super.key,
    this.subjectId = 'gen_ed',
    required this.sectionId,
    required this.mode,
    required this.randomize,
    this.restoredSession,
  });

  @override
  State<QuizScreen> createState() => _QuizScreenState();
}

class _QuizScreenState extends State<QuizScreen> {
  late QuizSession _session;
  late Timer _timer;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _initSession();
    _startTimer();
  }

  void _initSession() {
    final subject = QuizSubject.getById(widget.subjectId);
    if (widget.restoredSession != null) {
      final restored = widget.restoredSession!;
      final allQuestions = QuestionsRepository.getQuestionsForSection(widget.subjectId, widget.sectionId);
      final questionMap = {for (var q in allQuestions) q.id: q};
      final restoredQuestions = restored.questionIds
          .map((id) => questionMap[id])
          .whereType<Question>()
          .toList();

      _session = QuizSession(
        subjectId: widget.subjectId,
        sectionId: widget.sectionId,
        sectionTitle: '${subject.subtitle} • Section ${widget.sectionId}',
        mode: restored.mode,
        questions: restoredQuestions,
        currentIndex: restored.currentIndex,
        userAnswers: Map<int, int>.from(restored.userAnswers),
        bookmarkedIndices: Set<int>.from(restored.bookmarkedIndices),
        elapsedSeconds: restored.elapsedSeconds,
      );
    } else {
      final rawQuestions = QuestionsRepository.getQuestionsForSection(widget.subjectId, widget.sectionId);
      final questions = List<Question>.from(rawQuestions);
      if (widget.randomize) {
        questions.shuffle();
      }

      _session = QuizSession(
        subjectId: widget.subjectId,
        sectionId: widget.sectionId,
        sectionTitle: '${subject.subtitle} • Section ${widget.sectionId}',
        mode: widget.mode,
        questions: questions,
      );
    }

    setState(() {
      _isLoading = false;
    });
  }

  void _startTimer() {
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (mounted && !_session.isSubmitted) {
        setState(() {
          _session.elapsedSeconds++;
        });
      }
    });
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  Future<bool> _onWillPop() async {
    final result = await showDialog<String>(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: AppTheme.cardNavy,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: Row(
          children: [
            const Icon(Icons.exit_to_app_rounded, color: AppTheme.accentGold),
            const SizedBox(width: 10),
            Text(
              'Exit Assessment?',
              style: GoogleFonts.outfit(
                color: AppTheme.textWhite,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
        content: Text(
          'Would you like to save your current progress before exiting?',
          style: GoogleFonts.inter(color: AppTheme.textWhite, fontSize: 14),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, 'cancel'),
            child: Text(
              'Cancel',
              style: GoogleFonts.outfit(color: AppTheme.textMuted),
            ),
          ),
          OutlinedButton(
            onPressed: () => Navigator.pop(context, 'discard'),
            style: OutlinedButton.styleFrom(
              side: const BorderSide(color: AppTheme.errorRed),
            ),
            child: Text(
              'Discard',
              style: GoogleFonts.outfit(color: AppTheme.errorRed),
            ),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(context, 'save'),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.accentGold,
            ),
            child: Text(
              'Save & Exit',
              style: GoogleFonts.outfit(
                color: Colors.black,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ],
      ),
    );

    if (result == 'save') {
      await StorageService.saveSessionProgress(_session);
      return true;
    } else if (result == 'discard') {
      await StorageService.clearSavedProgress(widget.subjectId, widget.sectionId);
      return true;
    }

    return false;
  }

  void _selectOption(int optionIndex) {
    if (_session.mode == QuizMode.instantCheck &&
        _session.userAnswers.containsKey(_session.currentIndex)) {
      return;
    }

    setState(() {
      _session.userAnswers[_session.currentIndex] = optionIndex;
    });
  }

  void _nextQuestion() {
    if (_session.currentIndex < _session.totalQuestions - 1) {
      setState(() {
        _session.currentIndex++;
      });
    } else if (_session.mode == QuizMode.checkAtEnd) {
      _confirmSubmission();
    }
  }

  void _previousQuestion() {
    if (_session.currentIndex > 0) {
      setState(() {
        _session.currentIndex--;
      });
    }
  }

  void _toggleBookmark() {
    setState(() {
      if (_session.bookmarkedIndices.contains(_session.currentIndex)) {
        _session.bookmarkedIndices.remove(_session.currentIndex);
      } else {
        _session.bookmarkedIndices.add(_session.currentIndex);
      }
    });
  }

  Widget _buildStatItem(String label, String value, Color color, IconData icon) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 14, color: color),
            const SizedBox(width: 4),
            Text(
              value,
              style: GoogleFonts.outfit(
                fontSize: 15,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
          ],
        ),
        const SizedBox(height: 2),
        Text(
          label,
          style: GoogleFonts.inter(
            fontSize: 10,
            color: AppTheme.textMuted,
          ),
        ),
      ],
    );
  }

  void _confirmSubmission() {
    final answered = _session.answeredCount;
    final unanswered = _session.unansweredCount;
    final bookmarked = _session.bookmarkedIndices.length;
    final total = _session.totalQuestions;

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: AppTheme.cardNavy,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: AppTheme.accentGold.withValues(alpha: 0.15),
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.help_outline_rounded, color: AppTheme.accentGold, size: 22),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: Text(
                'Finish Section?',
                style: GoogleFonts.outfit(
                  color: AppTheme.textWhite,
                  fontWeight: FontWeight.bold,
                  fontSize: 18,
                ),
              ),
            ),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Are you sure you want to finish and submit this section? Here is your summary:',
              style: GoogleFonts.inter(color: AppTheme.textWhite, fontSize: 13, height: 1.4),
            ),
            const SizedBox(height: 14),

            // Stat Summary Cards
            Container(
              padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 8),
              decoration: BoxDecoration(
                color: AppTheme.backgroundNavy,
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: AppTheme.borderNavy),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _buildStatItem('Answered', '$answered/$total', AppTheme.accentCyan, Icons.check_circle_outline_rounded),
                  Container(height: 28, width: 1, color: AppTheme.borderNavy),
                  _buildStatItem(
                    'Unanswered',
                    '$unanswered',
                    unanswered > 0 ? AppTheme.warningOrange : AppTheme.textMuted,
                    Icons.help_outline_rounded,
                  ),
                  Container(height: 28, width: 1, color: AppTheme.borderNavy),
                  _buildStatItem('Bookmarked', '$bookmarked', AppTheme.accentGold, Icons.bookmark_border_rounded),
                ],
              ),
            ),

            if (unanswered > 0 || bookmarked > 0) ...[
              const SizedBox(height: 16),
              Text(
                'Review Options:',
                style: GoogleFonts.outfit(
                  color: AppTheme.textMuted,
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 0.8,
                ),
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  if (unanswered > 0)
                    Expanded(
                      child: OutlinedButton.icon(
                        onPressed: () {
                          Navigator.pop(context);
                          _openQuestionGridSheet(initialFilter: 'unanswered');
                        },
                        style: OutlinedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 8),
                          side: const BorderSide(color: AppTheme.warningOrange),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                        ),
                        icon: const Icon(Icons.help_outline_rounded, size: 14, color: AppTheme.warningOrange),
                        label: Text(
                          'Unanswered ($unanswered)',
                          style: GoogleFonts.outfit(
                            fontSize: 11,
                            color: AppTheme.warningOrange,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                  if (unanswered > 0 && bookmarked > 0) const SizedBox(width: 8),
                  if (bookmarked > 0)
                    Expanded(
                      child: OutlinedButton.icon(
                        onPressed: () {
                          Navigator.pop(context);
                          _openQuestionGridSheet(initialFilter: 'bookmarked');
                        },
                        style: OutlinedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 8),
                          side: const BorderSide(color: AppTheme.accentGold),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                        ),
                        icon: const Icon(Icons.bookmark_rounded, size: 14, color: AppTheme.accentGold),
                        label: Text(
                          'Bookmarked ($bookmarked)',
                          style: GoogleFonts.outfit(
                            fontSize: 11,
                            color: AppTheme.accentGold,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                ],
              ),
            ],
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text(
              'Keep Answering',
              style: GoogleFonts.outfit(color: AppTheme.textMuted),
            ),
          ),
          ElevatedButton.icon(
            onPressed: () {
              Navigator.pop(context);
              _finishQuiz();
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.accentGold,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
            ),
            icon: const Icon(Icons.check_circle_rounded, size: 16, color: Colors.black),
            label: Text(
              unanswered > 0 ? 'Submit Anyway' : 'Submit Now',
              style: GoogleFonts.outfit(
                color: Colors.black,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _finishQuiz() async {
    _session.isSubmitted = true;
    await StorageService.saveCompletedSession(_session);
    await StorageService.clearSavedProgress(widget.subjectId, widget.sectionId);
    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => ResultsScreen(session: _session),
        ),
      );
    }
  }

  void _openQuestionGridSheet({String initialFilter = 'all'}) {
    showModalBottomSheet(
      context: context,
      backgroundColor: AppTheme.cardNavy,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (context) => StatefulBuilder(
        builder: (context, setSheetState) {
          String activeFilter = initialFilter;

          return Container(
            padding: const EdgeInsets.all(20),
            height: MediaQuery.of(context).size.height * 0.75,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Header
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'QUESTION NAVIGATOR (${_session.totalQuestions} ITEMS)',
                      style: GoogleFonts.outfit(
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                        color: AppTheme.accentGold,
                        letterSpacing: 1.1,
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.close_rounded, color: AppTheme.textMuted),
                      onPressed: () => Navigator.pop(context),
                    ),
                  ],
                ),
                const SizedBox(height: 8),

                // Filter Tabs (All, Unanswered, Bookmarked)
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: [
                      _buildFilterChip(
                        filterKey: 'all',
                        label: 'All (${_session.totalQuestions})',
                        activeFilter: activeFilter,
                        onSelected: (val) => setSheetState(() => activeFilter = val),
                      ),
                      const SizedBox(width: 8),
                      _buildFilterChip(
                        filterKey: 'unanswered',
                        label: 'Unanswered (${_session.unansweredCount})',
                        activeFilter: activeFilter,
                        onSelected: (val) => setSheetState(() => activeFilter = val),
                      ),
                      const SizedBox(width: 8),
                      _buildFilterChip(
                        filterKey: 'bookmarked',
                        label: 'Bookmarked (${_session.bookmarkedIndices.length})',
                        activeFilter: activeFilter,
                        onSelected: (val) => setSheetState(() => activeFilter = val),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 12),

                // Legend
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    _buildLegendItem(AppTheme.accentCyan, 'Answered'),
                    _buildLegendItem(AppTheme.borderNavy, 'Unanswered'),
                    _buildLegendItem(AppTheme.accentGold, 'Bookmarked'),
                  ],
                ),
                const SizedBox(height: 14),

                // Question Grid
                Expanded(
                  child: GridView.builder(
                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 6,
                      crossAxisSpacing: 10,
                      mainAxisSpacing: 10,
                      childAspectRatio: 1,
                    ),
                    itemCount: _session.totalQuestions,
                    itemBuilder: (context, index) {
                      final isAnswered = _session.userAnswers.containsKey(index);
                      final isCurrent = index == _session.currentIndex;
                      final isBookmarked = _session.bookmarkedIndices.contains(index);

                      bool isFilteredOut = false;
                      if (activeFilter == 'unanswered' && isAnswered) {
                        isFilteredOut = true;
                      } else if (activeFilter == 'bookmarked' && !isBookmarked) {
                        isFilteredOut = true;
                      }

                      return GestureDetector(
                        onTap: () {
                          setState(() {
                            _session.currentIndex = index;
                          });
                          Navigator.pop(context);
                        },
                        child: AnimatedOpacity(
                          duration: const Duration(milliseconds: 200),
                          opacity: isFilteredOut ? 0.25 : 1.0,
                          child: _buildGridItemCell(index, isAnswered, isCurrent, isBookmarked),
                        ),
                      );
                    },
                  ),
                ),
                const SizedBox(height: 12),

                // Finish Section Button
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: () {
                      Navigator.pop(context);
                      _confirmSubmission();
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppTheme.accentGold,
                      padding: const EdgeInsets.symmetric(vertical: 12),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                    icon: const Icon(Icons.flag_rounded, color: Colors.black, size: 18),
                    label: Text(
                      'Finish & Submit Section',
                      style: GoogleFonts.outfit(
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                        color: Colors.black,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildFilterChip({
    required String filterKey,
    required String label,
    required String activeFilter,
    required ValueChanged<String> onSelected,
  }) {
    final isSelected = activeFilter == filterKey;
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
      backgroundColor: AppTheme.backgroundNavy,
      showCheckmark: false,
      side: BorderSide(
        color: isSelected ? AppTheme.accentGold : AppTheme.borderNavy,
      ),
      onSelected: (selected) {
        if (selected) {
          onSelected(filterKey);
        }
      },
    );
  }

  Widget _buildGridItemCell(int index, bool isAnswered, bool isCurrent, bool isBookmarked) {
    Color bgColor = AppTheme.backgroundNavy;
    Color borderColor = AppTheme.borderNavy;

    if (isAnswered) {
      bgColor = AppTheme.accentCyan.withValues(alpha: 0.2);
      borderColor = AppTheme.accentCyan;
    }

    if (isBookmarked) {
      borderColor = AppTheme.accentGold;
    }

    if (isCurrent) {
      bgColor = AppTheme.accentGold.withValues(alpha: 0.3);
      borderColor = AppTheme.accentGold;
    }

    return Container(
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(
          color: borderColor,
          width: isCurrent ? 2 : 1,
        ),
      ),
      child: Stack(
        children: [
          Center(
            child: Text(
              '${index + 1}',
              style: GoogleFonts.outfit(
                fontSize: 13,
                fontWeight: isCurrent ? FontWeight.bold : FontWeight.w600,
                color: isCurrent ? AppTheme.accentGold : AppTheme.textWhite,
              ),
            ),
          ),
          if (isBookmarked)
            const Positioned(
              top: 2,
              right: 2,
              child: Icon(
                Icons.bookmark_rounded,
                size: 10,
                color: AppTheme.accentGold,
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildLegendItem(Color color, String label) {
    return Row(
      children: [
        Container(
          width: 12,
          height: 12,
          decoration: BoxDecoration(
            color: color,
            borderRadius: BorderRadius.circular(3),
          ),
        ),
        const SizedBox(width: 6),
        Text(
          label,
          style: GoogleFonts.inter(fontSize: 11, color: AppTheme.textMuted),
        ),
      ],
    );
  }

  String _formatTime(int seconds) {
    final mins = seconds ~/ 60;
    final secs = seconds % 60;
    return '${mins.toString().padLeft(2, '0')}:${secs.toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(
        backgroundColor: AppTheme.backgroundNavy,
        body: Center(
          child: CircularProgressIndicator(color: AppTheme.accentGold),
        ),
      );
    }

    final currentQ = _session.currentQuestion;
    final isBookmarked = _session.bookmarkedIndices.contains(_session.currentIndex);
    final hasAnsweredCurrent = _session.userAnswers.containsKey(_session.currentIndex);
    final selectedOptionIndex = _session.userAnswers[_session.currentIndex];

    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, result) async {
        if (didPop) return;
        final shouldPop = await _onWillPop();
        if (shouldPop && context.mounted) {
          Navigator.pop(context);
        }
      },
      child: Scaffold(
        backgroundColor: AppTheme.backgroundNavy,
        appBar: AppBar(
          title: Text(
            'Section ${widget.sectionId}',
            style: GoogleFonts.outfit(fontWeight: FontWeight.bold),
          ),
          leading: IconButton(
            icon: const Icon(Icons.arrow_back_rounded),
            onPressed: () async {
              final shouldPop = await _onWillPop();
              if (shouldPop && context.mounted) {
                Navigator.pop(context);
              }
            },
          ),
          actions: [
            // Timer Display Badge
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              margin: const EdgeInsets.only(right: 8),
              decoration: BoxDecoration(
                color: AppTheme.backgroundNavy,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: AppTheme.borderNavy),
              ),
              child: Row(
                children: [
                  const Icon(Icons.timer_outlined,
                      color: AppTheme.accentCyan, size: 16),
                  const SizedBox(width: 4),
                  Text(
                    _formatTime(_session.elapsedSeconds),
                    style: GoogleFonts.outfit(
                      fontSize: 13,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.accentCyan,
                    ),
                  ),
                ],
              ),
            ),

            // Question Grid Drawer Button
            IconButton(
              icon: const Icon(Icons.grid_view_rounded, color: AppTheme.accentGold),
              onPressed: () => _openQuestionGridSheet(),
              tooltip: 'Question Grid',
            ),
          ],
        ),
        body: Column(
          children: [
            // Progress Bar Header
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
              color: AppTheme.primaryNavy,
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        'Question ${_session.currentIndex + 1} of ${_session.totalQuestions}',
                        style: GoogleFonts.outfit(
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                          color: AppTheme.textWhite,
                        ),
                      ),
                      Text(
                        'Mode: ${_session.mode == QuizMode.instantCheck ? "Instant Check" : "Check at End"}',
                        style: GoogleFonts.inter(
                          fontSize: 11,
                          color: _session.mode == QuizMode.instantCheck
                              ? AppTheme.accentGold
                              : AppTheme.accentCyan,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(6),
                    child: LinearProgressIndicator(
                      value: (_session.currentIndex + 1) / _session.totalQuestions,
                      minHeight: 6,
                      backgroundColor: AppTheme.borderNavy,
                      color: AppTheme.accentGold,
                    ),
                  ),
                ],
              ),
            ),

            // Question & Options Content Area
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Question Card
                    _buildQuestionCard(currentQ),
                    const SizedBox(height: 20),

                    // Option Cards (A, B, C, D)
                    ...List.generate(currentQ.options.length, (optIndex) {
                      return _buildOptionCard(
                        optionIndex: optIndex,
                        optionText: currentQ.options[optIndex],
                        question: currentQ,
                        hasAnswered: hasAnsweredCurrent,
                        selectedOptionIndex: selectedOptionIndex,
                      );
                    }),

                    // Instant Feedback Banner (for Instant Checking mode)
                    if (_session.mode == QuizMode.instantCheck && hasAnsweredCurrent) ...[
                      const SizedBox(height: 16),
                      _buildInstantFeedbackCard(currentQ, selectedOptionIndex!),
                    ],
                  ],
                ),
              ),
            ),

            // Bottom Control Navigation Toolbar
            _buildBottomToolbar(isBookmarked),
          ],
        ),
      ),
    );
  }

  Widget _buildQuestionCard(Question question) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppTheme.cardNavy,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppTheme.borderNavy),
        boxShadow: const [
          BoxShadow(
            color: Colors.black26,
            blurRadius: 8,
            offset: Offset(0, 3),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
            decoration: BoxDecoration(
              color: AppTheme.accentBlue.withValues(alpha: 0.2),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: AppTheme.accentBlue.withValues(alpha: 0.4)),
            ),
            child: Text(
              'Item #${question.id}',
              style: GoogleFonts.outfit(
                fontSize: 12,
                fontWeight: FontWeight.bold,
                color: AppTheme.accentBlue,
              ),
            ),
          ),
          const SizedBox(height: 14),

          // Question Text
          Text(
            question.questionText,
            style: GoogleFonts.inter(
              fontSize: 16,
              height: 1.4,
              fontWeight: FontWeight.w600,
              color: AppTheme.textWhite,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildOptionCard({
    required int optionIndex,
    required String optionText,
    required Question question,
    required bool hasAnswered,
    required int? selectedOptionIndex,
  }) {
    final optionLetter = String.fromCharCode(65 + optionIndex);
    final isSelected = selectedOptionIndex == optionIndex;
    final isCorrect = question.correctAnswerIndex == optionIndex;

    Color bgColor = AppTheme.cardNavy;
    Color borderColor = AppTheme.borderNavy;
    Color letterBg = AppTheme.backgroundNavy;
    Color letterTextColor = AppTheme.textWhite;

    if (_session.mode == QuizMode.instantCheck && hasAnswered) {
      if (isCorrect) {
        bgColor = AppTheme.successGreenBg.withValues(alpha: 0.6);
        borderColor = AppTheme.successGreen;
        letterBg = AppTheme.successGreen;
        letterTextColor = Colors.white;
      } else if (isSelected && !isCorrect) {
        bgColor = AppTheme.errorRedBg.withValues(alpha: 0.6);
        borderColor = AppTheme.errorRed;
        letterBg = AppTheme.errorRed;
        letterTextColor = Colors.white;
      }
    } else {
      if (isSelected) {
        bgColor = AppTheme.accentCyan.withValues(alpha: 0.15);
        borderColor = AppTheme.accentCyan;
        letterBg = AppTheme.accentCyan;
        letterTextColor = Colors.black;
      }
    }

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: () => _selectOption(optionIndex),
          borderRadius: BorderRadius.circular(14),
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 200),
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
            decoration: BoxDecoration(
              color: bgColor,
              borderRadius: BorderRadius.circular(14),
              border: Border.all(color: borderColor, width: isSelected ? 2 : 1),
            ),
            child: Row(
              children: [
                // Option Letter Badge (A, B, C, D)
                Container(
                  width: 34,
                  height: 34,
                  decoration: BoxDecoration(
                    color: letterBg,
                    shape: BoxShape.circle,
                  ),
                  child: Center(
                    child: Text(
                      optionLetter,
                      style: GoogleFonts.outfit(
                        fontSize: 15,
                        fontWeight: FontWeight.bold,
                        color: letterTextColor,
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 14),

                // Option Text
                Expanded(
                  child: Text(
                    optionText,
                    style: GoogleFonts.inter(
                      fontSize: 14,
                      fontWeight:
                          isSelected ? FontWeight.bold : FontWeight.w500,
                      color: AppTheme.textWhite,
                    ),
                  ),
                ),

                // Instant Check Feedback Icons
                if (_session.mode == QuizMode.instantCheck && hasAnswered) ...[
                  if (isCorrect)
                    const Icon(Icons.check_circle_rounded,
                        color: AppTheme.successGreen, size: 24)
                  else if (isSelected && !isCorrect)
                    const Icon(Icons.cancel_rounded,
                        color: AppTheme.errorRed, size: 24),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildInstantFeedbackCard(Question question, int selectedIndex) {
    final isCorrect = question.correctAnswerIndex == selectedIndex;
    final correctLetter = question.correctAnswerLetter;
    final correctText = question.options[question.correctAnswerIndex];

    return AnimatedContainer(
      duration: const Duration(milliseconds: 300),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isCorrect
            ? AppTheme.successGreenBg.withValues(alpha: 0.4)
            : AppTheme.errorRedBg.withValues(alpha: 0.4),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isCorrect ? AppTheme.successGreen : AppTheme.errorRed,
        ),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(
            isCorrect ? Icons.check_circle_rounded : Icons.info_outline_rounded,
            color: isCorrect ? AppTheme.successGreen : AppTheme.errorRed,
            size: 26,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  isCorrect ? 'Correct Answer!' : 'Incorrect Choice',
                  style: GoogleFonts.outfit(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: isCorrect ? AppTheme.successGreen : AppTheme.errorRed,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  isCorrect
                      ? 'Great job! You selected the correct answer.'
                      : 'The correct answer is Option $correctLetter: "$correctText".',
                  style: GoogleFonts.inter(
                    fontSize: 13,
                    color: AppTheme.textWhite,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBottomToolbar(bool isBookmarked) {
    final isLastQuestion = _session.currentIndex == _session.totalQuestions - 1;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: const BoxDecoration(
        color: AppTheme.primaryNavy,
        border: Border(top: BorderSide(color: AppTheme.borderNavy)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          // Previous Button
          OutlinedButton.icon(
            onPressed: _session.currentIndex > 0 ? _previousQuestion : null,
            icon: const Icon(Icons.arrow_back_ios_rounded, size: 14),
            label: const Text('Prev'),
          ),

          // Bookmark Button
          IconButton(
            onPressed: _toggleBookmark,
            icon: Icon(
              isBookmarked
                  ? Icons.bookmark_rounded
                  : Icons.bookmark_border_rounded,
              color: isBookmarked ? AppTheme.accentGold : AppTheme.textMuted,
            ),
            tooltip: isBookmarked ? 'Remove Bookmark' : 'Bookmark Question',
          ),

          // Next or Submit Button
          if (isLastQuestion)
            ElevatedButton.icon(
              onPressed: _confirmSubmission,
              icon: Icon(
                _session.mode == QuizMode.checkAtEnd
                    ? Icons.send_rounded
                    : Icons.flag_rounded,
                size: 16,
                color: Colors.black,
              ),
              label: Text(_session.mode == QuizMode.checkAtEnd ? 'Submit' : 'Finish'),
            )
          else
            ElevatedButton.icon(
              onPressed: _nextQuestion,
              icon: const Icon(Icons.arrow_forward_ios_rounded,
                  size: 14, color: Colors.black),
              label: const Text('Next'),
            ),
        ],
      ),
    );
  }
}
