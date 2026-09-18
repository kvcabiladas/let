import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../data/questions_repository.dart';
import '../models/question.dart';
import '../models/quiz_session.dart';
import '../models/quiz_subject.dart';
import 'firestore_sync_service.dart';

class SavedSessionData {
  final String subjectId;
  final int sectionId;
  final int currentIndex;
  final Map<int, int> userAnswers;
  final Set<int> bookmarkedIndices;
  final int elapsedSeconds;
  final QuizMode mode;
  final List<int> questionIds;

  SavedSessionData({
    this.subjectId = 'gen_ed',
    required this.sectionId,
    required this.currentIndex,
    required this.userAnswers,
    required this.bookmarkedIndices,
    required this.elapsedSeconds,
    required this.mode,
    required this.questionIds,
  });
}

class StorageService {
  static const String _keyBestScorePrefix = 'best_score_';
  static const String _keyLastMode = 'last_quiz_mode';
  static const String _keyRandomize = 'randomize_questions';
  static const String _keySavedSessionPrefix = 'saved_session_';
  static const String _keyCompletedSessionPrefix = 'completed_session_';

  static String _scoreKey(String subjectId, int sectionId) {
    return '$_keyBestScorePrefix${subjectId}_sec_$sectionId';
  }

  static String _sessionKey(String subjectId, int sectionId) {
    return '$_keySavedSessionPrefix${subjectId}_sec_$sectionId';
  }

  static String _completedSessionKey(String subjectId, int sectionId) {
    return '$_keyCompletedSessionPrefix${subjectId}_sec_$sectionId';
  }

  /// Sync all data from/to Cloud Firestore
  static Future<void> syncWithCloud() async {
    await FirestoreSyncService.syncAllData();
  }

