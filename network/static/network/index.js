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
//     })
// ', function () => ('inbox'));


function editPost(id) {
    const post = document.getElementById(`post-${id}`);
    const content = post.getElementsByClassName("content")[0];

    const textarea = document.createElement("textarea");
    textarea.value = content.innerHTML;

    const saveButton = document.createElement("button");
    saveButton.classList.add("btn", "btn-primary", "save");
    saveButton.innerHTML = "Save";
    saveButton.type = "button";

    saveButton.onclick = function () {
        fetch(`/edit/${id}`, {
            method: "PUT",
            body: JSON.stringify({
                content: textarea.value,
            })
        })
            .then(() => {
                content.innerHTML = textarea.value;
                saveButton.remove();
                textarea.remove();
            })

    }

    post.append(textarea);
    post.append(saveButton);
}


function toggleLike(button, id, likes) {
    fetch(`/like/${id}`, {
        method: "PUT",
        body: JSON.stringify({
            likes: !likes
        })
    })
        .then((response) => response.json())
        .then((result) => {
            button.innerHTML = button.getAttribute(`data-${likes ? "up" : "down"}-button`);
            button.onclick = () => toggleLike(button, id, !likes);
            document.getElementById(`post-like-count-${id}`).innerHTML = result.count;
        })
}