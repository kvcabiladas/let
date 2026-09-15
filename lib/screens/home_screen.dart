import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/quiz_subject.dart';
import '../theme/app_theme.dart';
import '../services/storage_service.dart';
import 'subject_sections_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final Map<String, int> _subjectTotalScores = {};
  final Map<String, int> _subjectPassedSections = {};
  bool _isLoading = true;
  String _selectedCategory = 'all'; // 'all', 'bped', 'gen_ed', 'prof_ed'

  @override
  void initState() {
    super.initState();
    _loadAllSubjectStats();
  }

  Future<void> _loadAllSubjectStats() async {
    for (final subject in QuizSubject.availableSubjects) {
      final scores = await StorageService.getAllBestScores(
        subject.id,
        subject.totalSections,
      );
      final sum = scores.values.fold(0, (prev, element) => prev + element);
      final passScore = (subject.itemsPerSection * 0.75).ceil();
      final passedCount = scores.values.where((score) => score >= passScore).length;

      _subjectTotalScores[subject.id] = sum;
      _subjectPassedSections[subject.id] = passedCount;
    }

    if (mounted) {
      setState(() {
        _isLoading = false;
      });
    }
  }

  int get _overallTotalScoreSum {
    return _subjectTotalScores.values.fold(0, (sum, score) => sum + score);
  }

  int get _overallTotalPassedSections {
    return _subjectPassedSections.values.fold(0, (sum, count) => sum + count);
  }

  void _onSubjectSelected(QuizSubject subject) async {
    await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => SubjectSectionsScreen(subject: subject),
      ),
    );
    _loadAllSubjectStats();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundNavy,
      appBar: AppBar(
        title: Row(
          children: [
            const Icon(Icons.school_rounded, color: AppTheme.accentGold, size: 26),
            const SizedBox(width: 10),
            Text(
              'LET PORTAL & REVIEWER',
              style: GoogleFonts.outfit(
                fontWeight: FontWeight.w800,
                letterSpacing: 1.2,
                fontSize: 18,
              ),
            ),
          ],
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
                  // Dashboard Banner Card
                  _buildDashboardBanner(),
                  const SizedBox(height: 24),

                  // Section Navigation Filter Tabs (BPED, GEN ED, PROF ED)
                  _buildSectionCategoryTabs(),
                  const SizedBox(height: 24),

                  // Display Sections Content based on filter
                  if (_selectedCategory == 'all' || _selectedCategory == 'bped')
                    _buildMainCategorySection(
                      categoryKey: 'bped',
                      sectionTitle: '1. BPED (Bachelor of Physical Education)',
                      badgeColor: const Color(0xFF10B981),
                      icon: Icons.fitness_center_rounded,
                      subtitle: 'Sports, Fitness & Movement Science',
                    ),

                  if (_selectedCategory == 'all' || _selectedCategory == 'gen_ed') ...[
                    if (_selectedCategory == 'all') const SizedBox(height: 28),
                    _buildMainCategorySection(
                      categoryKey: 'gen_ed',
                      sectionTitle: '2. GEN ED (General Education)',
                      badgeColor: AppTheme.accentGold,
                      icon: Icons.school_rounded,
                      subtitle: 'English, Mathematics, Science & Social Science',
                    ),
                  ],

                  if (_selectedCategory == 'all' || _selectedCategory == 'prof_ed') ...[
                    if (_selectedCategory == 'all') const SizedBox(height: 28),
                    _buildMainCategorySection(
                      categoryKey: 'prof_ed',
                      sectionTitle: '3. PROF ED (Professional Education)',
                      badgeColor: const Color(0xFFA855F7),
                      icon: Icons.psychology_rounded,
                      subtitle: 'Teaching Profession, Pedagogy & Assessment',
                    ),
                  ],
                ],
              ),
            ),
    );
  }

  Widget _buildDashboardBanner() {
    final totalAppQuestions = QuizSubject.availableSubjects.fold(
      0,
      (sum, s) => sum + s.totalQuestions,
    );
    final overallPercentage = (totalAppQuestions > 0)
        ? (_overallTotalScoreSum / totalAppQuestions) * 100
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
            blurRadius: 12,
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
                child: const Icon(
                  Icons.verified_user_rounded,
                  color: AppTheme.accentGold,
                  size: 30,
                ),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Licensure Exam Portal',
                      style: GoogleFonts.outfit(
                        fontSize: 19,
                        fontWeight: FontWeight.bold,
                        color: AppTheme.textWhite,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      'BPED • GEN ED • PROF ED Practice Drills',
                      style: GoogleFonts.inter(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: AppTheme.accentCyan,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 18),

          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Total Drill High Score: $_overallTotalScoreSum / $totalAppQuestions',
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
          const SizedBox(height: 16),

          Row(
            children: [
              _buildDashboardStat(
                icon: Icons.folder_copy_rounded,
                label: 'Main Sections',
                value: '3 Sections',
                color: AppTheme.accentCyan,
              ),
              const SizedBox(width: 10),
              _buildDashboardStat(
                icon: Icons.quiz_rounded,
                label: 'Total Items',
                value: '$totalAppQuestions Questions',
                color: const Color(0xFF10B981),
              ),
              const SizedBox(width: 10),
              _buildDashboardStat(
                icon: Icons.check_circle_outline_rounded,
                label: 'Passed Secs',
                value: '$_overallTotalPassedSections Passed',
                color: AppTheme.successGreen,
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildDashboardStat({
    required IconData icon,
    required String label,
    required String value,
    required Color color,
  }) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Row(
          children: [
            Icon(icon, color: color, size: 16),
            const SizedBox(width: 6),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    label,
                    style: GoogleFonts.inter(
                      fontSize: 9,
                      color: AppTheme.textMuted,
                    ),
                  ),
                  Text(
                    value,
                    style: GoogleFonts.outfit(
                      fontSize: 11,
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

  Widget _buildSectionCategoryTabs() {
    final categories = [
      {'key': 'all', 'label': 'ALL SECTIONS', 'icon': Icons.grid_view_rounded},
      {'key': 'bped', 'label': 'BPED', 'icon': Icons.fitness_center_rounded},
      {'key': 'gen_ed', 'label': 'GEN ED', 'icon': Icons.school_rounded},
      {'key': 'prof_ed', 'label': 'PROF ED', 'icon': Icons.psychology_rounded},
    ];

    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: Row(
        children: categories.map((cat) {
          final isSelected = _selectedCategory == cat['key'];
          return Padding(
            padding: const EdgeInsets.only(right: 10),
            child: ChoiceChip(
              showCheckmark: false,
              avatar: Icon(
                cat['icon'] as IconData,
                size: 16,
                color: isSelected ? AppTheme.primaryNavy : AppTheme.accentCyan,
              ),
              label: Text(
                cat['label'] as String,
                style: GoogleFonts.outfit(
                  fontSize: 13,
                  fontWeight: FontWeight.bold,
                  color: isSelected ? AppTheme.primaryNavy : AppTheme.textWhite,
                  letterSpacing: 0.8,
                ),
              ),
              selected: isSelected,
              selectedColor: AppTheme.accentCyan,
              backgroundColor: AppTheme.cardNavy,
              side: BorderSide(
                color: isSelected ? AppTheme.accentCyan : AppTheme.borderNavy,
                width: 1.5,
              ),
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
              onSelected: (selected) {
                if (selected) {
                  setState(() {
                    _selectedCategory = cat['key'] as String;
                  });
                }
              },
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildMainCategorySection({
    required String categoryKey,
    required String sectionTitle,
    required Color badgeColor,
    required IconData icon,
    required String subtitle,
  }) {
    final quizSubjects = QuizSubject.getByCategory(categoryKey);

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: AppTheme.cardNavy.withOpacity(0.8),
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: badgeColor.withOpacity(0.4), width: 1.5),
        boxShadow: const [
          BoxShadow(
            color: Colors.black26,
            blurRadius: 10,
            offset: Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Section Title Header
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: badgeColor.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: badgeColor, width: 1.5),
                ),
                child: Icon(icon, color: badgeColor, size: 24),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      sectionTitle,
                      style: GoogleFonts.outfit(
                        fontSize: 17,
                        fontWeight: FontWeight.bold,
                        color: AppTheme.textWhite,
                      ),
                    ),
                    Text(
                      subtitle,
                      style: GoogleFonts.inter(
                        fontSize: 12,
                        color: AppTheme.textMuted,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          const Divider(color: AppTheme.borderNavy),
          const SizedBox(height: 14),

          // Sub-heading for Quiz Subjects
          Row(
            children: [
              Icon(Icons.quiz_rounded, color: AppTheme.accentCyan, size: 18),
              const SizedBox(width: 8),
              Text(
                'PRACTICE DRILLS',
                style: GoogleFonts.outfit(
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                  color: AppTheme.accentCyan,
                  letterSpacing: 1.0,
                ),
              ),
              const Spacer(),
              Text(
                '${quizSubjects.length} ${quizSubjects.length == 1 ? "Drill" : "Drills"}',
                style: GoogleFonts.inter(fontSize: 11, color: AppTheme.textMuted),
              ),
            ],
          ),
          const SizedBox(height: 12),

          // List of Quiz Subject Cards
          ...quizSubjects.map((subject) {
            final highScoresSum = _subjectTotalScores[subject.id] ?? 0;
            final passedSections = _subjectPassedSections[subject.id] ?? 0;
            return _buildSubjectCard(subject, highScoresSum, passedSections, badgeColor);
          }),
        ],
      ),
    );
  }

  Widget _buildSubjectCard(
    QuizSubject subject,
    int highScoresSum,
    int passedSectionsCount,
    Color themeColor,
  ) {
    final maxScore = subject.totalQuestions;
    final percentage = maxScore > 0 ? (highScoresSum / maxScore) * 100 : 0.0;

    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      child: Card(
        color: AppTheme.backgroundNavy,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: BorderSide(color: themeColor.withOpacity(0.4), width: 1.2),
        ),
        child: InkWell(
          onTap: () => _onSubjectSelected(subject),
          borderRadius: BorderRadius.circular(16),
          child: Padding(
            padding: const EdgeInsets.all(14.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Container(
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: themeColor.withOpacity(0.15),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: themeColor, width: 1.2),
                      ),
                      child: Icon(
                        _getSubjectIconData(subject.iconType),
                        color: themeColor,
                        size: 24,
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            subject.title,
                            style: GoogleFonts.outfit(
                              fontSize: 15,
                              fontWeight: FontWeight.bold,
                              color: AppTheme.textWhite,
                            ),
                          ),
                          Text(
                            subject.subtitle,
                            style: GoogleFonts.inter(
                              fontSize: 12,
                              fontWeight: FontWeight.w600,
                              color: AppTheme.accentCyan,
                            ),
                          ),
                        ],
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: themeColor.withOpacity(0.15),
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(color: themeColor.withOpacity(0.5)),
                      ),
                      child: Text(
                        '${subject.totalSections} Secs',
                        style: GoogleFonts.outfit(
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                          color: themeColor,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                Text(
                  subject.description,
                  style: GoogleFonts.inter(
                    fontSize: 11,
                    color: AppTheme.textMuted,
                  ),
                ),
                const SizedBox(height: 12),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'Score: $highScoresSum / $maxScore',
                      style: GoogleFonts.inter(
                        fontSize: 11,
                        fontWeight: FontWeight.w600,
                        color: AppTheme.textWhite,
                      ),
                    ),
                    Text(
                      '$passedSectionsCount/${subject.totalSections} Passed',
                      style: GoogleFonts.outfit(
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                        color: passedSectionsCount > 0
                            ? AppTheme.successGreen
                            : AppTheme.textDim,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 6),
                ClipRRect(
                  borderRadius: BorderRadius.circular(6),
                  child: LinearProgressIndicator(
                    value: (percentage / 100).clamp(0.0, 1.0),
                    minHeight: 6,
                    backgroundColor: AppTheme.cardNavy,
                    color: themeColor,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  IconData _getSubjectIconData(String iconType) {
    switch (iconType) {
      case 'bped':
        return Icons.fitness_center_rounded;
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
}
