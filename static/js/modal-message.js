
// Comments function
document.addEventListener("DOMContentLoaded", function() {
    const sendBtn = document.getElementById('send-comment');

    sendBtn.addEventListener('click', function() {
        const text = document.getElementById('comment-text').value;
        const newsId = document.getElementById('new-id').value;

        fetch(`/news/${newsId}/add_comment/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                news_id: newsId,
                text: text
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "ok") {
                const commentsBlock = document.getElementById('comments');
                const newCommentElement = document.createElement('p');
                newCommentElement.innerHTML = `<strong>${data.username}</strong> (${data.created_at}): ${data.text}`;
                commentsBlock.prepend(newCommentElement);

                document.getElementById('comment-text').value = '';
                const modal = bootstrap.Modal.getInstance(document.getElementById("exampleModal"));
                modal.hide();
            } else{
                alert("Error: " + data.message);
            }
        });
    });
});