button_right.addEventListener("click", function(e) {

  /* set nav-div and links to vertical */
  nav.style.width = "150px";
  nav.style.height = "100vh";
  nav.style.top = "0px";
  list.style.display = "";

  /* reset top-property */
  main.style.top = "0px";

  /* set absolute main-position from left to right and delete left-property */
  nav.style.removeProperty("left");
  nav.style.right = "0px";

  /* check where main element is momentarily and set it accordingly */
  if (main.style.left == "0px" || main.style.left == "150px" || main.style.left == "") {

    main.style.left = "-150px";
  } else {

    main.style.left = "0px";
  }

});

