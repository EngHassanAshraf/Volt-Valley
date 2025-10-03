
const navSidebar = document.querySelector(".nav-sidebar");
const openNavSidebarButton = document.querySelector(".open-navsidebar");
const closeNavSidebarButton = document.querySelector(".close-navsidebar");

openNavSidebarButton.addEventListener("click", function () {
    navSidebar.style.display = "block";
});

closeNavSidebarButton.addEventListener("click", function () {
    navSidebar.style.display = "none";
});
