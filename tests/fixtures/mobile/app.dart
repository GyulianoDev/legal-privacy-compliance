FirebaseAuth.instance.signInWithEmailAndPassword(email: email, password: password);
FirebaseMessaging.instance.requestPermission();
FirebaseFirestore.instance.collection("profiles");
