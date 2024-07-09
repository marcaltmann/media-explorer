import videojs from "video.js";
import "video.js/dist/video-js.css";

const READY_STATE_HAVE_CURRENT_DATA = 2;

const player = videojs('resource-media');

player.ready(function() {
    this.on('timeupdate', function() {
        const event = new CustomEvent('timeupdate', { detail: this.currentTime() });
        document.dispatchEvent(event);
    })

    document.addEventListener('timerequest', (e) => {
        this.currentTime(e.detail);

        if (this.readyState() >= READY_STATE_HAVE_CURRENT_DATA) {
            this.play();
        } else {
            this.autoplay(true);
        }
    });
});
