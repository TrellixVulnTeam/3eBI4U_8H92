// CEP AUTOCOMPLETE ADDRESSES ON ADDRESS INFO PAGE
$(document).ready(function(){

    $('.js-cep').blur(function(){
        var cep = this.value.replace(/[^0-9]/, "");

        if(cep.length != 8){
            return false;
        }
        
       var url = "https://viacep.com.br/ws/"+cep+"/json/";
       
        $.getJSON(url, function(dadosRetorno){
            try{
                $('.js-end').val(dadosRetorno.logradouro);
                $('.js-bairro').val(dadosRetorno.bairro);
                $('.js-municipio').val(dadosRetorno.localidade);
                $('.js-estado').val(dadosRetorno.uf);
            }catch(ex){}
        });
    });

});

//MAKE VISIBLE SELECTION FIELD BAR ON FORM WIZARD TEMPLATES - VISIBILITY
function showField(x, y) {

    var checkbox    = document.getElementById(x);
    var elem     = document.getElementById(y);

    if (checkbox.checked == true){
        elem.style.visibility = "visible";
    } else{
        elem.style.visibility = "hidden";
    }
}

//MAKE VISIBLE SELECTION FIELD BAR ON FORM WIZARD TEMPLATES - DISPLAY
function displayField(x, y) {

    var checkbox    = document.getElementById(x);
    var elem     = document.getElementById(y);

    if (checkbox.checked == true){
        elem.style.display = "block";
    } else{
        elem.style.display = "none";
    }
}

function mascara(o,f){
    v_obj=o
    v_fun=f
    setTimeout("execmascara()",1)
}

function execmascara(){
    v_obj.value=v_fun(v_obj.value)
}

function soNumeros(v){
    return v.replace(/\D/g,"")
}

function telefone(v){
    v=v.replace(/\D/g,"")                 //Remove tudo o que não é dígito
    v=v.replace(/^(\d\d)(\d)/g,"($1) $2") //Coloca parênteses em volta dos dois primeiros dígitos
    v=v.replace(/(\d{4})(\d)/,"$1-$2")    //Coloca hífen entre o quarto e o quinto dígitos
    return v
}

function cpf(v){
    v=v.replace(/\D/g,"")                    //Remove tudo o que não é dígito
    v=v.replace(/(\d{3})(\d)/,"$1.$2")       //Coloca um ponto entre o terceiro e o quarto dígitos
    v=v.replace(/(\d{3})(\d)/,"$1.$2")       //Coloca um ponto entre o terceiro e o quarto dígitos
                                             //de novo (para o segundo bloco de números)
    v=v.replace(/(\d{3})(\d{1,2})$/,"$1-$2") //Coloca um hífen entre o terceiro e o quarto dígitos
    return v
}

function cep(v){
    v=v.replace(/D/g,"")                //Remove tudo o que não é dígito
    v=v.replace(/^(\d{5})(\d)/,"$1-$2") //Esse é tão fácil que não merece explicações
    return v
}

function cnpj(v){
    v=v.replace(/\D/g,"")                           //Remove tudo o que não é dígito
    v=v.replace(/^(\d{2})(\d)/,"$1.$2")             //Coloca ponto entre o segundo e o terceiro dígitos
    v=v.replace(/^(\d{2})\.(\d{3})(\d)/,"$1.$2.$3") //Coloca ponto entre o quinto e o sexto dígitos
    v=v.replace(/\.(\d{3})(\d)/,".$1/$2")           //Coloca uma barra entre o oitavo e o nono dígitos
    v=v.replace(/(\d{4})(\d)/,"$1-$2")              //Coloca um hífen depois do bloco de quatro dígitos
    return v
}