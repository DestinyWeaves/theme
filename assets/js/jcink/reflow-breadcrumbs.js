document.querySelectorAll(".jcink-reflow-breadcrumbs").forEach(nav => {
  const navlist = document.createElement("ol");
  navlist.className = "breadcrumb-nav-list";
  nav.querySelector("#navstrip").querySelectorAll("a").forEach(link => {
    const navitem = document.createElement("li");
    navitem.className = "breadcrumb-nav-list-item";
    navitem.appendChild(link);
    navlist.appendChild(navitem);
  });
  nav.replaceChildren(navlist);
});