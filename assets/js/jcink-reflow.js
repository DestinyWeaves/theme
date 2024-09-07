

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
  const excluded = ["Home", /*"Help", "Search", "Members",*/ "Calendar", "Shoutbox",];
  div.querySelector("#submenu").querySelectorAll("a").forEach(link => {
    if (! excluded.includes(link.text)) {
      const navitem = document.createElement("li");
      navitem.className = "aux-nav-list-item";
      navitem.appendChild(link);
      link.className = "site-button";
      div.insertAdjacentElement('beforebegin', navitem);
    }
  })
  div.remove();
});

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

document.querySelectorAll(".jcink-reflow-googleads").forEach(div => {
  const old_adbox = div.querySelector("table#submenu + div td");
  const adbox = document.createElement("div")
  adbox.className = "googleads";
  old_adbox.childNodes.forEach(node => {
    adbox.appendChild(node);
  });
  div.insertAdjacentElement('beforebegin', adbox);
  div.remove();
});

{
  const first_post_row = document.querySelector(".post_row");
  if (first_post_row) {
    first_post_row.previousElementSibling.remove(); // .postlinksbar
    first_post_row.previousElementSibling.remove(); // .maintitle

    const post_rows = document.querySelectorAll(".post_row");
    const last_post_row = post_rows[post_rows.length-1];
    last_post_row.nextElementSibling.remove(); // hr
    last_post_row.nextElementSibling.remove(); // .activeuserstrip
    last_post_row.nextElementSibling.remove(); // member list
    last_post_row.nextElementSibling.remove(); // .activeuserstrip
    last_post_row.nextElementSibling.remove(); // googlead block
    // TODO: preserve this ad element for TOS reasons
    // TODO: test against paid forum -- does this element still exist?
    
    const tableborder_div = first_post_row.parentElement;
    tableborder_div.previousElementSibling.remove(); // random br
    tableborder_div.previousElementSibling.remove(); // add reply / new topic / new poll
    tableborder_div.nextElementSibling.remove(); // random br

    // do post_box first, if there's an error here we want to leave the add-reply part intact
    const post_box = document.querySelector("#qr_open");
    const form = document.querySelector("#qr_open form");
    const inner_box = document.querySelector("#qr_open div.tableborder");

    const submitbutton = document.querySelector('input[name="submit"]');
    submitbutton.remove();
    form.prepend(submitbutton);

    const textinput = document.querySelector('textarea[name="Post"]');
    textinput.remove();
    form.prepend(textinput);

    inner_box.className = "";
    inner_box.setAttribute('style', "display:none");
    post_box.id = "post_box";
    post_box.setAttribute('align', "");
    post_box.setAttribute('style', "");

    tableborder_div.nextElementSibling.remove(); // add reply / fast reply / new topic / new poll
    tableborder_div.replaceWith(...tableborder_div.childNodes); // unwrap

  };
};