import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/quiz_session.dart';
import '../theme/app_theme.dart';
import '../services/storage_service.dart';
import 'quiz_screen.dart';
import 'review_screen.dart';

class ResultsScreen extends StatefulWidget {
  final QuizSession session;

  const ResultsScreen({super.key, required this.session});

  @override
  State<ResultsScreen> createState() => _ResultsScreenState();
}

class _ResultsScreenState extends State<ResultsScreen> {
  @override
  void initState() {
    super.initState();
    _saveResults();
  }

  Future<void> _saveResults() async {
    await StorageService.saveSectionScore(
      widget.session.subjectId,
      widget.session.sectionId,
      widget.session.correctCount,
      widget.session.totalQuestions,
    );
    await StorageService.saveCompletedSession(widget.session);
  }

  String _formatDuration(int seconds) {
    final mins = seconds ~/ 60;
    final secs = seconds % 60;
    if (mins == 0) return '${secs}s';
    return '${mins}m ${secs}s';
  }

  @override
  Widget build(BuildContext context) {
    final score = widget.session.correctCount;
    final total = widget.session.totalQuestions;
    final percentage = widget.session.scorePercentage;
    final isPassed = percentage >= 75.0;

    return Scaffold(
      backgroundColor: AppTheme.backgroundNavy,
      appBar: AppBar(
        title: Text(
          'Assessment Results',
          style: GoogleFonts.outfit(fontWeight: FontWeight.bold),
        ),
        automaticallyImplyLeading: false,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            // Score Summary Card
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: AppTheme.cardNavy,
                borderRadius: BorderRadius.circular(24),
                border: Border.all(color: AppTheme.borderNavy),
                boxShadow: const [
                  BoxShadow(
                    color: Colors.black38,
                    blurRadius: 12,
                    offset: Offset(0, 4),
                  ),
                ],
              ),
              child: Column(
                children: [
                  // Pass / Fail Badge
                  Container(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 16, vertical: 6),
                    decoration: BoxDecoration(
                      color: isPassed
                          ? AppTheme.successGreenBg
                          : AppTheme.errorRedBg,
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(
                        color: isPassed
                            ? AppTheme.successGreen
                            : AppTheme.errorRed,
                      ),
                    ),
                    child: Text(
                      isPassed ? 'PASSED LET DRILL' : 'NEEDS IMPROVEMENT',
                      style: GoogleFonts.outfit(
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                        color: isPassed
                            ? AppTheme.successGreen
                            : AppTheme.errorRed,
                        letterSpacing: 1.2,
                      ),
                    ),
                  ),
                  const SizedBox(height: 20),

                  // Circular Score Gauge
                  Stack(
                    alignment: Alignment.center,
                    children: [
                      SizedBox(
                        width: 140,
                        height: 140,
                        child: CircularProgressIndicator(
                          value: percentage / 100,
                          strokeWidth: 12,
                          backgroundColor: AppTheme.borderNavy,
                          color: isPassed
                              ? AppTheme.successGreen
                              : AppTheme.errorRed,
                        ),
                      ),
                      Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(
                            '${percentage.toStringAsFixed(1)}%',
                            style: GoogleFonts.outfit(
                              fontSize: 32,
                              fontWeight: FontWeight.bold,
                              color: AppTheme.textWhite,
                            ),
                          ),
                          Text(
                            '$score / $total',
                            style: GoogleFonts.inter(
                              fontSize: 14,
                              color: AppTheme.textMuted,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                  const SizedBox(height: 20),

                  Text(
                    'Section ${widget.session.sectionId} Completed',
                    style: GoogleFonts.outfit(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.accentGold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Mode: ${widget.session.mode == QuizMode.instantCheck ? "Instant Checking" : "Check at End"}',
                    style: GoogleFonts.inter(
                      fontSize: 12,
                      color: AppTheme.textMuted,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Performance Breakdown Grid
            Row(
              children: [
                Expanded(
                  child: _buildMetricTile(
                    label: 'Correct',
                    value: '$score',
                    icon: Icons.check_circle_rounded,
                    color: AppTheme.successGreen,
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: _buildMetricTile(
                    label: 'Incorrect',
                    value: '${widget.session.incorrectCount}',
                    icon: Icons.cancel_rounded,
                    color: AppTheme.errorRed,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(
                  child: _buildMetricTile(
                    label: 'Unanswered',
                    value: '${widget.session.unansweredCount}',
                    icon: Icons.remove_circle_outline_rounded,
                    color: AppTheme.warningOrange,
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: _buildMetricTile(
                    label: 'Time Spent',
                    value: _formatDuration(widget.session.elapsedSeconds),
                    icon: Icons.timer_rounded,
                    color: AppTheme.accentCyan,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),

            // Action Buttons
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => ReviewScreen(session: widget.session),
                    ),
                  );
                },
                icon: const Icon(Icons.rate_review_rounded, color: Colors.black),
                label: const Text('Review Detailed Answers'),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
              ),
            ),
            const SizedBox(height: 12),

            Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () {
                      Navigator.pushReplacement(
                        context,
                        MaterialPageRoute(
                          builder: (context) => QuizScreen(
                            sectionId: widget.session.sectionId,
                            mode: widget.session.mode,
                            randomize: true,
                          ),
                        ),
                      );
                    },
                    icon: const Icon(Icons.replay_rounded, size: 18),
                    label: const Text('Retake'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () {
                      Navigator.popUntil(context, (route) => route.isFirst);
                    },
                    icon: const Icon(Icons.home_rounded, size: 18),
                    label: const Text('Dashboard'),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMetricTile({
    required String label,
    required String value,
    required IconData icon,
    required Color color,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppTheme.cardNavy,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppTheme.borderNavy),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: color.withOpacity(0.15),
              shape: BoxShape.circle,
            ),
            child: Icon(icon, color: color, size: 20),
          ),
          const SizedBox(width: 12),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                label,
                style: GoogleFonts.inter(
                  fontSize: 11,
                  color: AppTheme.textMuted,
                ),
              ),
              Text(
                value,
                style: GoogleFonts.outfit(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: AppTheme.textWhite,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
