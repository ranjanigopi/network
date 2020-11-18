function editPost(id) {
    const post = document.getElementById(`post-${id}`);
    const content = post.getElementsByClassName("content")[0];

    content.style.display = "none";

    const textarea = document.createElement("textarea");
    textarea.value = content.innerHTML;
    textarea.classList.add("form-control", "edit-post");

    const saveButton = document.createElement("button");
    saveButton.classList.add("btn", "btn-primary", "save");
    saveButton.innerHTML = "Save";
    saveButton.type = "button";

    const cancelButton = document.createElement("button");
    cancelButton.classList.add("btn", "btn-link", "cancel");
    cancelButton.innerHTML = "Cancel";
    cancelButton.type = "button";

    const editContent = document.createElement("div");
    editContent.classList.add("edit-content");
    editContent.append(textarea);
    editContent.append(saveButton);
    editContent.append(cancelButton);

    saveButton.onclick = function () {
        fetch(`/edit/${id}`, {
            method: "PUT",
            body: JSON.stringify({
                content: textarea.value,
            })
        })
            .then(() => {
                content.innerHTML = textarea.value;
                content.style.display = "block";
                editContent.remove();
            })

    };
    cancelButton.onclick = function () {
        content.style.display = "block";
        editContent.remove();
    };

    post.append(editContent);
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