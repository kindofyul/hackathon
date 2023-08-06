// 제출하기 버튼을 클릭했을 때의 동작
document.getElementById("submitBtn").addEventListener("click", function() {
    // 팝업창으로 띄울 페이지의 URL
    var confirmationPageURL = "popup.html"; // 여기에 별도의 확인 페이지 URL을 입력해주세요.
  
    // 팝업 창의 크기와 위치를 지정
    var popupWidth = 400;
    var popupHeight = 300;
    var popupLeft = (window.innerWidth - popupWidth) / 2;
    var popupTop = (window.innerHeight - popupHeight) / 2;
  
    // 팝업 창 열기
    window.open(
      confirmationPageURL,
      "_blank",
      "width=" + popupWidth + ",height=" + popupHeight + ",left=" + popupLeft + ",top=" + popupTop
    );
  });
  
