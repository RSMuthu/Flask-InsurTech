// Function utilities for the Index page - Login/Register
function get_cookie_value(name) {
  // get the cookie value in the current page
  var result = document.cookie.match("(^|[^;]+)\\s*" + name + "\\s*=\\s*([^;]+)")
  return result ? result.pop() : ""
}

function process_login() {
  // to process the login request made by the user
  document.getElementById('login-submit').setAttribute('hidden','');
  document.getElementById('login-load').removeAttribute('hidden');
  if ($('#email').val().trim() == '' || $('#password').val().trim() == '') {
    alert("please enter all fields ...")
  } else {
    $.ajax({
      dataType  : 'json',
      data : JSON.stringify({
          email : $('#email').val(),
          passwd: md5($('#password').val())
        }),
        method : 'POST',
        url : '/auth/signin',
        contentType: "application/json",
        success: function(response) {
          location.href = "/dashboard"
        },
        error: function(response) {
          console.log(response)
          //var x = JSON.parse(response.responseText);
          //alert("Error: " + x.msg);
        }
      });
    }
    document.getElementById('login-load').setAttribute('hidden','');
    document.getElementById('login-submit').removeAttribute('hidden');
}

function process_register() {
  // to process the register request made by the user
  document.getElementById('register-submit').setAttribute('hidden','');
  document.getElementById('reg-load').removeAttribute('hidden');
  if ($('#password_reg').val().trim() == '' || $('#confirm_password').val().trim() == '' || $('#email_reg').val().trim() == '') {
    alert ("Please enter all the fields..");
  } else {
    var pass = $('#password_reg').val();
    var con_pass = $('#confirm_password').val();
    if (pass != con_pass) {
      alert("passwords do not match..")
    } else{
        $.ajax({
          dataType  : 'json',
          data : JSON.stringify({
              email : $('#email_reg').val(),
              passwd: md5(pass)
            }),
            method : 'POST',
            url : '/auth/signup',
            contentType: "application/json",
            success: function(response) {
              //var jwt = response.jwt;
              //localStorage.setItem("access_token") = jwt
              console.log(response);
              alert("User Registeration successful");
              location.reload();
            },
            error: function(error) {
              alert(errormsg);
            }
          });
      }
  }
  document.getElementById('reg-load').setAttribute('hidden','');
  document.getElementById('register-submit').removeAttribute('hidden');
}
