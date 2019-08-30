$(document).ready(function(){ // makes sure that html, css, cdn links are loaded before javascript can be used
    $('#email_field').keyup(function(){ // STEP 1 - client triggers our event listener on an HTML element tag
        var data = $('#email_field').serialize(); // storing the data from the input field into a variable
        $.ajax({ // STEP 2 - we call the appropriate server route without the page refreshing
            url: "/email",
            method: "POST",
            data: data // we send the data to the route, just like form data when we click the submit button
        })
        .done(function(res){ // STEP 4 - Once the server route finished and sends back a response, this callback 
                            // function is triggered
            $('#email_msg').html(res); // we inject the html we received back into our page
        });
    });
});
