import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../services/auth_service.dart';
import '../services/firestore_sync_service.dart';
import '../theme/app_theme.dart';
import 'auth_screen.dart';
import 'home_screen.dart';

class AuthWrapper extends StatefulWidget {
  const AuthWrapper({super.key});

  @override
  State<AuthWrapper> createState() => _AuthWrapperState();
}

class _AuthWrapperState extends State<AuthWrapper> {
  String? _lastSyncedUid;

  void _triggerBackgroundSync(User user) {
    if (_lastSyncedUid != user.uid) {
      _lastSyncedUid = user.uid;
      FirestoreSyncService.startRealtimeSync(user);
    }
  }

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<User?>(
      stream: AuthService.authStateChanges,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return _buildLoadingScreen('Connecting to LET Portal...');
        }

        final user = snapshot.data;

        if (user == null) {
          if (_lastSyncedUid != null) {
            _lastSyncedUid = null;
            FirestoreSyncService.stopRealtimeSync();
          }
          return const AuthScreen();
        }

        // Trigger real-time background sync for this user
        _triggerBackgroundSync(user);

        return const HomeScreen();
      },
    );
  }

  Widget _buildLoadingScreen(String statusMessage) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundNavy,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 80,
              height: 80,
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [AppTheme.accentGold, AppTheme.accentGoldLight],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                shape: BoxShape.circle,
                boxShadow: [
                  BoxShadow(
                    color: AppTheme.accentGold.withValues(alpha: 0.35),
                    blurRadius: 20,
                    offset: const Offset(0, 8),
                  ),
                ],
              ),
              child: const Center(
                child: Icon(
                  Icons.school_rounded,
                  color: AppTheme.primaryNavy,
                  size: 44,
                ),
              ),
            ),
            const SizedBox(height: 28),
            Text(
              'TOPNOTCHER YARN',
              style: GoogleFonts.outfit(
                fontSize: 22,
                fontWeight: FontWeight.w800,
                letterSpacing: 1.5,
                color: AppTheme.textWhite,
              ),
            ),
            const SizedBox(height: 18),
            const SizedBox(
              width: 28,
              height: 28,
              child: CircularProgressIndicator(
                strokeWidth: 2.5,
                color: AppTheme.accentGold,
              ),
            ),
            const SizedBox(height: 14),
            Text(
              statusMessage,
              style: GoogleFonts.inter(
                fontSize: 13,
                color: AppTheme.textMuted,
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
