<?php
require_once('conexion.php');  //llama al archivo conexion.php

$tarjeta=$_POST['device_label'];      //obtiene el dato de html
$chiller=$_POST['chiller'];
$ascensor1=$_POST['ascensor1'];

$conn = new conexionweb(); //crea la conexion

$consulta_insert = "INSERT INTO historicodedispositivos(idtarjeta,variable,valor_variable,fecha) VALUES ('$tarjeta','chiller','$chiller',NOW())";//inserta datos en la tabla
$insert = mysqli_query($conn->conectardb(),$consulta_insert); //inserta chiller

$consulta_insert = "INSERT INTO historicodedispositivos(idtarjeta,variable,valor_variable,fecha) VALUES ('$tarjeta','asc_1','$ascensor1',NOW())";
$insert = mysqli_query($conn->conectardb(),$consulta_insert); //inserta humedad

$consulta_update = "UPDATE estado_dispositivos SET chiller= $chiller, asc_1=$ascensor1 WHERE id_tarjeta= '$tarjeta'";//actualiza datos en la tabla (importantisimo)
$update = mysqli_query($conn->conectardb(),$consulta_update); //Update

$consulta_select = "SELECT * FROM estado_dispositivos WHERE id_tarjeta='$tarjeta'";//selecciona datos en la tabla para ver su estado
$select = mysqli_query($conn->conectardb(),$consulta_select); //select
$row = mysqli_fetch_row($select); //funcion crea un vector

$consulta_select_tarjeta3 = "SELECT chiller FROM estado_dispositivos WHERE id_tarjeta='tarjeta3'";//selecciona datos  de una columna en especifico en la tabla para ver su estado
$select_tarjeta3 = mysqli_query($conn->conectardb(),$consulta_select_tarjeta3); //select
$row_tarjeta3 = mysqli_fetch_row($select_tarjeta3); //funcion crea un vector
echo"{chiller=".$row_tarjeta3[0].",estado del chiller en la tarjeta 3}<br>";//muestra el estado de la base de datos (importantisimo)



echo"datos en la base <br>";
echo"{tarjeta=".$row[0].",chiller=".$row[1].",ascensor1=".$row[2].",planta1=".$row[3].",esc_1=".$row[4]."}<br>";//muestra el estado de la base de datos (importantisimo)
echo"datos enviados desde html <br>";
echo"{Tipo_tarjeta:".$tarjeta.",chiller:".$chiller.",ascensor1:".$ascensor1."}";

?>