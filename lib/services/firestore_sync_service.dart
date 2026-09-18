import 'dart:async';
import 'dart:convert';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

class FirestoreSyncService {
  static final FirebaseFirestore _firestore = FirebaseFirestore.instance;
  static StreamSubscription<DocumentSnapshot<Map<String, dynamic>>>? _realtimeSub;
  static String? _listeningUid;

  /// Global notifier that increments whenever cloud sync updates local data
  static final ValueNotifier<int> syncNotifier = ValueNotifier<int>(0);

  /// Last sync timestamp for UI display
  static DateTime? lastSyncedTime;

  static DocumentReference<Map<String, dynamic>>? get _userDoc {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return null;
    return _firestore.collection('users').doc(user.uid);
  }

  /// Start real-time Firestore auto-sync for the logged-in user
  static void startRealtimeSync(User user) {
    if (_listeningUid == user.uid && _realtimeSub != null) return;
    _listeningUid = user.uid;
    _realtimeSub?.cancel();

    // Perform an initial non-blocking full two-way sync
    syncAllData();

    // Listen to real-time changes on the user document (e.g. from another device)
    _realtimeSub = _firestore
        .collection('users')
        .doc(user.uid)
        .snapshots()
        .listen((snapshot) async {
      if (!snapshot.exists || snapshot.data() == null) return;

      // Skip local-only cache writes to avoid redundant loop processing
      if (snapshot.metadata.hasPendingWrites) return;

      final data = snapshot.data()!;
      await _applyCloudDataToLocal(data);
      lastSyncedTime = DateTime.now();
      syncNotifier.value++;
    }, onError: (e) {
      if (kDebugMode) print('Real-time cloud sync error: $e');
    });
  }

  /// Stop real-time sync (e.g. on logout)
  static void stopRealtimeSync() {
    _realtimeSub?.cancel();
    _realtimeSub = null;
    _listeningUid = null;
  }

  /// Apply incoming cloud data snapshot to local SharedPreferences
  static Future<void> _applyCloudDataToLocal(Map<String, dynamic> data) async {
    try {
      final prefs = await SharedPreferences.getInstance();

      // 1. Best Scores
      final cloudScores = (data['best_scores'] as Map<String, dynamic>?) ?? {};
      for (final entry in cloudScores.entries) {
        final cloudVal = (entry.value is int)
            ? entry.value as int
            : int.tryParse(entry.value.toString()) ?? 0;
        final currentLocal = prefs.getInt('best_score_${entry.key}') ?? 0;
        if (cloudVal > currentLocal) {
          await prefs.setInt('best_score_${entry.key}', cloudVal);
        }
      }

      // 2. Saved In-Progress Sessions
      final cloudSaved = (data['saved_sessions'] as Map<String, dynamic>?) ?? {};
      for (final entry in cloudSaved.entries) {
        final cloudVal = entry.value?.toString();
        if (cloudVal != null && cloudVal.isNotEmpty) {
          final localVal = prefs.getString('saved_session_${entry.key}');
          if (localVal == null) {
            await prefs.setString('saved_session_${entry.key}', cloudVal);
          } else {
            try {
              final localMap = jsonDecode(localVal) as Map<String, dynamic>;
              final cloudMap = jsonDecode(cloudVal) as Map<String, dynamic>;
              final localTime =
                  DateTime.tryParse(localMap['updatedAt']?.toString() ?? '');
              final cloudTime =
                  DateTime.tryParse(cloudMap['updatedAt']?.toString() ?? '');
              if (cloudTime != null &&
                  (localTime == null || cloudTime.isAfter(localTime))) {
                await prefs.setString('saved_session_${entry.key}', cloudVal);
              }
            } catch (_) {
              await prefs.setString('saved_session_${entry.key}', cloudVal);
            }
          }
        }
      }

      // 3. Completed Sessions
      final cloudCompleted =
          (data['completed_sessions'] as Map<String, dynamic>?) ?? {};
      for (final entry in cloudCompleted.entries) {
        final cloudVal = entry.value?.toString();
        if (cloudVal != null && cloudVal.isNotEmpty) {
          final localVal = prefs.getString('completed_session_${entry.key}');
          if (localVal == null) {
            await prefs.setString('completed_session_${entry.key}', cloudVal);
          } else {
            try {
              final localMap = jsonDecode(localVal) as Map<String, dynamic>;
              final cloudMap = jsonDecode(cloudVal) as Map<String, dynamic>;
              final localTime =
                  DateTime.tryParse(localMap['completedAt']?.toString() ?? '');
              final cloudTime =
                  DateTime.tryParse(cloudMap['completedAt']?.toString() ?? '');
              if (cloudTime != null &&
                  (localTime == null || cloudTime.isAfter(localTime))) {
                await prefs.setString('completed_session_${entry.key}', cloudVal);
              }
            } catch (_) {
              await prefs.setString('completed_session_${entry.key}', cloudVal);
            }
          }
        }
      }

      // 4. Settings
      final cloudSettings = (data['settings'] as Map<String, dynamic>?) ?? {};
      if (cloudSettings.containsKey('randomize_questions')) {
        await prefs.setBool(
            'randomize_questions', cloudSettings['randomize_questions'] == true);
      }
      if (cloudSettings.containsKey('last_quiz_mode')) {
        await prefs.setString(
            'last_quiz_mode', cloudSettings['last_quiz_mode'].toString());
      }
    } catch (e) {
      if (kDebugMode) print('Error applying cloud data to local: $e');
    }
  }

