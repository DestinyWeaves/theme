

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

document.querySelectorAll(".jcink-reflow-aux-nav").forEach(div => {
  div.querySelector("#submenu").querySelectorAll("a").forEach(link => {
    const navitem = document.createElement("li");
    navitem.className = "aux-nav-list-item";
    navitem.appendChild(link);
    link.className = "site-button";
    div.insertAdjacentElement('beforebegin', navitem);
  })
  div.remove();
});

document.querySelectorAll(".jcink-reflow-user-sidebar").forEach(div => {
  const table_cells = div.querySelector("#userlinks").querySelectorAll("td");
  const linfo = table_cells[0];
  const controls = table_cells[1];

  // TODO: how does the login info look when a user is logged out?
  
  const ninfo = document.createElement("div");
  ninfo.className = "login-nav";
  const ninfo_head = document.createElement("div");
  ninfo_head.className = "login-nav-head";
  ninfo.appendChild(ninfo_head);
  const ninfo_list = document.createElement("ul");
  ninfo_list.className = "login-nav-list";
  for (let query in ["#log-out", "#admin-link", "#modcp-link"]) {
    const list_link = linfo.querySelector(query);
    const list_item = document.createElement("li");
    list_item.className = "login-nav-list-item";
    ninfo_list.appendChild(list_item);
  }
  div.insertAdjacentElement('beforebegin', ninfo);
  // div.remove();
});
