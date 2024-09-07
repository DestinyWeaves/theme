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