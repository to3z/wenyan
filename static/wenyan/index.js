// 搜索联想
function resize_safari(){
    if(navigator.userAgent.indexOf("Safari")!=-1){
        $("#search_tips").css("padding-right","1px");
    }
}
$(document).ready(function(){
    $("#search").keyup(function(){
        let part=$(this).val();
        if(part=="")
        {
            $("#search_tips").html("");
            $("#search_tips").hide();
        }else{
            $.post("/wenyan/index_tips/",{search_part:part},function(result){
                if(result.code==200){
                    let htmlStr="";
                    for(let i=0;i<result.data.length;++i)
                        htmlStr+=`<li><a class="tipA" href="/wenyan/word/${result.data[i]}/">${result.data[i]}</a></li>`;
                    if(htmlStr!=""){
                        $("#search_tips").html(htmlStr);
                        $("#search_tips").show();
                        // $("#search_tips").css("display","inline-block");
                    }
                }
            },"json");
        }
    });
    // $("#search").blur(function(){
    //     $("#search_tips").empty();
    //     $("#search_tips").hide();
    //     $(this).css("border-bottom","4px solid rgb(55, 89, 152)");
    // });
});