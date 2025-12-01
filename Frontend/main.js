$(document).ready(function () {

    // Note: eel.init() is called in controller.js to avoid duplicate initialization

    // Text animation
    $('.text').textillate({
        loop: true,
        sync: true,
        in: { effect: "bounceIn" },
        out: { effect: "bounceOut" },
    });

    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: { effect: "fadeInUp", sync: true },
        out: { effect: "fadeOutUp", sync: true },
    });

    // SiriWave instance variable
    let siriWaveInstance;

    function startSiriWave() {
        $("#Oval").attr("hidden", true);
        $("#SiriWave").removeAttr("hidden");

        if (!siriWaveInstance) {
            siriWaveInstance = new SiriWave({
                container: document.getElementById("siri-container"),
                width: 800,
                height: 200,
                style: "ios9",
                amplitude: 1,
                speed: 0.3,
                autostart: true
            });
            siriWaveInstance.start();
        }
    }

    // Note: All interactive functions (PlayAssistant, event handlers, etc.) 
    // are implemented in controller.js to avoid duplicate processing

});
