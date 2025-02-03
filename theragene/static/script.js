document.addEventListener("DOMContentLoaded", function() {
    console.log("TheraGene.ai website is loaded!");

    var modal = document.getElementById("loginModal");
    var btn = document.getElementById("loginBtn");
    var span = document.getElementsByClassName("close")[0];

    btn.onclick = function() {
        modal.style.display = "block";
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    document.getElementById("loginForm").addEventListener("submit", function(event) {
        event.preventDefault();
        // Add your login logic here
        alert("Logged in successfully!");
        modal.style.display = "none";
    });
});


// cntactjs

document.addEventListener("DOMContentLoaded", function() {
    console.log("TheraGene.ai website is loaded!");

    var modal = document.getElementById("loginModal");
    var btn = document.getElementById("loginBtn");
    var span = document.getElementsByClassName("close")[0];

    btn.onclick = function() {
        modal.style.display = "block";
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    document.getElementById("loginForm").addEventListener("submit", function(event) {
        event.preventDefault();
        alert("Logged in successfully!");
        modal.style.display = "none";
    });

    document.getElementById("inquiryForm").addEventListener("submit", function(event) {
        event.preventDefault();
        alert("Your inquiry has been submitted. Thank you!");
        // Add your form submission logic here
    });
});
