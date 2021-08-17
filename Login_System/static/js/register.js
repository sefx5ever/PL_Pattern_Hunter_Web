document.getElementById('register-submit').addEventListener(
    "click", (event) => {
        event.preventDefault();
        request = new XMLHttpRequest();
        var url = window.location.protocol+'//'+window.location.host;
        var user = document.getElementById('register-form-user').value;
        var name = document.getElementById('register-form-name').value;
        var email = document.getElementById('register-form-email').value;
        var password = document.getElementById('register-form-password').value;
        var repassword = document.getElementById('register-form-repassword').value;
        var role = document.getElementById('register-form-identity').value;

        request.open(
            "POST",url+'/api/account/'
        )
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        request.onload = () => {
            var resp = JSON.parse(request.responseText);
            console.log(resp);
            if (resp['status'] == true) {
                alert("提示：恭喜您成功註冊，請至您的電子信息激活您的帳號！")
                window.location.href = url+'/login'
            } else {
                alert('提示：註冊失敗！')
            };
        }

        request.send(JSON.stringify({
            "user" : user,
            "name" : name,
            "email" : email,
            "role" : role,
            "password" : password,
            "repassword" : repassword
        }));
    }
)