$(function () {
    $("form").submit(function () {
    //    拿用户名 判断不能为空 并且大于三位
        var name = $("#name_id").val();
        if (name.length < 3){
            alert("用户名过短");
            //阻止提交
            return false;
        }

        var pwd = $("#pwd_id").val();
        var confirm_pwd = $("#c_pwd_id").val();
        if (pwd == confirm_pwd & pwd.length>=6){
        //    做加密
            var enc_pwd = md5(pwd);
            var enc_confirm_pwd = md5(confirm_pwd);
        //    设置回去
            $("#pwd_id").val(enc_pwd);
            $("#c_pwd_id").val(enc_confirm_pwd);
        } else {
            alert("密码过短或不一致");
            return false;
        }

    });
    $("#name_id").change(function () {
        var uname = $("#name_id").val();
        $.ajax({
           url:"/axf/check_uname",
           data:{
               uname: uname
           },
           method:"get",
           success: function (res) {
           //    提示用户
               if (res.code == 1){
                   $("#uname_msg").html(res.msg);
               } else {
                   //错误提示
                   alert(res.msg);
               }
           }
        });
    })

});