document.addEventListener('DOMContentLoaded', function () {
    const messages = document.querySelector('.messages');
    if (messages) {
        console.log("Message element found");

        setTimeout(function () {
            console.log("Hiding message");
            messages.classList.add('hide');

            console.log("Current classes:", messages.classList);

            messages.addEventListener('transitionend', function () {
                console.log("Transition ended, hiding message");
                messages.style.display = 'none';
            }, {once: true});
        }, 2000);
    } else {
        console.log("No message element found");
    }
});