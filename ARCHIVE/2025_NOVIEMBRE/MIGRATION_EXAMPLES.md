# 🎯 EJEMPLOS DE MIGRACIÓN RIVERPOD - SIDE BY SIDE

Este documento muestra ejemplos lado a lado del código ANTES y DESPUÉS de la migración.

---

## 📝 EJEMPLO 1: Widget Simple con Toggle

### ❌ ANTES (setState)

```dart
import 'package:flutter/material.dart';

class ExpandableCard extends StatefulWidget {
  final String title;
  final Widget content;

  const ExpandableCard({
    super.key,
    required this.title,
    required this.content,
  });

  @override
  State<ExpandableCard> createState() => _ExpandableCardState();
}

class _ExpandableCardState extends State<ExpandableCard> {
  bool _isExpanded = false;

  void _toggleExpansion() {
    setState(() {
      _isExpanded = !_isExpanded;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Column(
        children: [
          ListTile(
            title: Text(widget.title),
            trailing: IconButton(
              icon: Icon(_isExpanded ? Icons.expand_less : Icons.expand_more),
              onPressed: _toggleExpansion,
            ),
          ),
          if (_isExpanded) widget.content,
        ],
      ),
    );
  }
}
```

### ✅ DESPUÉS (Riverpod)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Provider genérico ya existe en widget_state_providers.dart
// final expansionProvider = StateProvider.family.autoDispose<bool, String>(
//   (ref, componentId) => false,
// );

class ExpandableCard extends ConsumerWidget {
  final String title;
  final Widget content;
  final String id; // Identificador único para el provider

  const ExpandableCard({
    super.key,
    required this.title,
    required this.content,
    required this.id,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isExpanded = ref.watch(expansionProvider(id));

    return Card(
      child: Column(
        children: [
          ListTile(
            title: Text(title),
            trailing: IconButton(
              icon: Icon(isExpanded ? Icons.expand_less : Icons.expand_more),
              onPressed: () {
                ref.read(expansionProvider(id).notifier).state = !isExpanded;
              },
            ),
          ),
          if (isExpanded) content,
        ],
      ),
    );
  }
}
```

**Cambios:**
- ✅ `StatefulWidget` → `ConsumerWidget`
- ✅ `State` eliminado
- ✅ `_isExpanded` → `expansionProvider(id)`
- ✅ `setState()` → `ref.read().state =`
- ✅ Añadido parámetro `id` para múltiples instancias
- ✅ Menos código (27 → 25 líneas)

---

## 📝 EJEMPLO 2: Screen con Loading State

### ❌ ANTES (setState)

```dart
import 'package:flutter/material.dart';

class UserProfileScreen extends StatefulWidget {
  @override
  State<UserProfileScreen> createState() => _UserProfileScreenState();
}

class _UserProfileScreenState extends State<UserProfileScreen> {
  bool _isLoading = false;
  String? _errorMessage;
  Map<String, dynamic>? _userData;

  @override
  void initState() {
    super.initState();
    _loadUserData();
  }

  Future<void> _loadUserData() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final data = await fetchUserData();
      setState(() {
        _userData = data;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    if (_errorMessage != null) {
      return Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Error: $_errorMessage'),
              ElevatedButton(
                onPressed: _loadUserData,
                child: Text('Retry'),
              ),
            ],
          ),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(title: Text('Profile')),
      body: ListView(
        children: [
          Text('Name: ${_userData?['name']}'),
          Text('Email: ${_userData?['email']}'),
        ],
      ),
    );
  }
}
```

### ✅ DESPUÉS (Riverpod - Opción 1: FutureProvider)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Provider para cargar datos del usuario
final userDataProvider = FutureProvider.autoDispose<Map<String, dynamic>>((ref) async {
  return await fetchUserData();
});

class UserProfileScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userDataAsync = ref.watch(userDataProvider);

    return Scaffold(
      appBar: AppBar(title: Text('Profile')),
      body: userDataAsync.when(
        data: (userData) => ListView(
          children: [
            Text('Name: ${userData['name']}'),
            Text('Email: ${userData['email']}'),
          ],
        ),
        loading: () => Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Error: $error'),
              ElevatedButton(
                onPressed: () => ref.refresh(userDataProvider),
                child: Text('Retry'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

**Cambios:**
- ✅ `StatefulWidget` → `ConsumerWidget`
- ✅ `State` eliminado
- ✅ 3 variables de estado → 1 `FutureProvider`
- ✅ 3 `setState()` eliminados
- ✅ Manejo de estados con `.when()` más limpio
- ✅ Retry con `ref.refresh()`
- ✅ Menos código (65 → 35 líneas)

---

## 📝 EJEMPLO 3: Form con Validación

### ❌ ANTES (setState)

```dart
import 'package:flutter/material.dart';

