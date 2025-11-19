#!/bin/bash
# Check Flutter debug status

echo "=== Checking Flutter Debug Status ==="
echo ""

# Check if device is connected
echo "1. Device Connection:"
flutter devices | grep "Alejandro Caceres"
echo ""

# Check if app is running on device
echo "2. Running Apps on iPhone:"
xcrun devicectl device info apps --device 00008150-0015244A2288401C 2>/dev/null | grep -i "zodiac\|runner" | head -5
echo ""

# Check for Flutter processes
echo "3. Active Flutter Processes:"
ps aux | grep "[f]lutter run" | wc -l
echo ""

# Check device logs for Flutter
echo "4. Recent Flutter Logs (last 10 lines):"
xcrun devicectl device info logs --device 00008150-0015244A2288401C 2>&1 | grep -i "flutter\|dart\|observatory" | tail -10 || echo "No logs available"
echo ""

echo "=== Done ==="
