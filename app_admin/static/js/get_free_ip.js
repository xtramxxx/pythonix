/**
 * Получаем список свободных IP
 */


$(function () {


        $('#id_select_clients_group').change(function() {
            alert($("select#id_select_clients_group").val());

            $.get("/get_free_ipaddress/1/", function(data) { //Выполняем запрос на получение списка компаний.
                    var text = "<option value=''>Выберите компанию</option>";
                    for (var i in data) {  //Наполняем список элементами.
                        add_element = "<option value="+i+">"+data[i]+"</option>";
                        text += add_element;

                        $("#id_select_company").append( $(add_element));
                    }
                    document.add_client_form.select_ip.innerHTML = text;
                });
        });




    });