class LoginScreen extends StatefulWidget {
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  bool _isLoading = false;
  String? _errorMessage;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _handleLogin() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      await login(_emailController.text, _passwordController.text);
      Navigator.of(context).pushReplacementNamed('/home');
    } catch (e) {
      setState(() {
        _errorMessage = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Login')),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: EdgeInsets.all(16),
          children: [
            if (_errorMessage != null)
              Card(
                color: Colors.red.shade100,
                child: Padding(
                  padding: EdgeInsets.all(8),
                  child: Text(_errorMessage!),
                ),
              ),
            TextFormField(
              controller: _emailController,
              decoration: InputDecoration(labelText: 'Email'),
              keyboardType: TextInputType.emailAddress,
              validator: (value) {
                if (value?.isEmpty ?? true) return 'Required';
                if (!value!.contains('@')) return 'Invalid email';
                return null;
              },
            ),
            TextFormField(
              controller: _passwordController,
              decoration: InputDecoration(labelText: 'Password'),
              obscureText: true,
              validator: (value) {
                if (value?.isEmpty ?? true) return 'Required';
                if (value!.length < 6) return 'Min 6 characters';
                return null;
              },
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: _isLoading ? null : _handleLogin,
              child: _isLoading
                  ? CircularProgressIndicator()
                  : Text('Login'),
            ),
          ],
        ),
      ),
    );
  }
}
```

### ✅ DESPUÉS (Riverpod)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Estado del form
class LoginFormState {
  final bool isLoading;
  final String? errorMessage;
  final String email;
  final String password;

  const LoginFormState({
    this.isLoading = false,
    this.errorMessage,
    this.email = '',
    this.password = '',
  });

  LoginFormState copyWith({
    bool? isLoading,
    String? errorMessage,
    String? email,
    String? password,
  }) {
    return LoginFormState(
      isLoading: isLoading ?? this.isLoading,
      errorMessage: errorMessage,
      email: email ?? this.email,
      password: password ?? this.password,
    );
  }
}

// Notifier
class LoginFormNotifier extends StateNotifier<LoginFormState> {
  LoginFormNotifier() : super(const LoginFormState());

  void setEmail(String email) => state = state.copyWith(email: email);
  void setPassword(String password) => state = state.copyWith(password: password);

  Future<bool> login() async {
    state = state.copyWith(isLoading: true, errorMessage: null);

    try {
      await loginUser(state.email, state.password);
      state = state.copyWith(isLoading: false);
      return true; // Success
    } catch (e) {
      state = state.copyWith(
        errorMessage: e.toString(),
        isLoading: false,
      );
      return false; // Error
    }
  }
}

// Provider
final loginFormProvider = StateNotifierProvider.autoDispose<
  LoginFormNotifier,
  LoginFormState
>((ref) => LoginFormNotifier());

// Widget
class LoginScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final formState = ref.watch(loginFormProvider);
    final formKey = GlobalKey<FormState>(); // ✅ GlobalKey permitido en Forms

    // Listen para navegación
    ref.listen<LoginFormState>(loginFormProvider, (previous, next) {
      if (previous?.isLoading == true && next.isLoading == false && next.errorMessage == null) {
        Navigator.of(context).pushReplacementNamed('/home');
      }
    });

    return Scaffold(
      appBar: AppBar(title: Text('Login')),
      body: Form(
        key: formKey,
        child: ListView(
          padding: EdgeInsets.all(16),
          children: [
            if (formState.errorMessage != null)
              Card(
                color: Colors.red.shade100,
                child: Padding(
                  padding: EdgeInsets.all(8),
                  child: Text(formState.errorMessage!),
                ),
              ),
            TextFormField(
              initialValue: formState.email,
              decoration: InputDecoration(labelText: 'Email'),
              keyboardType: TextInputType.emailAddress,
              onChanged: (value) => ref.read(loginFormProvider.notifier).setEmail(value),
              validator: (value) {
                if (value?.isEmpty ?? true) return 'Required';
                if (!value!.contains('@')) return 'Invalid email';
                return null;
              },
            ),
            TextFormField(
              initialValue: formState.password,
              decoration: InputDecoration(labelText: 'Password'),
              obscureText: true,
              onChanged: (value) => ref.read(loginFormProvider.notifier).setPassword(value),
              validator: (value) {
                if (value?.isEmpty ?? true) return 'Required';
                if (value!.length < 6) return 'Min 6 characters';
                return null;
              },
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: formState.isLoading
                  ? null
                  : () {
                      if (formKey.currentState!.validate()) {
                        ref.read(loginFormProvider.notifier).login();
                      }
                    },
              child: formState.isLoading
                  ? CircularProgressIndicator()
                  : Text('Login'),
            ),
          ],
        ),
      ),
    );
  }
}
```

