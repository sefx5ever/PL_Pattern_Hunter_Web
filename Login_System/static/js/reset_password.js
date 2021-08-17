document.getElementById('reset-password-submit').addEventListener(
    "click", (event) => {
        event.preventDefault();
        request = new XMLHttpRequest();
        var url = window.location.protocol+'//'+window.location.host;
        var email = document.getElementById('reset-password-form-email').value;

        request.open(
            "POST",url+'/api/mail/'
        )
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        request.onload = () => {
            var resp = JSON.parse(request.responseText);
            console.log(resp);
            if (resp['status'] == true) {
                alert("提示：系統已重置密碼，請至電子郵箱查看！")
                window.location.href = url+'/login'
            } else {
                alert('提示：重置失敗！')
            };
        }

        request.send(JSON.stringify({
            "email" : email
        }));
    }
)