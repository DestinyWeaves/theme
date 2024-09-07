{
  const first_post_row = document.querySelector(".post_row");
  if (first_post_row) {
    first_post_row.previousElementSibling.remove(); // .postlinksbar
    first_post_row.previousElementSibling.remove(); // .maintitle

    const post_rows = document.querySelectorAll(".post_row");
    const last_post_row = post_rows[post_rows.length-1];
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