  /// Clear all local scores and saved sessions (e.g. on sign out if switching user)
  static Future<void> clearAllLocalData() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
  }

  static Future<void> saveSectionScore(
      String subjectId, int sectionId, int score, int total) async {
    final prefs = await SharedPreferences.getInstance();
    final key = _scoreKey(subjectId, sectionId);
    final currentBest = prefs.getInt(key) ?? 0;
    if (score > currentBest) {
      await prefs.setInt(key, score);
      // Trigger cloud sync
      FirestoreSyncService.syncBestScore(subjectId, sectionId, score);
    }
  }

  static Future<int> getSectionBestScore(
      String subjectId, int sectionId) async {
    final prefs = await SharedPreferences.getInstance();
    final key = _scoreKey(subjectId, sectionId);
    if (prefs.containsKey(key)) {
      return prefs.getInt(key) ?? 0;
    }
    // Fallback check for legacy keys if subjectId == 'gen_ed'
    if (subjectId == 'gen_ed') {
      return prefs.getInt('best_score_sec_$sectionId') ?? 0;
    }
    return 0;
  }

  static Future<Map<int, int>> getAllBestScores(
      String subjectId, int totalSections) async {
    final prefs = await SharedPreferences.getInstance();
    final Map<int, int> scores = {};
    for (int i = 1; i <= totalSections; i++) {
      final key = _scoreKey(subjectId, i);
      if (prefs.containsKey(key)) {
        scores[i] = prefs.getInt(key) ?? 0;
      } else if (subjectId == 'gen_ed' &&
          prefs.containsKey('best_score_sec_$i')) {
        scores[i] = prefs.getInt('best_score_sec_$i') ?? 0;
      } else {
        scores[i] = 0;
      }
    }
    return scores;
  }

  static Future<void> saveLastMode(QuizMode mode) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyLastMode, mode.name);
    FirestoreSyncService.syncSettings(lastQuizMode: mode.name);
  }

  static Future<QuizMode> getLastMode() async {
    final prefs = await SharedPreferences.getInstance();
    final modeStr = prefs.getString(_keyLastMode);
    if (modeStr == QuizMode.instantCheck.name) {
      return QuizMode.instantCheck;
    }
    return QuizMode.checkAtEnd;
  }

  static Future<void> saveRandomizeSetting(bool value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_keyRandomize, value);
    FirestoreSyncService.syncSettings(randomize: value);
  }

  static Future<bool> getRandomizeSetting() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_keyRandomize) ?? true;
  }

  // Session Progress Persistence
  static Future<void> saveSessionProgress(QuizSession session) async {
    final prefs = await SharedPreferences.getInstance();
    final data = {
      'subjectId': session.subjectId,
      'sectionId': session.sectionId,
      'currentIndex': session.currentIndex,
      'userAnswers':
          session.userAnswers.map((k, v) => MapEntry(k.toString(), v)),
      'bookmarkedIndices': session.bookmarkedIndices.toList(),
      'elapsedSeconds': session.elapsedSeconds,
      'mode': session.mode.name,
      'questionIds': session.questions.map((q) => q.id).toList(),
      'updatedAt': DateTime.now().toIso8601String(),
    };
    await prefs.setString(
        _sessionKey(session.subjectId, session.sectionId), jsonEncode(data));
    FirestoreSyncService.syncSessionProgress(
        session.subjectId, session.sectionId, data);
  }

  static Future<bool> hasSavedProgress(String subjectId, int sectionId) async {
    final prefs = await SharedPreferences.getInstance();
    final key = _sessionKey(subjectId, sectionId);
    if (prefs.containsKey(key)) {
      return true;
    }
    if (subjectId == 'gen_ed' &&
        prefs.containsKey('saved_session_sec_$sectionId')) {
      return true;
    }
    return false;
  }

  static Future<Map<int, bool>> getAllSavedProgressStatus(
      String subjectId, int totalSections) async {
    final prefs = await SharedPreferences.getInstance();
    final Map<int, bool> status = {};
    for (int i = 1; i <= totalSections; i++) {
      final key = _sessionKey(subjectId, i);
      if (prefs.containsKey(key)) {
        status[i] = true;
      } else if (subjectId == 'gen_ed' &&
          prefs.containsKey('saved_session_sec_$i')) {
        status[i] = true;
      } else {
        status[i] = false;
      }
    }
    return status;
  }

  static Future<SavedSessionData?> loadSavedProgress(
      String subjectId, int sectionId) async {
    final prefs = await SharedPreferences.getInstance();
    String? jsonStr = prefs.getString(_sessionKey(subjectId, sectionId));
    if (jsonStr == null && subjectId == 'gen_ed') {
      jsonStr = prefs.getString('saved_session_sec_$sectionId');
    }
    if (jsonStr == null) return null;

    try {
      final Map<String, dynamic> data = jsonDecode(jsonStr);
      final rawAnswers = data['userAnswers'] as Map<String, dynamic>;
      final userAnswers =
          rawAnswers.map((k, v) => MapEntry(int.parse(k), v as int));
      final bookmarkedIndices =
          (data['bookmarkedIndices'] as List).map((e) => e as int).toSet();
      final questionIds =
          (data['questionIds'] as List).map((e) => e as int).toList();
      final modeStr = data['mode'] as String;
      final mode = modeStr == QuizMode.instantCheck.name
          ? QuizMode.instantCheck
          : QuizMode.checkAtEnd;

      return SavedSessionData(
        subjectId: (data['subjectId'] as String?) ?? subjectId,
        sectionId: data['sectionId'] as int,
        currentIndex: data['currentIndex'] as int,
        userAnswers: userAnswers,
        bookmarkedIndices: bookmarkedIndices,
        elapsedSeconds: data['elapsedSeconds'] as int,
        mode: mode,
        questionIds: questionIds,
      );
    } catch (e) {
      return null;
    }
  }

  static Future<void> clearSavedProgress(
      String subjectId, int sectionId) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_sessionKey(subjectId, sectionId));
    if (subjectId == 'gen_ed') {
      await prefs.remove('saved_session_sec_$sectionId');
    }
    FirestoreSyncService.syncClearSavedProgress(subjectId, sectionId);
  }

  // Completed Session Persistence
  static Future<void> saveCompletedSession(QuizSession session) async {
    final prefs = await SharedPreferences.getInstance();
    final data = {
      'subjectId': session.subjectId,
      'sectionId': session.sectionId,
      'sectionTitle': session.sectionTitle,
      'currentIndex': session.currentIndex,
      'userAnswers':
          session.userAnswers.map((k, v) => MapEntry(k.toString(), v)),
      'bookmarkedIndices': session.bookmarkedIndices.toList(),
      'elapsedSeconds': session.elapsedSeconds,
      'mode': session.mode.name,
      'questionIds': session.questions.map((q) => q.id).toList(),
      'isSubmitted': true,
      'completedAt': DateTime.now().toIso8601String(),
    };
    await prefs.setString(_completedSessionKey(session.subjectId, session.sectionId),
        jsonEncode(data));
    FirestoreSyncService.syncCompletedSession(
        session.subjectId, session.sectionId, data);
  }

  static Future<bool> hasCompletedSession(
      String subjectId, int sectionId) async {
    final prefs = await SharedPreferences.getInstance();
    final key = _completedSessionKey(subjectId, sectionId);
    if (prefs.containsKey(key)) {
      return true;
    }
    if (subjectId == 'gen_ed' &&
        prefs.containsKey('completed_session_sec_$sectionId')) {
      return true;
    }
    return false;
  }

  static Future<Map<int, bool>> getAllCompletedSessionStatus(
      String subjectId, int totalSections) async {
    final prefs = await SharedPreferences.getInstance();
    final Map<int, bool> status = {};
    for (int i = 1; i <= totalSections; i++) {
      final key = _completedSessionKey(subjectId, i);
      if (prefs.containsKey(key)) {
        status[i] = true;
      } else if (subjectId == 'gen_ed' &&
          prefs.containsKey('completed_session_sec_$i')) {
        status[i] = true;
      } else {
        status[i] = false;
      }
    }
    return status;
  }

  static Future<QuizSession?> loadCompletedSession(
      String subjectId, int sectionId) async {
    final prefs = await SharedPreferences.getInstance();
    String? jsonStr =
        prefs.getString(_completedSessionKey(subjectId, sectionId));
    if (jsonStr == null && subjectId == 'gen_ed') {
      jsonStr = prefs.getString('completed_session_sec_$sectionId');
    }
    if (jsonStr == null) return null;

    try {
      final Map<String, dynamic> data = jsonDecode(jsonStr);
      final rawAnswers = data['userAnswers'] as Map<String, dynamic>;
      final userAnswers =
          rawAnswers.map((k, v) => MapEntry(int.parse(k), v as int));
      final bookmarkedIndices =
          (data['bookmarkedIndices'] as List).map((e) => e as int).toSet();
      final questionIds =
          (data['questionIds'] as List).map((e) => e as int).toList();
      final modeStr = data['mode'] as String;
      final mode = modeStr == QuizMode.instantCheck.name
          ? QuizMode.instantCheck
          : QuizMode.checkAtEnd;

      final subject = QuizSubject.getById(subjectId);
      final allQuestions =
          QuestionsRepository.getQuestionsForSection(subjectId, sectionId);
      final questionMap = {for (var q in allQuestions) q.id: q};
      final orderedQuestions = questionIds
          .map((id) => questionMap[id])
          .whereType<Question>()
          .toList();

      if (orderedQuestions.isEmpty) return null;

      return QuizSession(
        subjectId: (data['subjectId'] as String?) ?? subjectId,
        sectionId: data['sectionId'] as int,
        sectionTitle: (data['sectionTitle'] as String?) ??
            '${subject.subtitle} • Section $sectionId',
        mode: mode,
        questions: orderedQuestions,
        currentIndex: (data['currentIndex'] as int?) ?? 0,
        userAnswers: userAnswers,
        bookmarkedIndices: bookmarkedIndices,
        elapsedSeconds: (data['elapsedSeconds'] as int?) ?? 0,
        isSubmitted: true,
      );
    } catch (e) {
      return null;
    }
  }

  static Future<void> clearCompletedSession(
      String subjectId, int sectionId) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_completedSessionKey(subjectId, sectionId));
    if (subjectId == 'gen_ed') {
      await prefs.remove('completed_session_sec_$sectionId');
    }
    FirestoreSyncService.syncClearCompletedSession(subjectId, sectionId);
  }
}
