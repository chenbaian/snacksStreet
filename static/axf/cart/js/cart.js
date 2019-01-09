/**
 * Created by c4513 on 2019/1/8.
 */
$(function () {
   $(".confirm").click(function () {
       $current_btn = $(this);
       var c_id = $(this).parents("li").attr("c_id");
   //    发送请求
       $.ajax({
           url:"/axf/cart_status",
           data:{
               c_id:c_id
           },
           method:"patch",
           success:function (res) {
               // console.log(res);
               if (res.code == 1){
               //    修改当前按钮的√
                   if (res.data.status){
                       $current_btn.find("span").find("span").html("√");
                   }
                   else {
                       $current_btn.find("span").find("span").html("");
                   }
               //   修改钱数
                   $("#money_id").html(res.data.sum_money);

               //    修改全选按钮
                   if (res.data.is_all_select){
                       $(".all_select > span > span").html("√");
                   }
                   else {
                       $(".all_select > span > span").html("");
                   }
               }
           }
       })
   });

   //   全选
   $(".all_select").click(function () {
       $.ajax({
           url:"/axf/cart_all_status",
           data:{},
           method:"put",
           success:function (res) {
               // console.log(res);
               if (res.code == 1){
               //    修改总价
                   $("#money_id").html(res.data.sum_money);
                   if (res.data.all_select){
                       $(".all_select>span>span").html("√");
                       $(".confirm").each(function () {
                           $(this).find("span").find("span").html("√");
                       })
                   }else {
                       $(".all_select>span>span").html("");
                       $(".confirm").each(function () {
                           $(this).find("span").find("span").html("");
                       })
                   }
               }
           }
       })
   });

//    加操作
   $(".addBtn").click(function () {
       var $current_btn = $(this);

       var c_id = $(this).parents("li").attr("c_id");
   //    发送请求
       $.ajax({
           url:"/axf/cart_item",
           data: {
               c_id: c_id
           },
           method:"post",
           success:function (res) {
               // console.log(res)
               if (res.code == 1){
                   //更新总价
                   $("#money_id").html(res.data.sum_money);
               //    更新显示的数量
                   $current_btn.prev().html(res.data.num);
               }else {
                   alert(res.msg);
               }
           }
       })
   });
//    减操作
   $(".subBtn").click(function () {
       var $current_btn = $(this);

       var c_id = $(this).parents("li").attr("c_id")

       $.ajax({
           url:"/axf/cart_item",
           data: {
               c_id: c_id
           },
           method: "delete",
           success:function (res) {
               // console.log(res);
               if (res.code==1) {
                   //更新商品数量
                   if (res.data.num == 0){
                       $current_btn.parents("li").remove();
                   }else {
                       $current_btn.next().html(res.data.num);
                   }
               //    更新总价
                   $("#money_id").html(res.data.sum_money);
               }else {
                   alert(res.msg);
               }
           }
       })
   });
//    下单
   $("#order").click(function () {
       var money = $("#money_id").html();
       console.log(money);
       if (parseFloat(money) > 0){
           // alert("您未下单");
           window.open("/axf/order", target="_self");
       }
   })
    
});