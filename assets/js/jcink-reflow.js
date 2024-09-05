
document.addEventListener("DOMContentLoaded", function() {
  document.querySelectorAll(".jcink-reflow-breadcrumbs").forEach(nav => {
    const strip = nav.querySelector("#navstrip");
    const links = strip.querySelectorAll("a");
    const navlist = document.createElement("ol");
    navlist.className="breadcrumb-nav-list";
    links.forEach(link => {
      const navitem = document.createElement("li");
      navitem.className="breadcrumb-nav-list-item";
      navitem.appendChild(link);
      navlist.appendChild(navitem);
    });
    nav.replaceChildren(navlist);
  });
});
