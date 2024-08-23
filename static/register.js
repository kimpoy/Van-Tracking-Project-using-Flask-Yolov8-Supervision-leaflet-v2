import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.1/firebase-app.js";
import {
  getDatabase,
  set,
  ref,
} from "https://www.gstatic.com/firebasejs/10.12.1/firebase-database.js";
import {
  getAuth,
  createUserWithEmailAndPassword,
} from "https://www.gstatic.com/firebasejs/10.12.1/firebase-auth.js";

import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.12.1/firebase-analytics.js";
const firebaseConfig = {
  apiKey: "AIzaSyCIJ4zoK93DWzqs_5oT553kKPzRrHcYiNY",
  authDomain: "iot-project-6b313.firebaseapp.com",
  databaseURL: "https://iot-project-6b313-default-rtdb.firebaseio.com",
  projectId: "iot-project-6b313",
  storageBucket: "iot-project-6b313.appspot.com",
  messagingSenderId: "495598691791",
  appId: "1:495598691791:web:63ea03368d69cdb7029eba",
  measurementId: "G-HGKZL3R7DW",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const db = getDatabase();
const auth = getAuth(app);

// register
let rname = document.getElementById("name");
let remail = document.getElementById("remail");
let rpassword = document.getElementById("rpassword");
let signup = document.getElementById("signup");

let RegisterUser = (evt) => {
  evt.preventDefault();
  createUserWithEmailAndPassword(auth, remail.value, rpassword.value)
    .then((credentials) => {
      console.log(credentials);
      set(ref(db, "UsersAuthList/" + credentials.user.uid), {
        name: rname.value,
      });
      window.location.href = "/";
    })
    .catch((error) => {
      alert(error.message);
      console.log(error.code);
      console.log(error.message);
    });
};

signup.addEventListener("submit", RegisterUser);
