// Chatbot UI logic
$(document).ready(function() {
    // Show chatbot window
    $('#chatbot-btn').click(function() {
        $('#chatbot-window').fadeIn();
        $('#chatbot-text').focus();
    });
    // Hide chatbot window
    $('#chatbot-close').click(function() {
        $('#chatbot-window').fadeOut();
    });
    // Send message
    $('#chatbot-send').click(function() {
        sendChatbotMessage();
    });
    $('#chatbot-text').keypress(function(e) {
        if (e.which === 13 && !e.shiftKey) {
            e.preventDefault();
            sendChatbotMessage();
        }
    });
    function sendChatbotMessage() {
        var msg = $('#chatbot-text').val().trim();
        if (!msg) return;
        $('#chatbot-body').append('<div class="chatbot-message chatbot-user">'+msg+'</div>');
        $('#chatbot-text').val('');
        $('#chatbot-body').scrollTop($('#chatbot-body')[0].scrollHeight);
        // Placeholder: Simulate bot reply
        setTimeout(function() {
            var reply = getChatbotReply(msg);
            $('#chatbot-body').append('<div class="chatbot-message chatbot-bot">'+reply+'</div>');
            $('#chatbot-body').scrollTop($('#chatbot-body')[0].scrollHeight);
        }, 700);
    }
    function getChatbotReply(msg) {
        // Simple FAQ/AI placeholder
        msg = msg.toLowerCase();
        if (msg.includes('career')) return 'I can help you explore career options. What are your skills or interests?';
        if (msg.includes('skills')) return 'Tell me about your skills and I will recommend suitable jobs.';
        if (msg.includes('salary')) return 'Salary information varies by role and location. Ask about a specific job.';
        if (msg.includes('resume')) return 'I can analyze your resume and suggest improvements.';
        if (msg.includes('job')) return 'Looking for jobs? Let me know your preferences.';
        return 'Thank you for your question. I will get back to you soon with a professional answer.';
    }
});
