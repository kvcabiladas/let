import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/pdf_reviewer.dart';
import '../theme/app_theme.dart';

class PdfViewerScreen extends StatelessWidget {
  final PdfReviewer pdf;

  const PdfViewerScreen({super.key, required this.pdf});

  Color _getCategoryColor(String category) {
    switch (category) {
      case 'bped':
        return const Color(0xFF10B981); // Emerald / Green for BPED
      case 'gen_ed':
        return AppTheme.accentGold;
      case 'prof_ed':
        return const Color(0xFFA855F7); // Purple accent for ProfEd
      default:
        return AppTheme.accentCyan;
    }
  }

  IconData _getCategoryIcon(String category) {
    switch (category) {
      case 'bped':
        return Icons.fitness_center_rounded;
      case 'gen_ed':
        return Icons.school_rounded;
      case 'prof_ed':
        return Icons.psychology_rounded;
      default:
        return Icons.picture_as_pdf_rounded;
    }
  }

  @override
  Widget build(BuildContext context) {
    final themeColor = _getCategoryColor(pdf.category);
    final iconData = _getCategoryIcon(pdf.category);

    return Scaffold(
      backgroundColor: AppTheme.backgroundNavy,
      appBar: AppBar(
        backgroundColor: AppTheme.primaryNavy,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_rounded, color: AppTheme.textWhite),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          'PDF REVIEWER DETAILS',
          style: GoogleFonts.outfit(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            letterSpacing: 1.2,
            color: AppTheme.textWhite,
          ),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // PDF Hero Header Card
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [
                    themeColor.withOpacity(0.2),
                    AppTheme.cardNavy,
                    AppTheme.primaryNavy,
                  ],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.circular(24),
                border: Border.all(color: themeColor.withOpacity(0.5), width: 1.5),
                boxShadow: const [
                  BoxShadow(
                    color: Colors.black45,
                    blurRadius: 16,
                    offset: Offset(0, 6),
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: themeColor.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(18),
                          border: Border.all(color: themeColor, width: 2),
                        ),
                        child: Icon(
                          Icons.picture_as_pdf_rounded,
                          color: themeColor,
                          size: 40,
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                              decoration: BoxDecoration(
                                color: themeColor.withOpacity(0.25),
                                borderRadius: BorderRadius.circular(8),
                                border: Border.all(color: themeColor),
                              ),
                              child: Text(
                                pdf.badgeText,
                                style: GoogleFonts.outfit(
                                  fontSize: 10,
                                  fontWeight: FontWeight.bold,
                                  color: themeColor,
                                  letterSpacing: 1.0,
                                ),
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              pdf.title,
                              style: GoogleFonts.outfit(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                color: AppTheme.textWhite,
                                height: 1.2,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 20),
                  Text(
                    pdf.description,
                    style: GoogleFonts.inter(
                      fontSize: 14,
                      color: AppTheme.textMuted,
                      height: 1.5,
                    ),
                  ),
                  const SizedBox(height: 20),
                  const Divider(color: AppTheme.borderNavy),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      _buildMetaInfo(Icons.topic_rounded, 'Topic', pdf.topic, themeColor),
                      _buildMetaInfo(Icons.auto_stories_rounded, 'Volume', pdf.pageCount, themeColor),
                      _buildMetaInfo(Icons.data_usage_rounded, 'File Size', pdf.fileSize, themeColor),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // Document Details Section
            Text(
              'DOCUMENT OVERVIEW',
              style: GoogleFonts.outfit(
                fontSize: 13,
                fontWeight: FontWeight.bold,
                color: AppTheme.accentCyan,
                letterSpacing: 1.2,
              ),
            ),
            const SizedBox(height: 12),

            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppTheme.cardNavy,
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: AppTheme.borderNavy),
              ),
              child: Column(
                children: [
                  _buildDetailRow(
                    icon: iconData,
                    title: 'Section Category',
                    value: pdf.category.toUpperCase().replaceAll('_', ' '),
                    color: themeColor,
                  ),
                  const Divider(color: AppTheme.borderNavy, height: 24),
                  _buildDetailRow(
                    icon: Icons.folder_zip_rounded,
                    title: 'Asset Location',
                    value: pdf.assetPath,
                    color: AppTheme.accentCyan,
                  ),
                  const Divider(color: AppTheme.borderNavy, height: 24),
                  _buildDetailRow(
                    icon: Icons.verified_rounded,
                    title: 'Status',
                    value: 'Ready for Review & Study',
                    color: AppTheme.successGreen,
                  ),
                ],
              ),
            ),
            const SizedBox(height: 30),

            // Action Buttons
            SizedBox(
              width: double.infinity,
              height: 54,
              child: ElevatedButton.icon(
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      backgroundColor: AppTheme.primaryNavy,
                      content: Row(
                        children: [
                          Icon(Icons.check_circle_rounded, color: themeColor),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Text(
                              'Opening "${pdf.title}" asset...',
                              style: GoogleFonts.inter(color: AppTheme.textWhite),
                            ),
                          ),
                        ],
                      ),
                    ),
                  );
                },
                icon: const Icon(Icons.file_open_rounded, color: AppTheme.primaryNavy),
                label: Text(
                  'OPEN / VIEW PDF DOCUMENT',
                  style: GoogleFonts.outfit(
                    fontSize: 15,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.0,
                    color: AppTheme.primaryNavy,
                  ),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: themeColor,
                  elevation: 6,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: OutlinedButton.icon(
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      backgroundColor: AppTheme.primaryNavy,
                      content: Row(
                        children: const [
                          Icon(Icons.download_done_rounded, color: AppTheme.accentGold),
                          SizedBox(width: 12),
                          Expanded(
                            child: Text(
                              'Document saved locally for offline study.',
                              style: TextStyle(color: AppTheme.textWhite),
                            ),
                          ),
                        ],
                      ),
                    ),
                  );
                },
                icon: const Icon(Icons.download_rounded, color: AppTheme.accentCyan),
                label: Text(
                  'SAVE FOR OFFLINE STUDY',
                  style: GoogleFonts.outfit(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.accentCyan,
                  ),
                ),
                style: OutlinedButton.styleFrom(
                  side: const BorderSide(color: AppTheme.borderNavy, width: 1.5),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMetaInfo(IconData icon, String label, String value, Color color) {
    return Column(
      children: [
        Icon(icon, color: color, size: 20),
        const SizedBox(height: 4),
        Text(
          label,
          style: GoogleFonts.inter(fontSize: 11, color: AppTheme.textMuted),
        ),
        const SizedBox(height: 2),
        Text(
          value,
          style: GoogleFonts.outfit(
            fontSize: 12,
            fontWeight: FontWeight.bold,
            color: AppTheme.textWhite,
          ),
        ),
      ],
    );
  }

  Widget _buildDetailRow({
    required IconData icon,
    required String title,
    required String value,
    required Color color,
  }) {
    return Row(
      children: [
        Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(
            color: color.withOpacity(0.15),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Icon(icon, color: color, size: 20),
        ),
        const SizedBox(width: 14),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: GoogleFonts.inter(
                  fontSize: 12,
                  color: AppTheme.textMuted,
                ),
              ),
              Text(
                value,
                style: GoogleFonts.outfit(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                  color: AppTheme.textWhite,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
