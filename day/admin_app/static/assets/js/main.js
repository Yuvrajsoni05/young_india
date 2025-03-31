
(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, all).forEach(e => e.addEventListener(type, listener))
    } else {
      select(el, all).addEventListener(type, listener)
    }
  }

  /**
   * Easy on scroll event listener
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }


 /**
 * Sidebar toggle (Ensures full expansion on mobile)
 */
 if (select('.toggle-sidebar-btn')) {
  on('click', '.toggle-sidebar-btn', function(e) {
    const body = select('body');
    const movieIcon = select('.movie-view-icon'); // Select your movie view icon element

    if (window.innerWidth <= 1199) {
      // Mobile View: Fully expand sidebar when clicked
      if (body.classList.contains("toggle-sidebar")) {
        body.classList.remove("toggle-sidebar"); // Collapse sidebar
        movieIcon.style.display = 'none'; // Hide movie view icon when collapsed
      } else {
        body.classList.add("toggle-sidebar"); // Expand sidebar
        movieIcon.style.display = 'block'; // Show movie view icon when expanded
      }
    } else {
      // Desktop View: Normal behavior
      body.classList.toggle("toggle-sidebar");
      // Here you can decide if you want to show or hide the icon depending on the state of the sidebar
      if (body.classList.contains("toggle-sidebar")) {
        movieIcon.style.display = 'block'; // Ensure icon is visible on desktop
      } else {
        movieIcon.style.display = 'none'; // Hide icon if sidebar is collapsed on desktop
      }
    }
  });
}


  /**
   * Search bar toggle
   */
  document.addEventListener("DOMContentLoaded", function () {
    const sidebarToggle = document.querySelector("#sidebarToggle");
    const sidebarIcon = document.querySelector("#sidebarIcon");
    const body = document.body;
  
    sidebarToggle.addEventListener("click", function () {
      body.classList.toggle("toggle-sidebar");
  
      // Change icon when sidebar is toggled
      if (body.classList.contains("toggle-sidebar")) {
        sidebarIcon.classList.replace("bi-list", "bi-x-lg"); // Change to '×' icon
      } else {
        sidebarIcon.classList.replace("bi-x-lg", "bi-list"); // Change back to menu icon
      }
    });
  });
  

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Initiate tooltips
   */
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  /**
   * Initiate quill editors
   */
  if (select('.quill-editor-default')) {
    new Quill('.quill-editor-default', {
      theme: 'snow'
    });
  }

  if (select('.quill-editor-bubble')) {
    new Quill('.quill-editor-bubble', {
      theme: 'bubble'
    });
  }

  if (select('.quill-editor-full')) {
    new Quill(".quill-editor-full", {
      modules: {
        toolbar: [
          [{
            font: []
          }, {
            size: []
          }],
          ["bold", "italic", "underline", "strike"],
          [{
              color: []
            },
            {
              background: []
            }
          ],
          [{
              script: "super"
            },
            {
              script: "sub"
            }
          ],
          [{
              list: "ordered"
            },
            {
              list: "bullet"
            },
            {
              indent: "-1"
            },
            {
              indent: "+1"
            }
          ],
          ["direction", {
            align: []
          }],
          ["link", "image", "video"],
          ["clean"]
        ]
      },
      theme: "snow"
    });
  }

  /**
   * Initiate TinyMCE Editor
   */

  /**
   * Initiate Bootstrap validation check
   */
  var needsValidation = document.querySelectorAll('.needs-validation')

  Array.prototype.slice.call(needsValidation)
    .forEach(function(form) {
      form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })

  /**
   * Initiate Datatables
   */
  const datatables = select('.datatable', true)
  datatables.forEach(datatable => {
    new simpleDatatables.DataTable(datatable, {
      perPageSelect: [5, 10, 15, ["All", -1]],
      columns: [{
          select: 2,
          sortSequence: ["desc", "asc"]
        },
        {
          select: 3,
          sortSequence: ["desc"]
        },
        {
          select: 4,
          cellClass: "green",
          headerClass: "red"
        }
      ]
    });
  })

  

})();

// // Disable caching on AJAX requests and unregister service workers
// if ('serviceWorker' in navigator) {
//   navigator.serviceWorker.getRegistrations().then(function (registrations) {
//       for (let registration of registrations) {
//           registration.unregister(); // Unregister service workers to prevent caching
//       }
//   });
// }

// // Force fresh request by adding timestamp to URL
// function disableCache(url) {
//   return url + (url.includes("?") ? "&" : "?") + "no_cache=" + new Date().getTime();
// }

// // Redirect to error page when offline
// window.addEventListener("offline", function () {
//   console.log("Network offline. Redirecting to error page...");
//   window.location.href = "/Error"; // Make sure this route exists in Django
// });

// // Reload when online to get fresh data
// window.addEventListener("online", function () {
//   console.log("Network restored. Reloading...");
//   location.reload(); // Reloads page to get fresh data
// });


// [22/Mar/2025 23:17:06,397] - Broken pipe from ('127.0.0.1', 51766)

