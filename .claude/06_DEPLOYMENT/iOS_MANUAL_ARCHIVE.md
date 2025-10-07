# 🍎 CREAR iOS ARCHIVE MANUALMENTE

## **PROBLEMA**: Flutter build ipa está fallando por configuraciones outdated

## **SOLUCIÓN**: Usar Xcode directamente para crear Archive

### **🔨 PASOS EN XCODE:**

1. **Abrir Xcode**:
   ```bash
   open ios/Runner.xcworkspace
   ```

2. **En Xcode**:
   - **Target**: Seleccionar "Any iOS Device (arm64)"
   - **Scheme**: "Runner"
   - **Configuration**: Cambiar a "Release"

3. **Product Menu**:
   - **Product** → **Clean Build Folder** (Cmd+Shift+K)
   - **Product** → **Archive** (Cmd+Shift+B)

4. **Si da error**, probar:
   - **Runner** → **Build Settings** → **Search "swift optimization"**
   - **Swift Compiler - Optimization Level** → **Optimize for Speed [-O]**

5. **Archive successful**:
   - **Organizer** se abre automáticamente
   - **Distribute App** → **iOS App Store**
   - **Export** → Guardar .ipa

### **📱 RESULTADO**: Archivo .ipa listo para App Store Connect

## **⚡ ALTERNATIVA RÁPIDA**:
Si Archive también falla, usar **TestFlight** method:
- **Distribute App** → **TestFlight**
- **Export** → Esto casi siempre funciona
- Luego usar ese .ipa para App Store