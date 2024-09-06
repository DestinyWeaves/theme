

document.querySelectorAll(".jcink-reflow-breadcrumbs").forEach(nav => {
  const navlist = document.createElement("ol");
  navlist.className="breadcrumb-nav-list";
  nav.querySelector("#navstrip").querySelectorAll("a").forEach(link => {
    const navitem = document.createElement("li");
    navitem.className="breadcrumb-nav-list-item";
    navitem.appendChild(link);
    navlist.appendChild(navitem);
  });
  nav.replaceChildren(navlist);
});

document.querySelectorAll(".jcink-reflow-aux-nav").forEach(div => {
  div.querySelector("#submenu").querySelectorAll("a").forEach(link => {
    const navitem = document.createElement("li");
    navitem.className="aux-nav-list-item";
    navitem.appendChild(link);
    link.className="site-button";
    div.insertAdjacentElement('beforebegin', navitem);
  })
  div.remove();
});