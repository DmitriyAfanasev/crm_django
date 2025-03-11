document.addEventListener("DOMContentLoaded", function () {
    const channelSelect = document.getElementById("id_channel");
    const descriptionDiv = document.getElementById("channel-description");
    const descriptionText = document.getElementById("description-text");

    channelSelect.addEventListener("change", function () {
        const selectedChannelId = this.value;
        const description = channelDescriptions[selectedChannelId];

        if (description) {
            descriptionText.textContent = description;
            descriptionDiv.style.display = "block";
        } else {
            descriptionDiv.style.display = "none";
        }
    });
});
