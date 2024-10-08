document.querySelectorAll(".jcink-reflow-user-sidebar").forEach(div => {
  const table_cells = div.querySelector("#userlinks").querySelectorAll("td");
  const old_info = table_cells[0];
  const old_ctrl = table_cells[1];

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
  // sidebar.appendChild(info_list);

  // const ctrl_list = document.createElement("ul");
  const ctrl_list = info_list;
  ctrl_list.className = "login-nav-list";
  [["#my-controls","Controls"],["#view-new-posts","New Posts"],["#my-friends","Friends"]].forEach(x => {
    const [query,label] = x;
    const list_link = old_ctrl.querySelector(query);
    list_link.textContent = label;
    const list_item = document.createElement("li");
    list_item.className = "login-nav-list-item";
    list_item.appendChild(list_link);
    ctrl_list.appendChild(list_item);
  });
  // sidebar.append(ctrl_list)

  // const alrt_list = document.createElement("ul");
  const alrt_list = info_list;
  alrt_list.className = "login-nav-list";
  ["#x-new-messages","#alerts-indicator",/*"#recent-alerts",*/].forEach(query => {
    const list_link = old_ctrl.querySelector(query);
    const list_item = document.createElement("li");
    list_item.className = "login-nav-list-item";
    list_item.appendChild(list_link);
    alrt_list.appendChild(list_item);
  });
  sidebar.append(alrt_list)

  div.insertAdjacentElement('beforebegin', sidebar);
  div.remove();
});