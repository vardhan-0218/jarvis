// main.js (Consolidated and Fixed)
$(document).ready(function () {

    // Initialize eel
    eel.init()();

    // ----------------------------------------------------
    // CRITICAL UI CONTROL FUNCTIONS
    // ----------------------------------------------------

    // CRITICAL: 1. Function to switch from SiriWave back to the main Oval interface
    eel.expose(ShowHood);
    function ShowHood() {
        $("#SiriWave").attr("hidden", true);
        $("#Oval").removeAttr("hidden");
    }

    // Show Welcome Animation
    eel.expose(showWelcomeAnimation);
    function showWelcomeAnimation() {
        $("#WelcomeAnimation").attr("hidden", false);
        $("#HelloGreet").attr("hidden", true);
        $("#SystemReady").attr("hidden", true);
    }

    // Show System Ready Animation
    eel.expose(showSystemReady);
    function showSystemReady() {
        $("#WelcomeAnimation").attr("hidden", true);
        $("#SystemReady").attr("hidden", false);
        $("#HelloGreet").attr("hidden", true);
    }

    // Hide Welcome Animations
    eel.expose(hideWelcomeAnimations);
    function hideWelcomeAnimations() {
        $("#WelcomeAnimation").attr("hidden", true);
        $("#SystemReady").attr("hidden", true);
    }

    // CRITICAL: 2. Function to hide the initial loader (#Start) and show the main interface (#Oval)
    eel.expose(show_main_ui);
    function show_main_ui() {
        $("#Start").attr("hidden", true);
        $("#Oval").removeAttr("hidden");
        // Remove the hardcoded text in SiriWave section (used for testing)
        $(".siri-message").text(""); 
    }
    
    // 3. Log user's message to the chat offcanvas
    eel.expose(senderText); 
    function senderText(text) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (text.trim() !== "") {
            // Using the structure from controller.js which matches your CSS
            chatBox.innerHTML += `<div class="row justify-content-end mb-4">
                <div class = "width-size">
                    <div class="sender_message">${text}</div>
                </div>
            </div>`; 
            // Scroll to the bottom of the chat
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // 4. Log assistant's response to the chat offcanvas
    eel.expose(receiverText); 
    function receiverText(text) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (text.trim() !== "") {
            // Using the structure from controller.js which matches your CSS
            chatBox.innerHTML += `<div class="row justify-content-start mb-4">
                <div class = "width-size">
                    <div class="receiver_message">${text}</div>
                </div>
            </div>`; 
            // Scroll to the bottom of the chat
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // 5. Temporary message in the main screen (Listening..., Recognizing...)
    eel.expose(DisplayMessage); 
    function DisplayMessage(text) {
        $("#WishMessage").text(text);
        $('.siri-message').textillate('stop');
        $('.siri-message').textillate('start');
    }
    
    // 6. Face Authentication Functions (from original controller.js)
    eel.expose(hideLoader);
    function hideLoader() {
        $("#Loader").attr("hidden", true);
        $("#FaceAuth").attr("hidden", false);
    }
    eel.expose(hideFaceAuth);
    function hideFaceAuth() {
        $("#FaceAuth").attr("hidden", true);
        $("#FaceAuthSuccess").attr("hidden", false);
    }
    eel.expose(hideFaceAuthSuccess);
    function hideFaceAuthSuccess() {
        $("#FaceAuthSuccess").attr("hidden", true);
        $("#HelloGreet").removeAttr("hidden"); // Assume HelloGreet is meant to be shown
    }


    // ----------------------------------------------------
    // CORE LOGIC & ANIMATIONS
    // ----------------------------------------------------

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

    // Function to send message to assistant
    function PlayAssistant(message) {
        if (message.trim() !== "") {
            startSiriWave();
            eel.allCommands(message)(); 
            $("#chatbox").val("");
            $("#MicBtn").removeAttr('hidden');
            $("#SendBtn").attr('hidden', true);
        }
    }

    // Toggle mic/send button
    function ShowHideButton(message) {
        if (message.trim().length === 0) {
            $("#MicBtn").removeAttr('hidden');
            $("#SendBtn").attr('hidden', true);
        } else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").removeAttr('hidden');
        }
    }

    // Mic button click
    $("#MicBtn").click(function () { 
        eel.playAssistantSound(); // CRITICAL: This must match the Python exposed name!
        startSiriWave();
        eel.allCommands()(); 
    });

    // Keyup for Cmd + J (Mac) or Ctrl + J (Windows/Linux)
    function doc_keyUp(e) {
        if (e.key === 'j' && (e.metaKey || e.ctrlKey)) {
            eel.playAssistantSound();
            startSiriWave();
            eel.allCommands()();
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    // Chatbox keyup to toggle buttons
    $("#chatbox").keyup(function () {
        let message = $("#chatbox").val();
        ShowHideButton(message);
    });

    // Send button click
    $("#SendBtn").click(function () {
        let message = $("#chatbox").val();
        PlayAssistant(message);
    });

    // Enter key in chatbox
    $("#chatbox").keypress(function (e) {
        if (e.which === 13) {
            let message = $("#chatbox").val();
            PlayAssistant(message);
        }
    });

    // ----------------------------------------------------
    // SETTINGS FUNCTIONALITY
    // ----------------------------------------------------

    // Settings button click
    $("#SettingsBtn").click(function () {
        $("#settingsModal").modal('show');
        loadSettings();
    });

    // Range input updates
    $("#speechRate").on('input', function() {
        $("#speechRateValue").text($(this).val());
    });

    $("#voiceVolume").on('input', function() {
        $("#voiceVolumeValue").text($(this).val());
    });

    $("#hotwordSensitivity").on('input', function() {
        $("#hotwordSensitivityValue").text($(this).val());
    });

    // Save settings
    $("#saveSettings").click(function() {
        saveSettings();
        $("#settingsModal").modal('hide');
        showNotification("Settings saved successfully!", "success");
    });

    // Reset settings
    $("#resetSettings").click(function() {
        if (confirm("Are you sure you want to reset all settings to default?")) {
            resetSettings();
            showNotification("Settings reset to default!", "info");
        }
    });

    // Settings functions
    function loadSettings() {
        // Load settings from localStorage or use defaults
        const settings = getSettings();
        
        $("#voiceGender").val(settings.voiceGender);
        $("#speechRate").val(settings.speechRate);
        $("#speechRateValue").text(settings.speechRate);
        $("#voiceVolume").val(settings.voiceVolume);
        $("#voiceVolumeValue").text(settings.voiceVolume);
        $("#enableTTS").prop('checked', settings.enableTTS);
        $("#aiModel").val(settings.aiModel);
        $("#responseLength").val(settings.responseLength);
        $("#enableAnimations").prop('checked', settings.enableAnimations);
        $("#enableSounds").prop('checked', settings.enableSounds);
        $("#theme").val(settings.theme);
        $("#enableHotword").prop('checked', settings.enableHotword);
        $("#hotwordSensitivity").val(settings.hotwordSensitivity);
        $("#hotwordSensitivityValue").text(settings.hotwordSensitivity);
    }

    function saveSettings() {
        const settings = {
            voiceGender: $("#voiceGender").val(),
            speechRate: parseInt($("#speechRate").val()),
            voiceVolume: parseInt($("#voiceVolume").val()),
            enableTTS: $("#enableTTS").is(':checked'),
            aiModel: $("#aiModel").val(),
            responseLength: $("#responseLength").val(),
            enableAnimations: $("#enableAnimations").is(':checked'),
            enableSounds: $("#enableSounds").is(':checked'),
            theme: $("#theme").val(),
            enableHotword: $("#enableHotword").is(':checked'),
            hotwordSensitivity: parseFloat($("#hotwordSensitivity").val())
        };

        localStorage.setItem('jarvisSettings', JSON.stringify(settings));
        
        // Apply settings immediately
        applySettings(settings);
        
        // Send settings to backend
        eel.updateSettings(settings)();
    }

    function getSettings() {
        const defaultSettings = {
            voiceGender: 'female',
            speechRate: 174,
            voiceVolume: 90,
            enableTTS: true,
            aiModel: 'gemini-1.5-pro',
            responseLength: 'medium',
            enableAnimations: true,
            enableSounds: true,
            theme: 'default',
            enableHotword: true,
            hotwordSensitivity: 0.5
        };

        const saved = localStorage.getItem('jarvisSettings');
        return saved ? {...defaultSettings, ...JSON.parse(saved)} : defaultSettings;
    }

    function resetSettings() {
        localStorage.removeItem('jarvisSettings');
        loadSettings();
        const settings = getSettings();
        applySettings(settings);
        eel.updateSettings(settings)();
    }

    function applySettings(settings) {
        // Apply theme
        if (settings.theme === 'dark') {
            document.body.classList.add('dark-theme');
            document.body.classList.remove('light-theme');
        } else if (settings.theme === 'light') {
            document.body.classList.add('light-theme');
            document.body.classList.remove('dark-theme');
        } else {
            document.body.classList.remove('dark-theme', 'light-theme');
        }

        // Apply animations
        if (!settings.enableAnimations) {
            document.body.classList.add('no-animations');
        } else {
            document.body.classList.remove('no-animations');
        }
    }

    function showNotification(message, type = 'info') {
        // Create notification element
        const notification = $(`
            <div class="alert alert-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'info'} alert-dismissible fade show position-fixed" 
                 style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `);
        
        $('body').append(notification);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.alert('close');
        }, 3000);
    }

    // Load settings on page load
    $(document).ready(function() {
        const settings = getSettings();
        applySettings(settings);
    });

});