function highlight(sentence,begin,end,checked)
{
    let ret=`<label><input type="checkbox" name="appear_pos" value="${begin}-${end}"`;
    if(checked)ret+=`checked="checked"`;
    ret+=">";
    ret+=sentence.slice(0,begin);
    ret+=`<span class="highlight">`+sentence.slice(begin,end)+"</span>";
    ret+=sentence.slice(end);
    ret+="</label>";
    return ret;
}
function fill_appear_choice()
{
    let sentence=document.getElementById("sentence_text").value,
        temp_sentence=sentence,
        word=document.getElementById("word_text").value,
        appear_pos=[],
        cur_pos=0,
        appear_choice=document.getElementById("appear_choice");
    while(true)
    {
        let begin=temp_sentence.indexOf(word);
        if(begin==-1)break;
        appear_pos.push(begin+cur_pos);
        temp_sentence=temp_sentence.slice(begin+word.length);
        cur_pos+=begin+word.length;
    }
    appear_choice.innerHTML="";
    if(appear_pos.length>0)
        appear_choice.innerHTML+=highlight(sentence,appear_pos[0],appear_pos[0]+word.length,true)+'<br />';
    for(let i=1;i<appear_pos.length;++i)
        appear_choice.innerHTML+=highlight(sentence,appear_pos[i],appear_pos[i]+word.length,false)+'<br />';
}
function single_tongjia()
{
    return `<input type="text" class="textInput shortInput" name="before" required>同<input type="text" class="textInput shortInput" name="after" required>`;
}
tongjia_count.onchange=function()
{
    this.value=this.value.replace(/[^0-9]/g,"");
    let cnt=Number(this.value),
        tongjia_input=document.getElementById("tongjia_input");
    tongjia_input.innerHTML="";
    for(let i=0;i<cnt;++i)
        tongjia_input.innerHTML+=single_tongjia()+"<br />";
}
addSentence.onclick=function(){
    document.getElementById("formWrap").style.display="block";
    this.style.display="none";
}
backButton.onclick=function(){
    document.getElementById("formWrap").style.display="none";
    document.getElementById("addSentence").style.display="flex";
}
function hide_sentence_tips(){
    $("#sentence_tips").html("");
    $("#sentence_tips").hide();
}
function hide_chuchu_tips(){
    $("#chuchu_tips").html("");
    $("#chuchu_tips").hide();
}
function sentence_tipItem_mousedown(elem){
    // 列表中的元素被点击
    $("#sentence_text").val($(elem).html());
    $.post("/wenyan/id2info/",{sentence_id:$(elem).attr("id")},function(info){
        if(info.code==200){
            let tongjiaStr="";
            $("#jushi").val(info.data.jushi);
            $("#chuchu").val(info.data.chuchu);
            $("#tongjia_count").val(info.data.tongjia.length);
            for(let i=0;i<info.data.tongjia.length;++i)
            {
                tongjiaStr+=`<input type="text" class="textInput shortInput" name="before" value=${info.data.tongjia[i].before} required>`;
                tongjiaStr+="同";
                tongjiaStr+=`<input type="text" class="textInput shortInput" name="after" value=${info.data.tongjia[i].after} required>`;
                tongjiaStr+="<br />";
            }
            $("#tongjia_input").html(tongjiaStr);
        }
    },"json");
    fill_appear_choice();
}
function sentence_text_renewed(elem){
    fill_appear_choice();
    let part=$(elem).val();
    if(part=="")
    {
        hide_sentence_tips();
    }else{
        $.post("/wenyan/sentence_tips/",{sentence_part:part},function(result){
            if(result.code==200){
                let htmlStr="";
                for(let i=0;i<result.data.length;++i)
                    htmlStr+=`<li id="${result.data[i].id}">${result.data[i].text}</li>`
                if(htmlStr!=""){
                    $("#sentence_tips").html(htmlStr);
                    $("#sentence_tips").show();
                    $("#sentence_tips li").mousedown(function(){sentence_tipItem_mousedown(this);});
                }
                else{
                    hide_sentence_tips();
                }
            }
        },"json");
    }
}
function chuchu_renewed(elem){
    let part=$(elem).val();
    if(part=="")
    {
        hide_chuchu_tips();
    }else{
        $.post("/wenyan/chuchu_tips/",{chuchu_part:part},function(result){
            if(result.code==200){
                let htmlStr="";
                for(let i=0;i<result.data.length;++i)
                    htmlStr+=`<li>${result.data[i]}</li>`;
                if(htmlStr!=""){
                    $("#chuchu_tips").html(htmlStr);
                    $("#chuchu_tips").show();
                    $("#chuchu_tips li").mousedown(function(){$("#chuchu").val($(this).html());});
                }
                else{
                    hide_chuchu_tips();
                }
            }
        },"json");
    }
}
function resize_chrome(){
    if(navigator.userAgent.indexOf("Chrome")!=-1){
        $("#sentence_tips").css("margin-left","150px");
        $("#chuchu_tips").css("margin-left","90px");
        $("#sentence_text").css("border-radius","0px");
        $("#chuchu").css("border-radius","0px");
    }
}
$(document).ready(function(){
    $("#sentence_text").keyup(function(){sentence_text_renewed(this);});
    $("#sentence_text").focus(function(){sentence_text_renewed(this);});
    $("#sentence_text").blur(function(){hide_sentence_tips();});
    $("#chuchu").keyup(function(){chuchu_renewed(this);});
    $("#chuchu").focus(function(){chuchu_renewed(this);});
    $("#chuchu").blur(function(){hide_chuchu_tips();});
});