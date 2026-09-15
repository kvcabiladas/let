import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/quiz_session.dart';
import '../models/quiz_subject.dart';
import '../theme/app_theme.dart';
import '../services/storage_service.dart';
import 'quiz_screen.dart';
import 'results_screen.dart';

class SubjectSectionsScreen extends StatefulWidget {
  final QuizSubject subject;

  const SubjectSectionsScreen({super.key, required this.subject});

  @override
  State<SubjectSectionsScreen> createState() => _SubjectSectionsScreenState();
}

class _SubjectSectionsScreenState extends State<SubjectSectionsScreen> {
  QuizMode _selectedMode = QuizMode.instantCheck;
  bool _randomizeQuestions = true;
  Map<int, int> _bestScores = {};
  Map<int, bool> _savedProgressStatus = {};
  Map<int, bool> _completedStatus = {};
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final mode = await StorageService.getLastMode();
    final randomize = await StorageService.getRandomizeSetting();
    final scores = await StorageService.getAllBestScores(
      widget.subject.id,
      widget.subject.totalSections,
    );
    final savedStatus = await StorageService.getAllSavedProgressStatus(
      widget.subject.id,
      widget.subject.totalSections,
    );
    final completedStatus = await StorageService.getAllCompletedSessionStatus(
      widget.subject.id,
      widget.subject.totalSections,
    );

