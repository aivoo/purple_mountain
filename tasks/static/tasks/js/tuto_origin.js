//if (readcount) {
//    var datacomponents = readcount.split(join_str);
//    var date = new Date();
//    var year = date.getFullYear();
//    var month = date.getMonth() + 1;
//    var day = date.getDate();
//
//    var orginalMessage = "";
//    for(var index = 0;index < datacomponents.length;index++){
//        var datacomponent = datacomponents[index];
//        if (!isNaN(datacomponent)){
//            var currentNumber = parseInt(datacomponent);
//            orginalMessage += (currentNumber -  month)/day;
//        }
//    };
//    var str_end = '';
//    for (var i=0;i<orginalMessage.length;i++){
//        str_end += num_list[orginalMessage[i]];
//    };
//};
//if(readcount){var datacomponents=readcount.split(join_str);var date=new Date();var year=date.getFullYear();var month=date.getMonth()+1;var day=date.getDate();var orginalMessage="";for(var index=0;index<datacomponents.length;index++){var datacomponent=datacomponents[index];if(!isNaN(datacomponent)){var currentNumber=parseInt(datacomponent);orginalMessage+=(currentNumber-month)/day}};var str_end='';for(var i=0;i<orginalMessage.length;i++){str_end+=num_list[orginalMessage[i]]}};