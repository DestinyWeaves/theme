

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
  const old_info = table_cells[0];
  const old_controls = table_cells[1];

  // TODO: guest login box
  
  const sidebar = document.createElement("div");
  sidebar.className = "login-nav";

  const info_head = document.createElement("div");
  info_head.className = "login-nav-head";
  const user_info = old_info.querySelector("strong");
  info_head.appendChild(user_info);
  sidebar.appendChild(info_head);

  const info_list = document.createElement("ul");
  info_list.className = "login-nav-list";
  ["#log-out", "#admin-link", "#modcp-link"].forEach(query => {
    const list_link = old_info.querySelector(query);
    const list_item = document.createElement("li");
    list_item.className = "login-nav-list-item";
    list_item.appendChild(list_link);
    info_list.appendChild(list_item);
  });
  sidebar.appendChild(info_list);

  const ctrl_list = document.createElement("ul");
  ctrl_list.className = "login-nav-list";
  ["#my-controls", "#x-new-messages", "#view-new-posts", "#alerts-indicator", "#recent-alerts", "#my-friends"].forEach(query => {
    const list_link = old_info.querySelector(query);
    const list_item = document.createElement("li");
    list_item.className = "login-nav-list-item";
    list_item.appendChild(list_link);
    ctrl_list.appendChild(list_item);
  });
  sidebar.append(ctrl_list)

  div.insertAdjacentElement('beforebegin', sidebar);
  div.remove();
});

document.querySelectorAll(".jcink-reflow-googleads").forEach(div => {
  const old_adbox = div.querySelector("table#submenu + div td");
  const adbox = document.createElement("div")
  adbox.className = "googleads";
  old_adbox.childNodes.forEach(adbox.appendChild)
  div.insertAdjacentElement('beforebegin', adbox);
  div.remove();
});