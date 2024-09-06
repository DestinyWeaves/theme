

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

document.querySelectorAll(".jcink-reflow-user-sidebar").forEach(div => {
  const table_cells = div.querySelector("#userlinks").querySelectorAll("td");
  const login_info = table_cells[0];
  const controls = table_cells[1];

  // TODO: how does the login info look when a user is logged out?
  const new_login_info = document.createElement("dl");
  new_login_info.appendChild(document.createElement("dt").appendChild(login_info.querySelector("strong")));
  new_login_info.appendChild(document.createElement("dl").appendChild(login_info.querySelector("#log-out")));
  new_login_info.appendChild(document.createElement("dl").appendChild(login_info.querySelector("#admin-link")));
  new_login_info.appendChild(document.createElement("dl").appendChild(login_info.querySelector("#modcp-link")));
  div.insertAdjacentElement('beforebegin', new_login_info);
  login_info.remove();

});
