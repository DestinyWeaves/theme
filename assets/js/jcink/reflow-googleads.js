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