  /// Sync all user data between Local SharedPreferences and Cloud Firestore
  /// Designed to be non-blocking with safety timeouts.
  static Future<void> syncAllData() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;

    try {
      final docRef = _firestore.collection('users').doc(user.uid);
      final prefs = await SharedPreferences.getInstance();

      final localBestScores = <String, int>{};
      final localSavedSessions = <String, String>{};
      final localCompletedSessions = <String, String>{};

      // 1. Gather all local keys
      for (final key in prefs.getKeys()) {
        if (key.startsWith('best_score_')) {
          final val = prefs.getInt(key);
          if (val != null) {
            final subKey = key.replaceFirst('best_score_', '');
            localBestScores[subKey] = val;
          }
        } else if (key.startsWith('saved_session_')) {
          final val = prefs.getString(key);
          if (val != null) {
            final subKey = key.replaceFirst('saved_session_', '');
            localSavedSessions[subKey] = val;
          }
        } else if (key.startsWith('completed_session_')) {
          final val = prefs.getString(key);
          if (val != null) {
            final subKey = key.replaceFirst('completed_session_', '');
            localCompletedSessions[subKey] = val;
          }
        }
      }

      // Fetch from Cloud with 5-second timeout to prevent hanging
      final docSnapshot = await docRef
          .get(const GetOptions(source: Source.serverAndCache))
          .timeout(const Duration(seconds: 5));

      if (!docSnapshot.exists) {
        // Document does not exist in Cloud yet. Push local data up.
        await docRef.set({
          'profile': {
            'uid': user.uid,
            'email': user.email ?? '',
            'displayName': user.displayName ?? '',
            'photoUrl': user.photoURL ?? '',
            'lastActiveAt': FieldValue.serverTimestamp(),
          },
          'best_scores': localBestScores,
          'saved_sessions': localSavedSessions,
          'completed_sessions': localCompletedSessions,
          'settings': {
            'randomize_questions': prefs.getBool('randomize_questions') ?? true,
            'last_quiz_mode': prefs.getString('last_quiz_mode') ?? 'checkAtEnd',
          },
          'lastSyncedAt': FieldValue.serverTimestamp(),
        }, SetOptions(merge: true)).timeout(const Duration(seconds: 5));

        lastSyncedTime = DateTime.now();
        syncNotifier.value++;
        return;
      }

      final data = docSnapshot.data() ?? {};

      // 2. Merge Cloud Best Scores with Local
      final cloudScores = (data['best_scores'] as Map<String, dynamic>?) ?? {};
      final mergedScores = Map<String, int>.from(localBestScores);

      for (final entry in cloudScores.entries) {
        final cloudVal = (entry.value is int)
            ? entry.value as int
            : int.tryParse(entry.value.toString()) ?? 0;
        final localVal = mergedScores[entry.key] ?? 0;
        final highest = cloudVal > localVal ? cloudVal : localVal;
        mergedScores[entry.key] = highest;
        await prefs.setInt('best_score_${entry.key}', highest);
      }

      for (final entry in mergedScores.entries) {
        await prefs.setInt('best_score_${entry.key}', entry.value);
      }

      // 3. Merge Saved In-Progress Sessions
      final cloudSaved = (data['saved_sessions'] as Map<String, dynamic>?) ?? {};
      final mergedSaved = Map<String, String>.from(localSavedSessions);
      for (final entry in cloudSaved.entries) {
        final val = entry.value?.toString();
        if (val != null && val.isNotEmpty) {
          if (!mergedSaved.containsKey(entry.key)) {
            await prefs.setString('saved_session_${entry.key}', val);
            mergedSaved[entry.key] = val;
          }
        }
      }

      // 4. Merge Completed Review Sessions
      final cloudCompleted =
          (data['completed_sessions'] as Map<String, dynamic>?) ?? {};
      final mergedCompleted = Map<String, String>.from(localCompletedSessions);
      for (final entry in cloudCompleted.entries) {
        final val = entry.value?.toString();
        if (val != null && val.isNotEmpty) {
          if (!mergedCompleted.containsKey(entry.key)) {
            await prefs.setString('completed_session_${entry.key}', val);
            mergedCompleted[entry.key] = val;
          }
        }
      }

      // 5. Restore Settings
      final cloudSettings = (data['settings'] as Map<String, dynamic>?) ?? {};
      if (cloudSettings.containsKey('randomize_questions')) {
        await prefs.setBool(
            'randomize_questions', cloudSettings['randomize_questions'] == true);
      }
      if (cloudSettings.containsKey('last_quiz_mode')) {
        await prefs.setString(
            'last_quiz_mode', cloudSettings['last_quiz_mode'].toString());
      }

      // 6. Write back the unified state to Cloud
      await docRef.set({
        'profile': {
          'uid': user.uid,
          'email': user.email ?? '',
          'displayName': user.displayName ?? '',
          'photoUrl': user.photoURL ?? '',
          'lastActiveAt': FieldValue.serverTimestamp(),
        },
        'best_scores': mergedScores,
        'saved_sessions': mergedSaved,
        'completed_sessions': mergedCompleted,
        'settings': {
          'randomize_questions': prefs.getBool('randomize_questions') ?? true,
          'last_quiz_mode': prefs.getString('last_quiz_mode') ?? 'checkAtEnd',
        },
        'lastSyncedAt': FieldValue.serverTimestamp(),
      }, SetOptions(merge: true)).timeout(const Duration(seconds: 5));

      lastSyncedTime = DateTime.now();
      syncNotifier.value++;

      if (kDebugMode) {
        print('Cloud Sync completed successfully for ${user.email}');
      }
    } catch (e) {
      if (kDebugMode) {
        print('Cloud Sync skipped or encountered error (safe fallback): $e');
      }
    }
  }

  /// Cloud save for best score
  static Future<void> syncBestScore(String subjectId, int sectionId, int score) async {
    final docRef = _userDoc;
    if (docRef == null) return;
    try {
      final key = '${subjectId}_sec_$sectionId';
      await docRef.set({
        'best_scores': {key: score},
        'lastSyncedAt': FieldValue.serverTimestamp(),
      }, SetOptions(merge: true)).timeout(const Duration(seconds: 3));
    } catch (e) {
      if (kDebugMode) print('Cloud sync best score error: $e');
    }
  }

  /// Cloud save for in-progress session
  static Future<void> syncSessionProgress(
      String subjectId, int sectionId, Map<String, dynamic> sessionData) async {
    final docRef = _userDoc;
    if (docRef == null) return;
    try {
      final key = '${subjectId}_sec_$sectionId';
      await docRef.set({
        'saved_sessions': {key: jsonEncode(sessionData)},
        'lastSyncedAt': FieldValue.serverTimestamp(),
      }, SetOptions(merge: true)).timeout(const Duration(seconds: 3));
    } catch (e) {
      if (kDebugMode) print('Cloud sync session error: $e');
    }
  }

  /// Cloud remove for saved session
  static Future<void> syncClearSavedProgress(
      String subjectId, int sectionId) async {
    final docRef = _userDoc;
    if (docRef == null) return;
    try {
      final key = '${subjectId}_sec_$sectionId';
      await docRef.update({
        'saved_sessions.$key': FieldValue.delete(),
        'lastSyncedAt': FieldValue.serverTimestamp(),
      }).timeout(const Duration(seconds: 3));
    } catch (e) {
      if (kDebugMode) print('Cloud clear session error: $e');
    }
  }

  /// Cloud save for completed session
  static Future<void> syncCompletedSession(
      String subjectId, int sectionId, Map<String, dynamic> sessionData) async {
    final docRef = _userDoc;
    if (docRef == null) return;
    try {
      final key = '${subjectId}_sec_$sectionId';
      await docRef.set({
        'completed_sessions': {key: jsonEncode(sessionData)},
        'lastSyncedAt': FieldValue.serverTimestamp(),
      }, SetOptions(merge: true)).timeout(const Duration(seconds: 3));
    } catch (e) {
      if (kDebugMode) print('Cloud sync completed session error: $e');
    }
  }

  /// Cloud remove for completed session
  static Future<void> syncClearCompletedSession(
      String subjectId, int sectionId) async {
    final docRef = _userDoc;
    if (docRef == null) return;
    try {
      final key = '${subjectId}_sec_$sectionId';
      await docRef.update({
        'completed_sessions.$key': FieldValue.delete(),
        'lastSyncedAt': FieldValue.serverTimestamp(),
      }).timeout(const Duration(seconds: 3));
    } catch (e) {
      if (kDebugMode) print('Cloud clear completed session error: $e');
    }
  }

  /// Cloud save for settings
  static Future<void> syncSettings(
      {bool? randomize, String? lastQuizMode}) async {
    final docRef = _userDoc;
    if (docRef == null) return;
    try {
      final Map<String, dynamic> settingsUpdate = {};
      if (randomize != null) settingsUpdate['randomize_questions'] = randomize;
      if (lastQuizMode != null) settingsUpdate['last_quiz_mode'] = lastQuizMode;

      if (settingsUpdate.isNotEmpty) {
        await docRef.set({
          'settings': settingsUpdate,
          'lastSyncedAt': FieldValue.serverTimestamp(),
        }, SetOptions(merge: true)).timeout(const Duration(seconds: 3));
      }
    } catch (e) {
      if (kDebugMode) print('Cloud sync settings error: $e');
    }
  }
}