**Cambios:**
- ✅ `StatefulWidget` → `ConsumerWidget`
- ✅ `State` eliminado
- ✅ Controllers eliminados (estado en provider)
- ✅ 2 `setState()` eliminados
- ✅ `GlobalKey<FormState>` se mantiene (necesario)
- ✅ Navegación con `ref.listen()`
- ✅ Estado más estructurado y testeable

---

## 📝 EJEMPLO 4: Widget con AnimationController

### ❌ ANTES (setState)

```dart
import 'package:flutter/material.dart';

class FadeInCard extends StatefulWidget {
  final Widget child;

  const FadeInCard({super.key, required this.child});

  @override
  State<FadeInCard> createState() => _FadeInCardState();
}

class _FadeInCardState extends State<FadeInCard>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;
  bool _isExpanded = false;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: Duration(milliseconds: 500),
    );
    _animation = Tween<double>(begin: 0, end: 1).animate(_controller);
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _toggleExpansion() {
    setState(() {
      _isExpanded = !_isExpanded;
    });
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _animation,
      child: Card(
        child: Column(
          children: [
            widget.child,
            if (_isExpanded) _buildExpandedContent(),
            IconButton(
              icon: Icon(_isExpanded ? Icons.expand_less : Icons.expand_more),
              onPressed: _toggleExpansion,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildExpandedContent() {
    return Container(
      padding: EdgeInsets.all(16),
      child: Text('Expanded content here'),
    );
  }
}
```

### ✅ DESPUÉS (Riverpod)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Provider para estado de expansión (usa provider genérico)
// final expansionProvider = StateProvider.family.autoDispose<bool, String>(
//   (ref, id) => false,
// );

class FadeInCard extends ConsumerStatefulWidget {
  final Widget child;
  final String id; // Identificador único

  const FadeInCard({super.key, required this.child, required this.id});

  @override
  ConsumerState<FadeInCard> createState() => _FadeInCardState();
}

