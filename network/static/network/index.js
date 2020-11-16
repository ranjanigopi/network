/*
client:
likeButton.onclick -> call /like/<post-id> with { likeButton.getAttribute('data-like') }
                   -> get like count from response
                   -> update screen -> count
                                    -> update button text
                                    -> update data attribute (btn.setAttribute('', 'yes or no') )

server:
like/<post-id> -> see if user is logged in
               if yes - remove record
               else add record
               -> add/remove like record
               -> respond {
                  likeCount: Number
               }
 */
// function
//
//     document.querySelectorAll('.like').forEach(button => {
//         button.addEventListener('click', )
    })
// ', function () => ('inbox'));
