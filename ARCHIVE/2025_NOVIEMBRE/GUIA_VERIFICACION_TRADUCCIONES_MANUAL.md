# 🌍 Guía de Verificación Manual de Traducciones

## 📊 Estado Actual de Archivos

| Idioma | Archivo | Keys | Tamaño | Última Modificación |
|--------|---------|------|--------|---------------------|
| 🇬🇧 Inglés | `app_en.arb` | **1998** | 116 KB | Nov 13 22:30 |
| 🇪🇸 Español | `app_es.arb` | **1829** | 106 KB | Nov 13 22:27 |
| 🇩🇪 Alemán | `app_de.arb` | **1755** | 102 KB | Nov 13 22:31 |
| 🇫🇷 Francés | `app_fr.arb` | **1700** | 100 KB | Nov 13 22:31 |
| 🇮🇹 Italiano | `app_it.arb` | **2072** | 118 KB | Nov 13 22:31 |
| 🇵🇹 Portugués | `app_pt.arb` | **2019** | 117 KB | Nov 13 22:31 |

### ⚠️ Observaciones:

**Inconsistencias en número de keys:**
- 🇬🇧 EN: 1998 (base)
- 🇮🇹 IT: 2072 (+74 keys más que EN) ⚠️
- 🇵🇹 PT: 2019 (+21 keys más que EN) ⚠️
- 🇪🇸 ES: 1829 (-169 keys menos) ⚠️
- 🇩🇪 DE: 1755 (-243 keys menos) ⚠️
- 🇫🇷 FR: 1700 (-298 keys menos) ⚠️

**Posibles causas:**
- Italiano y Portugués tienen keys extras (duplicados o metadata)
- Español, Alemán y Francés les faltan traducciones

---

## 🧪 Cómo Verificar Manualmente en la App

### **1. Cambiar Idioma en la App**

```
1. Abre la app
2. Ve a Settings/Ajustes
3. Cambia el idioma a cada uno:
   - Español
   - English
   - Deutsch
   - Français
   - Italiano
   - Português
```

---

### **2. Verificar Pantallas Principales**

Para **CADA idioma**, revisa estas pantallas:

#### **A) Home Screen / Pantalla Principal**
- [ ] Título "Horoscope" traducido correctamente
- [ ] Botones traducidos
- [ ] Signos del zodiaco traducidos
- [ ] Tabs (Daily, Weekly, Monthly) traducidos

#### **B) Cosmic Coach**
- [ ] Título "Cosmic Coach" o equivalente
- [ ] "Tus metas" / "Your goals"
- [ ] Botón "Generar nuevas metas"
- [ ] Mensaje celebración al completar
- [ ] Categorías de metas traducidas

#### **C) Analytics Dashboard**
- [ ] Título "Analytics"
- [ ] Labels: "Coach Sessions", "Compatibility Checks"
- [ ] "Tu viaje cósmico" / "Your cosmic journey"
- [ ] Nombres de días de la semana
- [ ] Nombres de meses

#### **D) Compatibility Screen**
- [ ] Título "Compatibility"
- [ ] Signos del zodiaco
- [ ] Resultados de compatibilidad
- [ ] Descripciones

#### **E) Premium Screen**
- [ ] Título "Premium"
- [ ] Beneficios traducidos
- [ ] Precios (deberían mostrar en moneda local)
- [ ] Botones "Subscribe", "Restore"

---

### **3. Verificar Elementos Específicos**

#### **Signos del Zodiaco**

Verifica que en cada idioma aparezcan correctamente:

| Signo | ES | EN | DE | FR | IT | PT |
|-------|----|----|----|----|----|----|
| Aries | Aries | Aries | Widder | Bélier | Ariete | Áries |
| Taurus | Tauro | Taurus | Stier | Taureau | Toro | Touro |
| Gemini | Géminis | Gemini | Zwillinge | Gémeaux | Gemelli | Gêmeos |
| Cancer | Cáncer | Cancer | Krebs | Cancer | Cancro | Câncer |
| Leo | Leo | Leo | Löwe | Lion | Leone | Leão |
| Virgo | Virgo | Virgo | Jungfrau | Vierge | Vergine | Virgem |
| Libra | Libra | Libra | Waage | Balance | Bilancia | Libra |
| Scorpio | Escorpio | Scorpio | Skorpion | Scorpion | Scorpione | Escorpião |
| Sagittarius | Sagitario | Sagittarius | Schütze | Sagittaire | Sagittario | Sagitário |
| Capricorn | Capricornio | Capricorn | Steinbock | Capricorne | Capricorno | Capricórnio |
| Aquarius | Acuario | Aquarius | Wassermann | Verseau | Acquario | Aquário |
| Pisces | Piscis | Pisces | Fische | Poissons | Pesci | Peixes |

#### **Días de la Semana**

| Día | ES | EN | DE | FR | IT | PT |
|-----|----|----|----|----|----|----|
| Monday | Lunes | Monday | Montag | Lundi | Lunedì | Segunda |
| Tuesday | Martes | Tuesday | Dienstag | Mardi | Martedì | Terça |
| Wednesday | Miércoles | Wednesday | Mittwoch | Mercredi | Mercoledì | Quarta |
| Thursday | Jueves | Thursday | Donnerstag | Jeudi | Giovedì | Quinta |
| Friday | Viernes | Friday | Freitag | Vendredi | Venerdì | Sexta |
| Saturday | Sábado | Saturday | Samstag | Samedi | Sabato | Sábado |
| Sunday | Domingo | Sunday | Sonntag | Dimanche | Domenica | Domingo |

#### **Meses**

Verifica que los nombres de meses estén traducidos correctamente en:
- Analytics Dashboard
- Birth Date pickers
- Horoscope sections

