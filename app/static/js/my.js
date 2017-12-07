function isEmpty(){
    //form1是form中的name属性
    var conf_data = document.conf_data;

    if(conf_data.inter_name.value.trim()==""){
        alert("接口名不能为空!");
        return
    }
    if(conf_data.inter_url.value.trim()==""){
        alert("接口地址不能为空!");
        return
    }
    if(conf_data.inter_expect.value.trim()==""){
        alert("接口预期结果不能为空!");
        return
    }
    alert("保存成功!")
    return true;
}