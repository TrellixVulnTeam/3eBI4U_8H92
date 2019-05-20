$(document).ready(function(){
    $('.date').mask('00/00/0000');
    $('.cep').mask('00000-000');
    $('.tel').mask('(00)0000Z-0000', {translation: {'Z' : {pattern: /[0-9]/, optional: true}}});
    $('.money').mask('#.##0,00', {reverse: true});
    $('.percent').mask('00,00', {reverse: true});
    $('.cnpj').mask('00.000.000/0000-00', {reverse: true});
    $('.cpf').mask('000.000.000-00', {reverse: true});
});