---

### **4. Verificar Mensajes Específicos**

#### **Cosmic Coach - Celebración**
Al completar una meta, verifica el mensaje:
- 🇪🇸 "¡Increíble!" / "¡Bien hecho!"
- 🇬🇧 "Amazing!" / "Well done!"
- 🇩🇪 "Fantastisch!" / "Gut gemacht!"
- 🇫🇷 "Incroyable!" / "Bien joué!"
- 🇮🇹 "Incredibile!" / "Ben fatto!"
- 🇵🇹 "Incrível!" / "Muito bem!"

#### **Analytics - Labels**
- "Coach Sessions" → Sesiones de coach / Sitzungen / Sessions / Sessioni / Sessões
- "Compatibility Checks" → Compatibilidades / Kompatibilität / Compatibilité / Compatibilità / Compatibilidade

---

## 🔍 Cómo Encontrar Textos en Inglés (No Traducidos)

Si encuentras textos en inglés cuando deberían estar en otro idioma:

### **Método 1: Visual**
1. Toma screenshot
2. Anota el texto exacto que aparece en inglés
3. Busca ese texto en `app_en.arb`:
   ```bash
   grep -i "texto aquí" assets/l10n/app_en.arb
   ```

### **Método 2: Búsqueda Sistemática**

Ejecuta este comando para encontrar keys faltantes:

```bash
# Comparar EN vs ES
jq -r 'keys[]' assets/l10n/app_en.arb | sort > /tmp/en_keys.txt
jq -r 'keys[]' assets/l10n/app_es.arb | sort > /tmp/es_keys.txt
diff /tmp/en_keys.txt /tmp/es_keys.txt | grep "^<"
```

Esto mostrará las keys que están en EN pero NO en ES.

---

## 📝 Checklist de Verificación

### **Español (ES)**
- [ ] Home screen completo
- [ ] Cosmic Coach completo
- [ ] Analytics completo
- [ ] Compatibility completo
- [ ] Premium screen completo
- [ ] Signos del zodiaco
- [ ] Días y meses
- [ ] Mensajes de error/éxito

### **English (EN)**
- [ ] Home screen
- [ ] Cosmic Coach
- [ ] Analytics
- [ ] Compatibility
- [ ] Premium screen
- [ ] Zodiac signs
- [ ] Days and months
- [ ] Error/success messages

### **Deutsch (DE)**
- [ ] Startseite
- [ ] Cosmic Coach
- [ ] Analytics
- [ ] Kompatibilität
- [ ] Premium-Bildschirm
- [ ] Sternzeichen
- [ ] Tage und Monate
- [ ] Nachrichten

### **Français (FR)**
- [ ] Écran d'accueil
- [ ] Cosmic Coach
- [ ] Analytics
- [ ] Compatibilité
- [ ] Écran Premium
- [ ] Signes du zodiaque
- [ ] Jours et mois
- [ ] Messages

### **Italiano (IT)**
- [ ] Schermata principale
- [ ] Cosmic Coach
- [ ] Analytics
- [ ] Compatibilità
- [ ] Schermo Premium
- [ ] Segni zodiacali
- [ ] Giorni e mesi
- [ ] Messaggi

### **Português (PT)**
- [ ] Tela inicial
- [ ] Cosmic Coach
- [ ] Analytics
- [ ] Compatibilidade
- [ ] Tela Premium
- [ ] Signos do zodíaco
- [ ] Dias e meses
- [ ] Mensagens

---

## 🐛 Problemas Comunes a Buscar

### **1. Textos en Inglés en Otros Idiomas**
- Busca palabras como: "Goal", "Session", "Analytics", "Premium"
- Deberían estar traducidas en todos los idiomas

### **2. Placeholders Sin Reemplazar**
- Busca: `{variable}`, `%s`, `$value`
- Deben funcionar correctamente

### **3. Formatos de Número/Fecha Incorrectos**
- Fechas: DD/MM/YYYY vs MM/DD/YYYY
- Números: 1.000 vs 1,000

### **4. Género/Plural Incorrecto**
- Alemán: der/die/das
- Francés: le/la, masculine/féminine
- Italiano: il/la, masculine/femminile
- Portugués: o/a, masculine/feminino

---

## 📊 Comando para Generar Reporte de Keys Faltantes

Ejecuta este script para ver qué keys faltan en cada idioma:

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/assets/l10n

echo "=== Keys Faltantes por Idioma ==="
echo ""

# Obtener keys de EN (base)
jq -r 'keys[]' app_en.arb | sort > /tmp/en_keys.txt

for lang in es de fr it pt; do
  echo "--- $lang ---"
  jq -r 'keys[]' app_$lang.arb | sort > /tmp/${lang}_keys.txt
  missing=$(diff /tmp/en_keys.txt /tmp/${lang}_keys.txt | grep "^<" | wc -l)
  extra=$(diff /tmp/en_keys.txt /tmp/${lang}_keys.txt | grep "^>" | wc -l)
  echo "Keys faltantes: $missing"
  echo "Keys extras: $extra"
  echo ""
done
```

---

## ✅ Resultado Esperado

Después de la verificación manual, deberías tener:

1. ✅ Lista de textos en inglés encontrados en otros idiomas
2. ✅ Screenshots de problemas (si hay)
3. ✅ Lista de keys faltantes por idioma
4. ✅ Priorización de qué arreglar primero

---

## 🚀 Próximos Pasos

Una vez terminada la verificación manual:

1. Reporta cualquier texto en inglés que encuentres
2. Prioriza los más importantes (pantallas principales)
3. Podemos agregar/corregir las traducciones faltantes

---

**Nota:** Los archivos de traducción están en:
`/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/assets/l10n/`

**Última actualización:** 13 Nov 2025
