class PdfReviewer {
  final String id;
  final String title;
  final String category; // 'bped', 'gen_ed', 'prof_ed'
  final String assetPath;
  final String description;
  final String fileSize;
  final String pageCount;
  final String badgeText;
  final String topic;

  const PdfReviewer({
    required this.id,
    required this.title,
    required this.category,
    required this.assetPath,
    required this.description,
    required this.fileSize,
    required this.pageCount,
    required this.badgeText,
    required this.topic,
  });
}
