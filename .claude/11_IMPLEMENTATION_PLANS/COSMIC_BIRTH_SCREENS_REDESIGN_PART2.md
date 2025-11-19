# 🌌 PLAN MAESTRO: REDISEÑO CÓSMICO - BIRTH & ASCENDANT SCREENS
## **PARTE 2: IMPLEMENTACIÓN TÉCNICA**

---

## 🔧 COMPONENTES A IMPLEMENTAR

### **1. CosmicDatePicker Widget**

```dart
// lib/widgets/cosmic_pickers/cosmic_date_picker.dart

import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../design_system/cosmic_colors_expanded.dart';

class CosmicDatePicker extends StatefulWidget {
  final DateTime initialDate;
  final DateTime firstDate;
  final DateTime lastDate;
  final Function(DateTime) onDateSelected;
  final bool showZodiacPreview;
  
  const CosmicDatePicker({
    super.key,
    required this.initialDate,
    required this.firstDate,
    required this.lastDate,
    required this.onDateSelected,
    this.showZodiacPreview = true,
  });

  @override
  State<CosmicDatePicker> createState() => _CosmicDatePickerState();
}

class _CosmicDatePickerState extends State<CosmicDatePicker> 
    with TickerProviderStateMixin {
  
  late DateTime _selectedDate;
  late DateTime _displayedMonth;
  late AnimationController _glowController;
  int? _hoveredDay;
  
  @override
  void initState() {
    super.initState();
    _selectedDate = widget.initialDate;
    _displayedMonth = DateTime(_selectedDate.year, _selectedDate.month);
    
    // Animación de glow pulsante
    _glowController = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    )..repeat(reverse: true);
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      height: MediaQuery.of(context).size.height * 0.75,
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            CosmicColors.deepSpace,
            CosmicColors.cosmicPurple.withOpacity(0.3),
          ],
        ),
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
      ),
      child: ClipRRect(
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 20, sigmaY: 20),
          child: Container(
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.1),
              border: Border(
                top: BorderSide(
                  width: 1,
                  color: Colors.white.withOpacity(0.2),
                ),
              ),
            ),
            child: Column(
              children: [
                _buildHandle(),
                _buildHeader(),
                _buildMonthYearSelector(),
                _buildCalendarGrid(),
                if (widget.showZodiacPreview) _buildZodiacPreview(),
                _buildActions(),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildHandle() {
    return Container(
      margin: const EdgeInsets.only(top: 12),
      width: 40,
      height: 4,
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.3),
        borderRadius: BorderRadius.circular(2),
      ),
    ).animate().fadeIn().scale();
  }

  Widget _buildHeader() {
    return Padding(
      padding: const EdgeInsets.all(20),
      child: Row(
        children: [
          Icon(
            Icons.auto_awesome,
            color: CosmicColors.cosmicGold,
            size: 28,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              'Select Your Birth Date',
              style: TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
                color: Colors.white,
                shadows: [
                  Shadow(
                    color: CosmicColors.cosmicPurple.withOpacity(0.5),
                    blurRadius: 10,
                  ),
                ],
              ),
            ),
          ),
          Icon(
            Icons.auto_awesome,
            color: CosmicColors.cosmicGold,
            size: 28,
          ),
        ],
      ).animate().fadeIn(delay: 100.ms).slideX(begin: -0.2, end: 0),
    );
  }

  Widget _buildMonthYearSelector() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          // Previous month button
          _buildNavButton(
            icon: Icons.chevron_left,
            onTap: () => _changeMonth(-1),
          ),
          
          // Month/Year display
          GestureDetector(
            onTap: _showYearPicker,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(
                  color: Colors.white.withOpacity(0.2),
                ),
              ),
              child: Text(
                _formatMonthYear(_displayedMonth),
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w600,
                  color: Colors.white,
                ),
              ),
            ).animate().scale(delay: 200.ms),
          ),
          
          // Next month button
          _buildNavButton(
            icon: Icons.chevron_right,
            onTap: () => _changeMonth(1),
          ),
        ],
      ),
    );
  }

  Widget _buildNavButton({required IconData icon, required VoidCallback onTap}) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: Colors.white.withOpacity(0.1),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: Colors.white.withOpacity(0.2),
          ),
        ),
        child: Icon(
          icon,
          color: Colors.white,
          size: 24,
        ),
      ),
    ).animate().fadeIn(delay: 200.ms);
  }

  Widget _buildCalendarGrid() {
    final daysInMonth = DateTime(
      _displayedMonth.year,
      _displayedMonth.month + 1,
      0,
    ).day;
    
    final firstDayWeekday = DateTime(
      _displayedMonth.year,
      _displayedMonth.month,
      1,
    ).weekday;

    return Expanded(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // Weekday headers
            _buildWeekdayHeaders(),
            const SizedBox(height: 12),
            
            // Days grid
            Expanded(
              child: GridView.builder(
                physics: const NeverScrollableScrollPhysics(),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 7,
                  childAspectRatio: 1,
                  crossAxisSpacing: 8,
                  mainAxisSpacing: 8,
                ),
                itemCount: 42, // 6 weeks max
                itemBuilder: (context, index) {
                  final dayNumber = index - (firstDayWeekday % 7) + 1;
                  
                  if (dayNumber < 1 || dayNumber > daysInMonth) {
                    return const SizedBox.shrink();
                  }
                  
                  final date = DateTime(
                    _displayedMonth.year,
                    _displayedMonth.month,
                    dayNumber,
                  );
                  
                  final isSelected = _isSameDay(date, _selectedDate);
                  final isToday = _isSameDay(date, DateTime.now());
                  
                  return _buildDayCell(
                    dayNumber: dayNumber,
                    date: date,
                    isSelected: isSelected,
                    isToday: isToday,
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildWeekdayHeaders() {
    const weekdays = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
    
    return Row(
      children: weekdays.map((day) => Expanded(
        child: Center(
          child: Text(
            day,
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w600,
              color: Colors.white.withOpacity(0.5),
              letterSpacing: 0.5,
            ),
          ),
        ),
      )).toList(),
    );
  }

  Widget _buildDayCell({
    required int dayNumber,
    required DateTime date,
    required bool isSelected,
    required bool isToday,
  }) {
    return MouseRegion(
      onEnter: (_) => setState(() => _hoveredDay = dayNumber),
      onExit: (_) => setState(() => _hoveredDay = null),
      child: GestureDetector(
        onTap: () => setState(() => _selectedDate = date),
        child: AnimatedBuilder(
          animation: _glowController,
          builder: (context, child) {
            final isHovered = _hoveredDay == dayNumber;
            
            return Container(
              decoration: BoxDecoration(
                color: isSelected 
                    ? CosmicColors.cosmicPurple.withOpacity(0.3)
                    : isHovered
                        ? Colors.white.withOpacity(0.1)
                        : Colors.transparent,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(
                  color: isSelected 
                      ? CosmicColors.cosmicGold.withOpacity(_glowController.value)
                      : isToday
                          ? CosmicColors.cosmicGold.withOpacity(0.3)
                          : Colors.transparent,
                  width: 2,
                ),
                boxShadow: isSelected ? [
                  BoxShadow(
                    color: CosmicColors.cosmicPurple.withOpacity(
                      0.3 * _glowController.value,
                    ),
                    blurRadius: 12,
                    spreadRadius: 2,
                  ),
                ] : null,
              ),
              child: Center(
                child: Text(
                  '$dayNumber',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                    color: isSelected 
                        ? Colors.white
                        : Colors.white.withOpacity(0.8),
                  ),
                ),
              ),
            );
          },
        ),
      ).animate(
        delay: (dayNumber * 20).ms,
      ).fadeIn().scale(begin: const Offset(0.8, 0.8)),
    );
  }

  Widget _buildZodiacPreview() {
    final zodiacSign = _getZodiacSign(_selectedDate);
    final zodiacEmoji = _getZodiacEmoji(zodiacSign);
    
    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            CosmicColors.cosmicPurple.withOpacity(0.2),
            CosmicColors.cosmicGold.withOpacity(0.1),
          ],
        ),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: CosmicColors.cosmicGold.withOpacity(0.3),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            zodiacEmoji,
            style: const TextStyle(fontSize: 32),
          ),
          const SizedBox(width: 12),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                _formatDate(_selectedDate),
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              Text(
                'Your Sun Sign: $zodiacSign',
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.white.withOpacity(0.7),
                ),
              ),
            ],
          ),
        ],
      ),
    ).animate().fadeIn(delay: 300.ms).slideY(begin: 0.2, end: 0);
  }

  Widget _buildActions() {
    return Padding(
      padding: const EdgeInsets.all(20),
      child: Row(
        children: [
          Expanded(
            child: TextButton(
              onPressed: () => Navigator.pop(context),
              style: TextButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                backgroundColor: Colors.white.withOpacity(0.1),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: const Text(
                'Cancel',
                style: TextStyle(
                  fontSize: 16,
                  color: Colors.white,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            flex: 2,
            child: ElevatedButton(
              onPressed: () => widget.onDateSelected(_selectedDate),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                backgroundColor: CosmicColors.cosmicPurple,
                foregroundColor: Colors.white,
                elevation: 0,
                shadowColor: CosmicColors.cosmicPurple.withOpacity(0.5),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  Icon(Icons.auto_awesome, size: 20),
                  SizedBox(width: 8),
                  Text(
                    'Accept',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ).animate().shimmer(delay: 400.ms, duration: 1500.ms),
          ),
        ],
      ),
    );
  }

  // Helper methods
  void _changeMonth(int delta) {
    setState(() {
      _displayedMonth = DateTime(
        _displayedMonth.year,
        _displayedMonth.month + delta,
      );
    });
  }

  void _showYearPicker() {
    // TODO: Implement year picker modal
  }

  bool _isSameDay(DateTime a, DateTime b) {
    return a.year == b.year && a.month == b.month && a.day == b.day;
  }

  String _formatMonthYear(DateTime date) {
    const months = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];
    return '${months[date.month - 1]} ${date.year}';
  }

  String _formatDate(DateTime date) {
    const weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    final weekday = weekdays[(date.weekday - 1) % 7];
    return '$weekday, ${_formatMonthYear(date).split(' ')[0]} ${date.day}, ${date.year}';
  }

  String _getZodiacSign(DateTime date) {
    // Implement zodiac sign logic (ya existe en birth_date_screen.dart)
    return 'Aries'; // Placeholder
  }

  String _getZodiacEmoji(String sign) {
    const zodiacEmojis = {
      'Aries': '♈', 'Taurus': '♉', 'Gemini': '♊',
      'Cancer': '♋', 'Leo': '♌', 'Virgo': '♍',
      'Libra': '♎', 'Scorpio': '♏', 'Sagittarius': '♐',
      'Capricorn': '♑', 'Aquarius': '♒', 'Pisces': '♓',
    };
    return zodiacEmojis[sign] ?? '⭐';
  }

  @override
  void dispose() {
    _glowController.dispose();
    super.dispose();
  }
}
```

---

**CONTINÚA EN PARTE 3 con CosmicTimePicker y CosmicPlacePicker...**
