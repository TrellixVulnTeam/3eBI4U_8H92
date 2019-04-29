// CEP AUTOCOMPLETE ADDRESSES ON ADDRESS INFO PAGE
$(document).ready(function(){

    jQuery('input[name="Address Info-end_CEP"]').blur(function(){
        var cep = jQuery('input[name="Address Info-end_CEP"]').val().replace(/[^0-9]/, "");

        if(cep.length != 8){
            return false;
        }
        
       var url = "https://viacep.com.br/ws/"+cep+"/json/";
       
        $.getJSON(url, function(dadosRetorno){
            try{
                jQuery('input[name="Address Info-end_geral"]').val(dadosRetorno.logradouro);
                jQuery('input[name="Address Info-end_bairro"]').val(dadosRetorno.bairro);
                jQuery('input[name="Address Info-end_municipio"]').val(dadosRetorno.localidade);
                jQuery('input[name="Address Info-end_estado"]').val(dadosRetorno.uf);
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



