# 🤖 AUTO MULTI-AGENT HOOK SYSTEM

## **CONFIGURACIÓN AUTOMÁTICA**

### **Hook de Activación Automática**
```json
{
  "trigger": "user_instruction_received",
  "action": "activate_multiagent_planning",
  "agents_priority": [
    "ZODIAC_FLUTTER_EXPERT_2025.md",
    "ZODIAC_BACKEND_EXPERT_2025.md",
    "ZODIAC_BUSINESS_EXPERT_2025.md"
  ],
  "auto_planning": true,
  "context": "Zodiac Life Coach production app"
}
```

### **Workflow Automático**
1. **Usuario envía instrucción** → Sistema detecta
2. **Auto-análisis** → ¿Qué tipo de tarea es?
3. **Plan automático** → TodoWrite con pasos
4. **Agentes sugeridos** → Según tipo de tarea
5. **Ejecución coordinada** → Task tool con múltiples agentes

### **Tipos de Instrucción → Agentes Automáticos**
```
🔧 "Implementa/Agrega/Fix" → Flutter + Backend experts
💰 "Optimiza conversión/Revenue" → Business + Flutter experts
🚀 "Deploy/Launch" → Todos los agentes + deployment plan
📊 "Analiza/Revisa" → Status master + agentes específicos
🐛 "Soluciona bug" → Flutter expert + análisis
```