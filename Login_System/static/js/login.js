document.getElementById('login-submit').addEventListener(
    "click", (event) => {
        event.preventDefault();
        request = new XMLHttpRequest();
        var url = window.location.protocol+'//'+window.location.host;
        var user = document.getElementById('login-form-username').value
        var password = document.getElementById('login-form-password').value
        var params = `user=${user}&password=${password}`
        request.open(
                "GET",url+'/api/account/?'+params
        )
    
        request.onload = () => {
            
            var resp = JSON.parse(request.responseText);
            if (resp['status'] == true) {
                localStorage.setItem('acc',JSON.stringify(resp))
                window.location.href = url+'/dashboardUser'
            } else {
                alert('提示：您所輸入的帳號或密碼不正確！')
            };
        }

        request.send();
    }
)