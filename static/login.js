import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.1/firebase-app.js";
import {
  getDatabase,
  get,
  ref,
  child,
} from "https://www.gstatic.com/firebasejs/10.12.1/firebase-database.js";
import {
  getAuth,
  signInWithEmailAndPassword,
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
const dbref = ref(db);

// login
let email = document.getElementById("email");
let password = document.getElementById("password");
let signin = document.getElementById("signin");

let SignInUser = (evt) => {
  evt.preventDefault();

  signInWithEmailAndPassword(auth, email.value, password.value)
    .then((credentials) => {
      /* console.log(credentials) */
      get(child(dbref, "UsersAuthList/" + credentials.user.uid)).then(
        (snapshot) => {
          if (snapshot.exists) {
            /*  sessionStorage.setItem(
              "user-info",
              JSON.stringify({
                name: snapshot.val().name,
              })
            ); */
            sessionStorage.setItem(
              "user-creds",
              JSON.stringify(credentials.user)
            );
            window.location.href = "/home";
          }
        }
      );
    })
    .catch((error) => {
      alert(error.message);
      console.log(error.code);
      console.log(error.message);
    });
};

signin.addEventListener("submit", SignInUser);
