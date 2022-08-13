addExplanation.onclick=function(){
    document.getElementById("formWrap").style.display="block";
    this.style.display="none";
}
backButton.onclick=function(){
    document.getElementById("formWrap").style.display="none";
    document.getElementById("addExplanation").style.display="flex";
}