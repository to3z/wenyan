addExplanation.onclick=function(){
    document.getElementById("formWrap").style.display="block";
    this.style.display="none";
}
backButton.onclick=function(){
    document.getElementById("formWrap").style.display="none";
    document.getElementById("addExplanation").style.display="flex";
}
function show_deleteConf(elem){
    // elem: class="explanationOption explanationDelete"
    $(".deleteConf").hide(); // 隐藏其它deleteConf
    $(elem).parent().siblings(".deleteConf").show(); // 只显示本deleteConf
}
function hide_deleteConf(elem){
    // elem: class="darkButton deleteCancel"
    $(elem).parents(".deleteConf").hide();
}
$(document).ready(function(){
    $(".explanationDelete").click(function(){show_deleteConf(this);});
    $(".deleteCancel").click(function(){hide_deleteConf(this);});
});