const inputs = document.querySelectorAll(".form-input");

function addfocus() {
    let parent = this.parentNode.parentNode;
    parent.classList.add("focus");
}

function remfocus() {
    let parent = this.parentNode.parentNode;
    if(this.value == ""){
        parent.classList.remove("focus");
    }
}

inputs.forEach(input => {
    input.addEventListener("focus", addfocus);
    input.addEventListener("blur", remfocus)
});



// Disable caching on AJAX requests
if ('serviceWorker' in navigator) {
navigator.serviceWorker.getRegistrations().then(function (registrations) {
    for (let registration of registrations) {
        registration.unregister(); // Unregister service workers to prevent caching
    }
});
}

// Force fresh request by adding timestamp to URL
function disableCache(url) {
    return url + (url.includes("?") ? "&" : "?") + "no_cache=" + new Date().getTime();
}
  
// Redirect to error page when offline
window.addEventListener("offline", function () {
    console.log("Network offline. Redirecting to error page...");
    window.location.href = "/Error"; // Make sure this route exists in Django
});

// Reload when online to get fresh data
window.addEventListener("online", function () {
    console.log("Network restored. Reloading...");
    location.reload(); // Reloads page to get fresh data
});
  