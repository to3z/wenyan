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
sentence_text.onchange=function()
{
    let sentence=this.value,
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
        appear_choice.innerHTML=highlight(sentence,appear_pos[0],appear_pos[0]+word.length,true);
    for(let i=1;i<appear_pos.length;++i)
        appear_choice.innerHTML=highlight(sentence,appear_pos[i],appear_pos[i]+word.length,true);
}
function single_tongjia()
{
    return `<input type=text" name="before">同<input type="text" name="after">`;
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
