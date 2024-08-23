let UserInfo = JSON.parse(sessionStorage.getItem("user-info"));
let Usercred = JSON.parse(sessionStorage.getItem("user-creds"));
let Displayname = document.getElementById("display-name");
let SignoutBtn = document.getElementById("signoutbutton");

if (UserInfo) {
  Displayname.innerText = Usercred.user;
  console.log(Usercred.email);
}

let Signout = () => {
  sessionStorage.removeItem("user-creds");
  sessionStorage.removeItem("user-info");
  window.location.href = "/";
};

let CheckCred = () => {
  if (!sessionStorage.getItem("user-creds")) window.location.href = "/";
  else {
    Displayname.innerText = Usercred.email;
  }
};
window.addEventListener("load", CheckCred);
SignoutBtn.addEventListener("click", Signout);