    if (mounted) {
      setState(() {
        _selectedMode = mode;
        _randomizeQuestions = randomize;
        _bestScores = scores;
        _savedProgressStatus = savedStatus;
        _completedStatus = completedStatus;
        _isLoading = false;
      });
    }
  }

  Future<void> _updateMode(QuizMode mode) async {
    setState(() => _selectedMode = mode);
    await StorageService.saveLastMode(mode);
  }

  Future<void> _toggleRandomize(bool val) async {
    setState(() => _randomizeQuestions = val);
    await StorageService.saveRandomizeSetting(val);
  }

  void _viewAssessmentSummary(int sectionId) async {
    final completedSession = await StorageService.loadCompletedSession(
      widget.subject.id,
      sectionId,
    );
    if (completedSession != null && mounted) {
      await Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ResultsScreen(session: completedSession),
        ),
      );
      _loadSettings();
    }
  }

  void _onSectionTap(int sectionId) async {
    final hasSaved = _savedProgressStatus[sectionId] ?? false;
    final hasCompleted = _completedStatus[sectionId] ?? false;

    if (hasSaved) {
      final savedData = await StorageService.loadSavedProgress(
        widget.subject.id,
        sectionId,
      );

      if (savedData != null && mounted) {
        final choice = await showDialog<String>(
          context: context,
          builder: (context) => AlertDialog(
            backgroundColor: AppTheme.cardNavy,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
            title: Row(
              children: [
                const Icon(Icons.history_toggle_off_rounded,
                    color: AppTheme.accentGold),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    'Saved Progress Found',
                    style: GoogleFonts.outfit(
                      color: AppTheme.textWhite,
                      fontWeight: FontWeight.bold,
                      fontSize: 18,
                    ),
                  ),
                ),
              ],
            ),
            content: Text(
              'You have saved progress for Section $sectionId (${savedData.userAnswers.length} items answered). Would you like to resume or start fresh?',
              style: GoogleFonts.inter(color: AppTheme.textWhite, fontSize: 14),
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context, 'fresh'),
                child: Text(
                  'Start Fresh',
                  style: GoogleFonts.outfit(color: AppTheme.errorRed),
                ),
              ),
              ElevatedButton(
                onPressed: () => Navigator.pop(context, 'resume'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.accentGold,
                ),
                child: Text(
                  'Resume Progress',
                  style: GoogleFonts.outfit(
                    color: Colors.black,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
        );

        if (choice == 'resume' && mounted) {
          await Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => QuizScreen(
                subjectId: widget.subject.id,
                sectionId: sectionId,
                mode: savedData.mode,
                randomize: false,
                restoredSession: savedData,
              ),
            ),
          );
          _loadSettings();
          return;
        } else if (choice == 'fresh') {
          await StorageService.clearSavedProgress(widget.subject.id, sectionId);
        } else {
          return;
        }
      }
    } else if (hasCompleted) {
      if (mounted) {
        final choice = await showDialog<String>(
          context: context,
          builder: (context) => AlertDialog(
            backgroundColor: AppTheme.cardNavy,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
            title: Row(
              children: [
                const Icon(Icons.assessment_rounded,
                    color: AppTheme.accentGold),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    'Section $sectionId Attempted',
                    style: GoogleFonts.outfit(
                      color: AppTheme.textWhite,
                      fontWeight: FontWeight.bold,
                      fontSize: 18,
                    ),
                  ),
                ),
              ],
            ),
            content: Text(
              'You have a saved assessment summary for Section $sectionId. Would you like to view your last results or retake this section?',
              style: GoogleFonts.inter(color: AppTheme.textWhite, fontSize: 14),
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context, 'summary'),
                child: Text(
                  'View Summary',
                  style: GoogleFonts.outfit(color: AppTheme.accentCyan, fontWeight: FontWeight.bold),
                ),
              ),
              ElevatedButton(
                onPressed: () => Navigator.pop(context, 'retake'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.accentGold,
                ),
                child: Text(
                  'Retake Section',
                  style: GoogleFonts.outfit(
                    color: Colors.black,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
        );

        if (choice == 'summary') {
          _viewAssessmentSummary(sectionId);
          return;
        } else if (choice != 'retake') {
          return;
        }
      }
    }

    if (mounted) {
      await Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => QuizScreen(
            subjectId: widget.subject.id,
            sectionId: sectionId,
            mode: _selectedMode,
            randomize: _randomizeQuestions,
          ),
        ),
      );
      _loadSettings();
    }
  }

  int get _totalPassedSections {
    // 50 items section: >= 38 is passing (76%)
    final passScore = (widget.subject.itemsPerSection * 0.75).ceil();
    return _bestScores.values.where((score) => score >= passScore).length;
  }

  int get _overallBestScoreSum {
    return _bestScores.values.fold(0, (sum, score) => sum + score);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundNavy,
      appBar: AppBar(
        title: Text(
          widget.subject.title.toUpperCase(),
          style: GoogleFonts.outfit(
            fontWeight: FontWeight.w800,
            letterSpacing: 1.2,
            fontSize: 17,
          ),
        ),
        elevation: 0,
        backgroundColor: AppTheme.primaryNavy,
      ),
      body: _isLoading
          ? const Center(
              child: CircularProgressIndicator(color: AppTheme.accentGold),
            )
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Subject Header Dashboard
                  _buildSubjectHeader(),
                  const SizedBox(height: 20),

                  // Mode Selector Card
                  _buildModeSelector(),
                  const SizedBox(height: 20),

                  // Section Title Header
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        'DRILL SECTIONS (${widget.subject.itemsPerSection} ITEMS EACH)',
                        style: GoogleFonts.outfit(
                          fontSize: 13,
                          fontWeight: FontWeight.bold,
                          color: AppTheme.accentCyan,
                          letterSpacing: 1.1,
                        ),
                      ),
                      Text(
                        '${widget.subject.totalQuestions} Total Items',
                        style: GoogleFonts.inter(
                          fontSize: 12,
                          color: AppTheme.textMuted,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),

                  // Section Cards List
                  ListView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: widget.subject.totalSections,
                    itemBuilder: (context, index) {
                      final sectionId = index + 1;
                      final bestScore = _bestScores[sectionId] ?? 0;
                      final hasSaved = _savedProgressStatus[sectionId] ?? false;
                      final hasCompleted = _completedStatus[sectionId] ?? false;
                      return _buildSectionCard(sectionId, bestScore, hasSaved, hasCompleted);
                    },
                  ),
                ],
              ),
            ),
    );
  }

  Widget _buildSubjectHeader() {
    final maxPossibleScore = widget.subject.totalQuestions;
    final overallPercentage = (maxPossibleScore > 0)
        ? (_overallBestScoreSum / maxPossibleScore) * 100
        : 0.0;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [
            Color(0xFF0F172A),
            Color(0xFF1E293B),
            Color(0xFF111827),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppTheme.borderNavy, width: 1.5),
        boxShadow: const [
          BoxShadow(
            color: Colors.black38,
            blurRadius: 10,
            offset: Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: AppTheme.accentGold.withOpacity(0.15),
                  shape: BoxShape.circle,
                  border: Border.all(color: AppTheme.accentGold, width: 1.5),
                ),
                child: Icon(
                  _getSubjectIconData(widget.subject.iconType),
                  color: AppTheme.accentGold,
                  size: 28,
                ),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      widget.subject.title,
                      style: GoogleFonts.outfit(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: AppTheme.textWhite,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      widget.subject.subtitle,
                      style: GoogleFonts.inter(
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                        color: AppTheme.accentCyan,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            widget.subject.description,
            style: GoogleFonts.inter(
              fontSize: 12,
              color: AppTheme.textMuted,
              height: 1.4,
            ),
          ),
          const SizedBox(height: 18),

          // Progress Overview Bar
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'High Score Sum: $_overallBestScoreSum / $maxPossibleScore',
                style: GoogleFonts.inter(
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: AppTheme.textWhite,
                ),
              ),
              Text(
                '${overallPercentage.toStringAsFixed(1)}%',
                style: GoogleFonts.outfit(
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  color: AppTheme.accentGold,
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          ClipRRect(
            borderRadius: BorderRadius.circular(10),
            child: LinearProgressIndicator(
              value: (overallPercentage / 100).clamp(0.0, 1.0),
              minHeight: 10,
              backgroundColor: AppTheme.borderNavy,
              color: AppTheme.accentGold,
            ),
          ),
          const SizedBox(height: 14),

          // Stats Chips
          Row(
            children: [
              _buildHeaderStat(
                icon: Icons.check_circle_rounded,
                label: 'Passed',
                value: '$_totalPassedSections / ${widget.subject.totalSections} Secs',
                color: AppTheme.successGreen,
              ),
              const SizedBox(width: 12),
              _buildHeaderStat(
                icon: Icons.assignment_turned_in_rounded,
                label: 'Items/Sec',
                value: '${widget.subject.itemsPerSection} Items',
                color: AppTheme.accentCyan,
              ),
            ],
          ),
        ],
      ),
    );
  }

  IconData _getSubjectIconData(String iconType) {
    switch (iconType) {
      case 'gen_ed':
        return Icons.school_rounded;
      case 'prof_150':
        return Icons.assignment_turned_in_rounded;
      case 'prof_1000':
        return Icons.quiz_rounded;
      default:
        return Icons.menu_book_rounded;
    }
  }

  Widget _buildHeaderStat({
    required IconData icon,
    required String label,
    required String value,
    required Color color,
  }) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Row(
          children: [
            Icon(icon, color: color, size: 18),
            const SizedBox(width: 8),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    label,
                    style: GoogleFonts.inter(
                      fontSize: 10,
                      color: AppTheme.textMuted,
                    ),
                  ),
                  Text(
                    value,
                    style: GoogleFonts.outfit(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.textWhite,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildModeSelector() {
    return Card(
      color: AppTheme.cardNavy,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(
                  Icons.settings_suggest_rounded,
                  color: AppTheme.accentGold,
                  size: 20,
                ),
                const SizedBox(width: 8),
                Text(
                  'ASSESSMENT SETTINGS',
                  style: GoogleFonts.outfit(
                    fontSize: 13,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.textWhite,
                    letterSpacing: 1.1,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 14),

            // Mode Selection Segment
            Text(
              'Checking Mode:',
              style: GoogleFonts.inter(
                fontSize: 12,
                color: AppTheme.textMuted,
              ),
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(
                  child: _buildModeOption(
                    mode: QuizMode.instantCheck,
                    title: 'Instant Check',
                    subtitle: 'Immediate Answer Key',
                    icon: Icons.bolt_rounded,
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: _buildModeOption(
                    mode: QuizMode.checkAtEnd,
                    title: 'Check at End',
                    subtitle: 'Simulated Exam Mode',
                    icon: Icons.fact_check_rounded,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 14),

            // Randomize Toggle
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
              decoration: BoxDecoration(
                color: AppTheme.backgroundNavy,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppTheme.borderNavy),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      const Icon(
                        Icons.shuffle_rounded,
                        color: AppTheme.accentCyan,
                        size: 20,
                      ),
                      const SizedBox(width: 10),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Randomize Questions',
                            style: GoogleFonts.inter(
                              fontSize: 13,
                              fontWeight: FontWeight.w600,
                              color: AppTheme.textWhite,
                            ),
                          ),
                          Text(
                            'Shuffle item order within section',
                            style: GoogleFonts.inter(
                              fontSize: 11,
                              color: AppTheme.textMuted,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                  Switch(
                    value: _randomizeQuestions,
                    onChanged: _toggleRandomize,
                    activeTrackColor: AppTheme.accentGold,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildModeOption({
    required QuizMode mode,
    required String title,
    required String subtitle,
    required IconData icon,
  }) {
    final isSelected = _selectedMode == mode;
    final activeColor =
        mode == QuizMode.instantCheck ? AppTheme.accentGold : AppTheme.accentCyan;

    return GestureDetector(
      onTap: () => _updateMode(mode),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
        decoration: BoxDecoration(
          color: isSelected ? activeColor.withOpacity(0.15) : AppTheme.backgroundNavy,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isSelected ? activeColor : AppTheme.borderNavy,
            width: isSelected ? 2 : 1,
          ),
        ),
        child: Column(
          children: [
            Icon(
              icon,
              color: isSelected ? activeColor : AppTheme.textMuted,
              size: 24,
            ),
            const SizedBox(height: 6),
            Text(
              title,
              textAlign: TextAlign.center,
              style: GoogleFonts.outfit(
                fontSize: 13,
                fontWeight: FontWeight.bold,
                color: isSelected ? AppTheme.textWhite : AppTheme.textMuted,
              ),
            ),
            const SizedBox(height: 2),
            Text(
              subtitle,
              textAlign: TextAlign.center,
              style: GoogleFonts.inter(
                fontSize: 10,
                color: isSelected ? activeColor : AppTheme.textDim,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionCard(int sectionId, int bestScore, bool hasSaved, bool hasCompleted) {
    final itemsPerSec = widget.subject.itemsPerSection;
    final startNum = (sectionId - 1) * itemsPerSec + 1;
    final endNum = sectionId * itemsPerSec;
    final hasTaken = bestScore > 0 || hasCompleted;
    final passScore = (itemsPerSec * 0.75).ceil(); // 38 out of 50
    final isPassed = bestScore >= passScore;

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      child: Card(
        color: AppTheme.cardNavy,
        child: InkWell(
          onTap: () => _onSectionTap(sectionId),
          borderRadius: BorderRadius.circular(16),
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              children: [
                Row(
                  children: [
                    // Section Number Circle
                    Container(
                      width: 50,
                      height: 50,
                      decoration: BoxDecoration(
                        color: isPassed
                            ? AppTheme.successGreen.withOpacity(0.2)
                            : (hasTaken
                                ? AppTheme.errorRed.withOpacity(0.2)
                                : AppTheme.accentBlue.withOpacity(0.2)),
                        shape: BoxShape.circle,
                        border: Border.all(
                          color: isPassed
                              ? AppTheme.successGreen
                              : (hasTaken ? AppTheme.errorRed : AppTheme.accentBlue),
                          width: 1.5,
                        ),
                      ),
                      child: Center(
                        child: Text(
                          '$sectionId',
                          style: GoogleFonts.outfit(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: isPassed
                                ? AppTheme.successGreen
                                : (hasTaken ? AppTheme.errorRed : AppTheme.textWhite),
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 14),

                    // Section Title & Range
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Text(
                                'SECTION $sectionId',
                                style: GoogleFonts.outfit(
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                  color: AppTheme.textWhite,
                                ),
                              ),
                              if (hasSaved) ...[
                                const SizedBox(width: 8),
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                      horizontal: 8, vertical: 2),
                                  decoration: BoxDecoration(
                                    color: AppTheme.accentGold.withOpacity(0.2),
                                    borderRadius: BorderRadius.circular(6),
                                    border: Border.all(color: AppTheme.accentGold),
                                  ),
                                  child: Text(
                                    'RESUME',
                                    style: GoogleFonts.outfit(
                                      fontSize: 10,
                                      fontWeight: FontWeight.bold,
                                      color: AppTheme.accentGold,
                                    ),
                                  ),
                                ),
                              ] else if (hasTaken) ...[
                                const SizedBox(width: 8),
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                      horizontal: 8, vertical: 2),
                                  decoration: BoxDecoration(
                                    color: isPassed
                                        ? AppTheme.successGreenBg
                                        : AppTheme.errorRedBg,
                                    borderRadius: BorderRadius.circular(6),
                                  ),
                                  child: Text(
                                    isPassed ? 'PASSED' : 'RETAKE',
                                    style: GoogleFonts.outfit(
                                      fontSize: 10,
                                      fontWeight: FontWeight.bold,
                                      color: isPassed
                                          ? AppTheme.successGreen
                                          : AppTheme.errorRed,
                                    ),
                                  ),
                                ),
                              ],
                            ],
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Questions $startNum – $endNum ($itemsPerSec Items)',
                            style: GoogleFonts.inter(
                              fontSize: 12,
                              color: AppTheme.textMuted,
                            ),
                          ),
                        ],
                      ),
                    ),

                    // Score Badge or Start Button
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        if (hasTaken)
                          Text(
                            '$bestScore / $itemsPerSec',
                            style: GoogleFonts.outfit(
                              fontSize: 15,
                              fontWeight: FontWeight.bold,
                              color: isPassed
                                  ? AppTheme.successGreen
                                  : AppTheme.errorRed,
                            ),
                          )
                        else
                          Text(
                            'Unattempted',
                            style: GoogleFonts.inter(
                              fontSize: 11,
                              color: AppTheme.textDim,
                            ),
                          ),
                        const SizedBox(height: 6),
                        Container(
                          padding: const EdgeInsets.all(6),
                          decoration: BoxDecoration(
                            color: AppTheme.accentGold.withOpacity(0.15),
                            shape: BoxShape.circle,
                          ),
                          child: const Icon(
                            Icons.arrow_forward_ios_rounded,
                            color: AppTheme.accentGold,
                            size: 14,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
                if (hasCompleted) ...[
                  const SizedBox(height: 12),
                  const Divider(color: AppTheme.borderNavy, height: 1),
                  const SizedBox(height: 10),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      InkWell(
                        onTap: () => _viewAssessmentSummary(sectionId),
                        borderRadius: BorderRadius.circular(8),
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                          decoration: BoxDecoration(
                            color: AppTheme.accentCyan.withOpacity(0.15),
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: AppTheme.accentCyan.withOpacity(0.5)),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              const Icon(Icons.assessment_rounded,
                                  color: AppTheme.accentCyan, size: 16),
                              const SizedBox(width: 6),
                              Text(
                                'View Last Assessment Summary',
                                style: GoogleFonts.outfit(
                                  fontSize: 12,
                                  fontWeight: FontWeight.bold,
                                  color: AppTheme.accentCyan,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}
