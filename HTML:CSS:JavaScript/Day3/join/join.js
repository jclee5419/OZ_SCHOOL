const form = document.getElementById("form")

form.addEventListener("submit", function(event){
    event.preventDefault() // 기본 동작 방지

    let userId = event.target.id.value
    let userPassword1 = event.target.password1.value
    let userPassword2 = event.target.password2.value
    let userName = event.target.name.value
    let userPhone = event.target.phone.value
    let userPosition = event.target.position.value
    let userGender = event.target.gender.value
    let userEmail = event.target.email.value
    let userIntroduction = event.target.introduction.value

    if (userId.length < 4) {
        alert("아이디는 4자 이상이어야 합니다. 다시 입력해주세요.")
        return
    }

    if(userPassword1 !== userPassword2) {
        alert("비밀번호가 일치하지 않습니다. 다시 입력해주세요.")
        return
    }

    document.body.innerHTML = ""
    document.write(`<p>${userId}님 가입을 환영합니다!.</p>`
    + `<p>회원가입시 입력하신 내역은 다음과 같습니다.</p>`
    + `<p>아이디: ${userId}</p>`
    + `<p>비밀번호: ${userPassword1}</p>`
    + `<p>이름: ${userName}</p>`
    + `<p>전화번호: ${userPhone}</p>`
    + `<p>원하는 직무: ${userPosition}</p>` 
    )
})
// 제출 이벤트 받기 (이벤트 핸들링)

// 제출된 입력값들을 참조

// 입력값에 문제가 있는 경우 이를 감지한다

// 가입 환영 인사를 제공한다
