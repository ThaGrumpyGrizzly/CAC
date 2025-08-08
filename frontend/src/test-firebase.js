// Test Firebase connection
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyBDSZshpU6QdbG9dcQz_0WK8eFZjomnias",
  authDomain: "coffee-investing-app.firebaseapp.com",
  projectId: "coffee-investing-app",
  storageBucket: "coffee-investing-app.firebasestorage.app",
  messagingSenderId: "263487924561",
  appId: "1:263487924561:web:87c64b223e78238d030b70",
  measurementId: "G-7EVD2CNW05"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

console.log('✅ Firebase initialized successfully!');
console.log('🔧 Auth domain:', firebaseConfig.authDomain);
console.log('📱 Project ID:', firebaseConfig.projectId);

export { app, auth }; 