<?php
//実動作環境ではsmartyを使用しているためsmartyの構成ファイル読み込み
require('./libs/Smarty.class.php');
$smarty = new Smarty;

$command = "/usr/bin/python3 finance_viet_dol.py 2>&1";
exec($command,$output);
$VNDUSD=$output[0];


//smartyでhtmlファイルへレートデータを返す
$smarty->assign("VNDUSD", $VNDUSD);
$smarty->display('exchange.html');

?>