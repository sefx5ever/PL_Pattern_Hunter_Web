window.onclick = function(e) {
    if  (e.target.matches('#dropdown-icon')) {  
        var buttonDropDown = document.getElementById("nav-ele");
        var iconDropDown = document.getElementById("dropdown-icon");

        if (buttonDropDown.style.display === "flex") {
            buttonDropDown.style.display = "none";
            iconDropDown.style.transform = "rotate(90deg)"
        } else { //if (buttonDropDown.style.display === "none")
            buttonDropDown.style.display = "flex";
            iconDropDown.style.transform = "rotate(0deg)"
        }
    }
};

window.onload = () => {
    if (localStorage.getItem("acc") != null) {
        var userData = JSON.parse(localStorage.getItem("acc"))
        var nameList = document.getElementsByClassName("ele-name");
        for (let i=0;i < nameList.length; i++) { 
            nameList[i].textContent = userData['name']
        }
        document.getElementById("account-username").value = userData['user']
        document.getElementById("account-email").value = userData['email']
        document.getElementById("account-name").value = userData['name']
    } else {
        alert('提示：請重新登錄網頁！')
        window.location.href = "/login/"
    }
};

document.getElementById('update-account-submit').addEventListener(
    "click", (event) => {
        var request = new XMLHttpRequest();
        var url = window.location.protocol+'//'+window.location.host;
        event.preventDefault();
        var user = document.getElementById('account-username').value
        var name = document.getElementById('account-name').value
        var email = document.getElementById('account-email').value
        var password = document.getElementById('account-password').value
        var repassword = document.getElementById('account-re-password').value

        if(password != "" && repassword != "") {
            request.open(
                "PUT",url+'/api/account/'
            )
            request.setRequestHeader('Content-type','application/json; charset=utf-8');

            request.onload = () => {
                var resp = JSON.parse(request.responseText);
                if (resp['status'] == true) {
                    localStorage.setItem('acc',JSON.stringify(resp))
                    alert('提示：完成更新帳號資訊！')
                } else {
                    alert('提示：抱歉，網路傳輸有誤！')
                };
            }
    
            request.send(JSON.stringify({
                "user" : user,
                "name" : name,
                "email" : email,
                "password" : password,
                "repassword" : repassword
            }));
        } else {
            alert('提示：請輸入密碼！')
        }
    }
)

document.getElementById('del-account-submit').addEventListener(
    "click", (event) => {
        event.preventDefault();
        var password = document.getElementById('account-password').value
        var repassword = document.getElementById('account-re-password').value
        if(password != "" && repassword != "") {
            var request_del = new XMLHttpRequest();
            var url = window.location.protocol+'//'+window.location.host;
            var cofirmation = window.confirm("提示：您確認刪除帳號？");
            console.log(cofirmation)
            if (cofirmation) {
                var user = JSON.parse(localStorage.getItem('acc'))['user']
                request_del.open(
                    "DELETE",url+`/api/account/?user=${user}`
                )
            
                request_del.onload = () => {
                    var resp = JSON.parse(request_del.responseText);
                    if (resp['status'] == true) {
                        alert('提示：您的帳號已刪除！')
                        window.location.href = '/login'
                    } else {
                        alert('提示：抱歉，網路傳輸有誤！')
                    }
                };
                
                request_del.send()
            }
        } else {
            alert('提示：請輸入密碼！')
        }
    }
)