class _FadeInCardState extends ConsumerState<FadeInCard>
    with SingleTickerProviderStateMixin {
  // ✅ AnimationController permanece local (necesita vsync)
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: Duration(milliseconds: 500),
    );
    _animation = Tween<double>(begin: 0, end: 1).animate(_controller);
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // ✅ Leer estado de expansión del provider
    final isExpanded = ref.watch(expansionProvider(widget.id));

    return FadeTransition(
      opacity: _animation,
      child: Card(
        child: Column(
          children: [
            widget.child,
            if (isExpanded) _buildExpandedContent(),
            IconButton(
              icon: Icon(isExpanded ? Icons.expand_less : Icons.expand_more),
              onPressed: () {
                // ✅ Actualizar provider en lugar de setState
                ref.read(expansionProvider(widget.id).notifier).state = !isExpanded;
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildExpandedContent() {
    return Container(
      padding: EdgeInsets.all(16),
      child: Text('Expanded content here'),
    );
  }
}
```

**Cambios:**
- ✅ `StatefulWidget` → `ConsumerStatefulWidget` (porque tiene AnimationController)
- ✅ `State` → `ConsumerState`
- ✅ `AnimationController` se mantiene local
- ✅ `_isExpanded` → `expansionProvider(id)`
- ✅ `setState()` → `ref.read().state =`
- ✅ Añadido parámetro `id`

---

## 📝 EJEMPLO 5: List con Pull-to-Refresh

### ❌ ANTES (setState)

```dart
import 'package:flutter/material.dart';

class ItemListScreen extends StatefulWidget {
  @override
  State<ItemListScreen> createState() => _ItemListScreenState();
}

class _ItemListScreenState extends State<ItemListScreen> {
  List<String> _items = [];
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadItems();
  }

  Future<void> _loadItems() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final items = await fetchItems();
      setState(() {
        _items = items;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString();
        _isLoading = false;
      });
    }
  }

  Future<void> _refreshItems() async {
    await _loadItems();
  }

  void _deleteItem(int index) {
    setState(() {
      _items.removeAt(index);
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading && _items.isEmpty) {
      return Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return Scaffold(
      appBar: AppBar(title: Text('Items')),
      body: RefreshIndicator(
        onRefresh: _refreshItems,
        child: _errorMessage != null
            ? Center(child: Text('Error: $_errorMessage'))
            : ListView.builder(
                itemCount: _items.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    title: Text(_items[index]),
                    trailing: IconButton(
                      icon: Icon(Icons.delete),
                      onPressed: () => _deleteItem(index),
                    ),
                  );
                },
              ),
      ),
    );
  }
}
```

### ✅ DESPUÉS (Riverpod - AsyncNotifier)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Provider con AsyncNotifier para lista
class ItemListNotifier extends AsyncNotifier<List<String>> {
  @override
  Future<List<String>> build() async {
    return await fetchItems();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() => fetchItems());
  }

  void deleteItem(int index) {
    state.whenData((items) {
      final newItems = List<String>.from(items);
      newItems.removeAt(index);
      state = AsyncData(newItems);
    });
  }
}

final itemListProvider = AsyncNotifierProvider<ItemListNotifier, List<String>>(
  () => ItemListNotifier(),
);

class ItemListScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final itemsAsync = ref.watch(itemListProvider);

    return Scaffold(
      appBar: AppBar(title: Text('Items')),
      body: RefreshIndicator(
        onRefresh: () => ref.read(itemListProvider.notifier).refresh(),
        child: itemsAsync.when(
          data: (items) => ListView.builder(
            itemCount: items.length,
            itemBuilder: (context, index) {
              return ListTile(
                title: Text(items[index]),
                trailing: IconButton(
                  icon: Icon(Icons.delete),
                  onPressed: () {
                    ref.read(itemListProvider.notifier).deleteItem(index);
                  },
                ),
              );
            },
          ),
          loading: () => Center(child: CircularProgressIndicator()),
          error: (error, stack) => Center(child: Text('Error: $error')),
        ),
      ),
    );
  }
}
```

**Cambios:**
- ✅ `StatefulWidget` → `ConsumerWidget`
- ✅ `State` eliminado
- ✅ 3 variables de estado → 1 `AsyncNotifier`
- ✅ 4 `setState()` eliminados
- ✅ Pull-to-refresh integrado
- ✅ Manejo de errores automático
- ✅ Menos código y más limpio

---

## 🎯 RESUMEN DE PATRONES

### Patrón 1: Estado Simple → StateProvider
```dart
// Antes: setState(() => _value = newValue);
// Después: ref.read(provider(id).notifier).state = newValue;
```

### Patrón 2: Estado Complejo → StateNotifierProvider
```dart
// Antes: setState(() { _var1 = ...; _var2 = ...; });
// Después: ref.read(provider.notifier).update(...);
```

### Patrón 3: Datos Async → FutureProvider o AsyncNotifierProvider
```dart
// Antes: setState + try/catch + loading/error
// Después: AsyncValue.when(data/loading/error)
```

### Patrón 4: Animaciones → ConsumerStatefulWidget
```dart
// AnimationController permanece local con vsync
// Estado NO relacionado con animación → Provider
```

### Patrón 5: Forms → ConsumerWidget + GlobalKey
```dart
// GlobalKey<FormState> permitido (necesario)
// Estado del form → StateNotifierProvider
```

---

**Tip:** Siempre empieza por el patrón más simple y solo complica si es necesario.
