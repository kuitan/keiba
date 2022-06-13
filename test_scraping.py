import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np


def get_test_data(param):
    result_dir = param['result_dir']
    url = param['test_url']

    proxies = {
        "http": "http://proxy.nagaokaut.ac.jp:8080",
        "https": "http://proxy.nagaokaut.ac.jp:8080"
    }

    # ブラウザを起動
    options = Options()
    options.add_argument('--headless')
    chrome_service = service.Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=options)

    # 検索
    driver.get(url)
    time.sleep(1)

    pd.set_option('display.max_columns', 100)

    # htmlを取得
    source_code = driver.page_source
    source_code = """
    
<!DOCTYPE html>
<html>
<head>
<meta charset="EUC-JP">

<!-- block=common__meta_tag_each_race (cg) -->
<meta http-equiv="content-language" content="ja">
<meta http-equiv="X-UA-Compatible" content="IE=edge"/>
<meta name="viewport" content="width=1000">
<meta name="format-detection" content="telephone=no" />
<meta name="description" content="2022年6月12日 東京11R エプソムカップ(G3)の出馬表です。JRA開催レースの出馬表や最新オッズ、レース結果速報、払戻情報をはじめ、競馬予想やデータ分析など予想に役立つ情報も満載です。" />
<meta name="keywords" content="競馬,keiba,出馬表,オッズ,予想,レース結果,払戻し,結果速報,競馬予想,ネット競馬,netkeiba" />
<meta name="thumbnail" content="https://www.netkeiba.com/style/netkeiba.ja/image/netkeiba.png" />
<!-- ogp用 -->
<meta property="og:site_name" content="netkeiba.com" />
<meta property="og:type" content="article" />
<meta property="og:title" content="エプソムカップ(G3) 出馬表 | 2022年6月12日 東京11R レース情報(JRA) - netkeiba.com" />
<meta property="og:url" content="https://race.netkeiba.com/race/shutuba.html?race_id=202205030411" />
<meta property="og:description" content="2022年6月12日 東京11R エプソムカップ(G3)の出馬表です。JRA開催レースの出馬表や最新オッズ、レース結果速報、払戻情報をはじめ、競馬予想やデータ分析など予想に役立つ情報も満載です。" />
<meta property="og:image" content="https://www.netkeiba.com/style/netkeiba.ja/image/netkeiba.png" />
<!-- Twitter用 -->
<meta property="twitter:card" content="summary">
<meta property="twitter:site" content="@netkeiba">
<!-- Facebook用 -->
<meta property="fb:admins" content="30367" />
<link rel="canonical" href="https://race.netkeiba.com/race/shutuba.html?race_id=202205030411" />
<link rel="alternate" media="only screen and (max-width: 640px)" href="https://race.sp.netkeiba.com/race/shutuba.html?race_id=202205030411" />
<link rel="alternate" type="application/rss+xml" href="https://rss.netkeiba.com?pid=rss_netkeiba&site=netkeiba" />
<!-- アノテーション -->
<title>エプソムカップ(G3) 出馬表 | 2022年6月12日 東京11R レース情報(JRA) - netkeiba.com</title>
<script type="application/ld+json">
[
{
"@context": "http://schema.org",
"@type": "BreadcrumbList",
"itemListElement": [
{
"@type": "ListItem",
"position": 1,
"item": {
"@id": "https://www.netkeiba.com/",
"name": "netkeiba.comトップ"
}
},
{
"@type": "ListItem",
"position": 2,
"item": {
"@id": "https://race.netkeiba.com/top/",
"name": "レース情報(JRA) "
}
},
{
"@type": "ListItem",
"position": 3,
"item": {
"@id": "https://race.netkeiba.com/race/shutuba.html?race_id=202205030411&rf=race_submenu",
"name": "エプソムカップ(G3) 出馬表 | 2022年6月12日 東京11R"
}
}
]
},
{
"@context": "http://schema.org",
"@type": "WebSite",
"url": "https://www.netkeiba.com/",
"name": "netkeiba.com",
"alternateName": "netkeiba.com - 国内最大級の競馬情報サイト",
"description": "netkeiba.comは国内最大級の競馬情報サイトです。JRA全レースの出馬表やオッズ・予想、ニュース、コラム、競走馬50万頭以上収録の競馬データベース、地方競馬、POG、予想大会、コミュニティなどがご利用いただけます。",
"sameAs": [
"https://twitter.com/netkeiba",
"https://www.facebook.com/netkeiba"
]
},
{
"@context": "http://www.schema.org",
"@type": "Organization",
"name": "netkeiba.com",
"url": "https://www.netkeiba.com/",
"logo": "https://cdn.netkeiba.com/img.sp/common/img/common/netkeiba_logo.png",
"description": "netkeiba.comは国内最大級の競馬情報サイト「netkeiba.com」を運営しています。"
}
]
</script>
<!-- block=common__advertisement_taboola_head (d) -->
<script type="text/javascript">
window._taboola = window._taboola || [];
_taboola.push({article:'auto'});
!function (e, f, u, i) {
if (!document.getElementById(i)){
e.async = 1;
e.src = u;
e.id = i;
f.parentNode.insertBefore(e, f);
}
}(document.createElement('script'),
document.getElementsByTagName('script')[0],
'//cdn.taboola.com/libtrc/netkeiba/loader.js',
'tb_loader_script');
if(window.performance && typeof window.performance.mark == 'function') {window.performance.mark('tbl_ic');}
</script>
<!-- 共通css include -->
<!-- block=common__css (d) -->
<link rel='stylesheet' href="https://cdn.netkeiba.com/img.racev3/common/css/race_pc_new.css?20220304" type='text/css' media="all">
<link rel='stylesheet' href="https://cdn.netkeiba.com/img.racev3/common/css/colorbox.css" type='text/css' media="all">
<!-- 共通js include -->
<!-- block=common__js (d) -->
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
<script type="text/javascript" src="https://cdn.netkeiba.com/img.racev3/common/js/slick.min.js?2019080501"></script>
<script type="text/javascript" src="https://cdn.netkeiba.com/img.racev3/common/js/raceapi.action.js?2019073001"></script>
<script type="text/javascript" src="https://cdn.netkeiba.com/img.racev3/common/js/YosoJranar.js?2019073001" type="text/javascript"></script>
<script type="text/javascript" src="https://cdn.netkeiba.com/img.racev3/common/js/sweetalert.min.js?2019073001" type="text/javascript"></script>
<script type="text/javascript" src="https://cdn.netkeiba.com/img.racev3/common/js/jquery.colorbox.js?2019073001"></script>
<script type="text/javascript" src="https://cdn.netkeiba.com/img.regist.sp/common/js/monthly_goods_link.js?2019101001"></script>
<script type="text/javascript" src="https://cdn.netkeiba.com/img.racev3/common/js/common_pc_new.js?2019073001" type="text/javascript"></script>
<script type="text/javascript">
// $Id: race_common_js.html 20040 2019-02-28 07:05:48Z m-ashizawa $
//window.console = {};
//window.console.log = function(i){return;};
</script>
<!-- GoogleAdsense -->
<script async type="text/javascript" src="https://cpt.geniee.jp/hb/v1/211239/47/wrapper.min.js"></script>
<script async src="https://securepubads.g.doubleclick.net/tag/js/gpt.js"></script>
<script>
window.googletag = window.googletag || {cmd: []};
googletag.cmd.push(function() {
googletag.defineSlot('/9116787,21246805/1491440', [[728, 90], 'fluid'], '1491440').addService(googletag.pubads());
googletag.defineSlot('/9116787,21246805/1492791', [728, 90], '1492791').addService(googletag.pubads());
googletag.defineSlot('/9116787,21246805/1491441', [[300, 250], 'fluid', [250, 250], [336, 280], [200, 200], [320, 180]],'1491441').addService(googletag.pubads());
googletag.defineSlot('/9116787,21246805/1491442', [[160, 600], 'fluid'], '1491442').addService(googletag.pubads());
googletag.defineSlot('/9116787,21246805/1491463', [728, 90], '1491463').addService(googletag.pubads());
googletag.pubads().enableSingleRequest();
googletag.pubads().disableInitialLoad();
googletag.enableServices();
});
</script>
<script type="text/javascript" src="https://cdn.netkeiba.com/img.racev3/common/js/jquery.lazyscript.js"></script>
<!-- その他 include -->
<!-- block=race_common_other (d) -->

</head>
<body class="race page_race_shutuba" id="race_top">
<div id="page">
<noscript>
お客様のブラウザはジャバスクリプト（JavaScript）に対応していないか無効になっています。
</noscript>
<!-- block=common__race_header (d) -->
<link rel="stylesheet" href="https://cdn.netkeiba.com/img.www/style/netkeiba.ja/css/pc_header.css" type="text/css" media="all" />

<header class="Header_Area fc">
<div class="Header_Inner">
<h1>
<a href="https://www.netkeiba.com/?rf=logo" title="netkeiba.com">
<img src="https://cdn.netkeiba.com/img.www/style/netkeiba.ja/image/common/netkeiba_logo01.png" alt="netkeiba.com">
</a>
</h1>
<div class="DB_Search_Input">
<form class="Search_Box" action="https://www.netkeiba.com/" method="POST">
<input type="hidden" name="pid" value="search">
<input type="hidden" name="type" value="db">
<div class="InputTxt_Form_Box">

<input class="Txt_Form" placeholder="馬名で検索" value="" type="text" name="word" id="keywords">
</div><!-- / .InputTxt_Form -->
<div class="Submit_Btn_Box">
<svg xmlns="http://www.w3.org/2000/svg" width="41.05" height="41.05" viewBox="0 0 41.05 41.05" class="IconInput01">
<g id="icon_search" transform="translate(-234.6 -459.7)">
<circle cx="15.6" cy="15.6" r="15.6" transform="translate(236.1 461.2)" class="st0"/>
<g>
<path d="M275.2,498.2a1.335,1.335,0,0,1,0,2l-.1.1a1.335,1.335,0,0,1-2,0l-11.2-11.2a1.335,1.335,0,0,1,0-2l.1-.1a1.335,1.335,0,0,1,2,0Z" class="st1"/>
</g>
</g>
</svg>
<input class="Submit_Btn" type="submit" name="submit" value="検 索">
</div><!-- / .Submit_Btn_Box -->
</form>
</div><!-- / .DB_Search_Input -->
<ul class="UserMyMenu fc">

<li>
<a href="https://regist.netkeiba.com/?pid=premium&rf=header">
<span>プレミアムサービス</span>
</a>
</li>
<li>
<a href="https://race.netkeiba.com/bookmark/bookmark.html?rf=navi" class="Icon_Header Icon_MyfavHorse">
<span>お気に入り馬</span>
</a>
</li>
<li>
<a href="https://regist.netkeiba.com/account/?pid=login" class="Icon_Header Icon_Login">
<span>ログイン/会員登録</span>
</a>
</li>
<li class="disp_none header_stage_area no_login_show">
<a href="https://regist.netkeiba.com?pid=stage_login&action=login&return_url=https://regist.netkeiba.com">
<span>(s)ログイン</span>
</a>
</li>
<li class="disp_none header_stage_area no_login_show">
<a href="https://regist.netkeiba.com?pid=user_add_form&payment=nk_user&goods_cd=310409&opt=init">
<span>(s)無料会員登録</span>
</a>
<li class="disp_none header_stage_area login_show">
<a href="https://regist.netkeiba.com?pid=stage_login&action=logout&return_url=https://regist.netkeiba.com">
<span>(s)ログアウト</span>
</a>
</li>
</ul>
<div class="SiteToggleBtn01 Keirin">
<a href="https://keirin.netkeiba.com/?rf=nk_pc_header">
<span class="LiveRace">LIVE</span>
<img src="https://cdn.netkeiba.com/img.www/style/netkeiba.ja/image/common/icon_keirin01.png" alt="" width="21" height="16" class="KeirinLogoMark01">競輪
</a>
</div><!-- /.SiteToggleBtn01 -->
</div><!-- /.Header_Inner -->
</header>
<nav class="ContentNavi01">
<ul class="fc">
<li class="Top">
<a href="https://www.netkeiba.com/?rf=navi" title="トップ" id="navi_link_top">トップ</a>
</li>
<li class="News">
<a href="https://news.netkeiba.com?rf=navi" title="ニュース" id="navi_link_news">ニュース</a>
</li>
<li class="Race">
<a href="../top/" title="レース" id="navi_link_race">レース</a>
</li>
<li class="Yoso">
<a href="https://yoso.netkeiba.com?access=init&rf=navi" title="予想" id="navi_link_yoso">予想</a>
</li>
<li class="Column">
<a href="https://news.netkeiba.com?pid=column_top&rf=navi" title="コラム" id="navi_link_column">コラム</a>
</li>
<li class="Tv">
<a href="https://tv.netkeiba.com/?rf=navi" title="netkeibaTV" id="navi_link_tv">netkeibaTV</a>
</li>
<li class="Local">
<a href="https://nar.netkeiba.com/top/?rf=navi" title="地方競馬" id="navi_link_nar">地方競馬</a>
</li>
<li class="Db">
<a href="https://db.netkeiba.com?rf=navi" title="データベース" id="navi_link_db">データベース</a>
</li>
<li class="Paper">
<a href="https://yoso.netkeiba.com/senmonshi/?rf=navi" title="競馬新聞" id="navi_link_senmonshi">競馬新聞</a>
</li>
<li class="YosoCS">
<a href="https://orepro.netkeiba.com?rf=navi" title="俺プロ" id="navi_link_orepro">俺プロ</a>
</li>
<li class="Owner">
<a href="https://owner.netkeiba.com?rf=navi" title="一口馬主" id="navi_link_owner">一口馬主</a>
</li>
<li class="Pog">
<a href="https://pog.netkeiba.com?rf=navi" title="POG" id="navi_link_pog">POG</a>
</li>
<li class="Matome">
<a href="https://dir.netkeiba.com//keibamatome/index.html?rf=navi" title="まとめ" id="navi_link_keibamatome">まとめ</a>
</li>
</ul>
</nav><!-- /.ContentNavi01 -->
<!-- 広告配信用 -->
<script>
var googletag = googletag || {};
googletag.cmd = googletag.cmd || [];
</script>
<!-- /広告配信用 -->
<script type="text/javascript">
$(document).ready(function() {
show_user();
});
function show_user(){
var is_stage = '';
var is_user  = '';
var is_alert = '';
var is_sp    = '';
var nickname = '';
var user_img = '';
if(is_sp) {
$('.sp_nk_btn').show();
}
if(! is_stage) {
$('.header_stage_area').remove();
}
if(is_user){
//ログイン中
$('.login_show').show();
if(is_alert) {
$('.Alert_New').show();
}
} else {
//未ログイン
$('.no_login_show').show();
$('.login_show').remove();
}
}
</script>
<!-- block=shutuba__race_title (cg) -->
<div class="RaceChange_BtnArea">
<div class="RaceList_Date clearfix">
<div class="RaceDayPrev">
<a href="../top/race_list.html?kaisai_date=20220605#racelist_top_a" class="Active">前</a>
</div>

<dl id="RaceList_DateList">

<dd><a href="../top/race_list.html?&kaisai_date=20220604&kaisai_id=2022070401&current_group=1020220611#racelist_top_a" title="6月4日(土)" class="">6月4日<span class="Sat">(土)</span></a></dd>
<dd><a href="../top/race_list.html?&kaisai_date=20220605&kaisai_id=2022070402&current_group=1020220611#racelist_top_a" title="6月5日(日)" class="">6月5日<span class="Sun">(日)</span></a></dd>
<dd><a href="../top/race_list.html?&kaisai_date=20220611&kaisai_id=2022070403&current_group=1020220611#racelist_top_a" title="6月11日(土)" class="">6月11日<span class="Sat">(土)</span></a></dd><dd class="Active"><a href="../top/race_list.html?kaisai_date=20220612&kaisai_id=2022070404&current_group=1020220611#racelist_top_a" title="6月12日(日)">6月12日<span class="Sun">(日)</span></a></dd>

</dl>

<div class="RaceDayNext NoLink">
<span>次</span>
</div>
</div><!-- /.RaceDayWrap -->
</div>
<!-- block=shutuba__change_session (d) -->
<script type="text/javascript">
var _action_api_url_change_session = '/api/api_post_change_session.html';
</script>

<div class="RaceColumn01">
<div class="RaceColumnWrap fc">
<div class="RaceMainColumn">
<!-- block=shutuba__race_kaisai_navi (cg) -->
<script>
$(function() {
$('body').append('<div id="modal_overlay_menu"></div>');
var overlay = $('#modal_overlay_menu');
var content = $('#modal_content_menu');
$('.RaceUseful_Btn').click(function() {
overlay.show().html($('#modal_content_menu').html());
});
overlay.click(function() {
$(this).hide();
});
$('.Close').click(function() {
overlay.hide();
});
});
</script>
<div class="RaceKaisaiWrap">
<ul class="Col Col3">
<li class="Active"><a href="?race_id=202205030411">東京</a></li>

<li><a href="?race_id=202207040411">中京</a></li>

<li><a href="?race_id=202202010211">函館</a></li>

</ul>
</div>
<!-- /.RaceKaisaiWrap -->
<!-- block=shutuba__race_kaisai_wrap (cg) -->
<div class="RaceNumWrap">
<ul class="fc">
<li class="">
<a href="?race_id=202205030401" title="3歳未勝利">
1R
</a>
</li><li class="">
<a href="?race_id=202205030402" title="3歳未勝利">
2R
</a>
</li><li class="">
<a href="?race_id=202205030403" title="3歳未勝利">
3R
</a>
</li><li class="">
<a href="?race_id=202205030404" title="3歳未勝利">
4R
</a>
</li><li class="">
<a href="?race_id=202205030405" title="2歳新馬">
5R
</a>
</li><li class="">
<a href="?race_id=202205030406" title="3歳未勝利">
6R
</a>
</li><li class="">
<a href="?race_id=202205030407" title="3歳以上1勝クラス">
7R
</a>
</li><li class="">
<a href="?race_id=202205030408" title="3歳以上1勝クラス">
8R
</a>
</li><li class="">
<a href="?race_id=202205030409" title="八王子特別">
9R
</a>
</li><li class="">
<a href="?race_id=202205030410" title="夏至S">
10R
</a>
</li><li class="Active">
<a href="?race_id=202205030411" title="エプソムC">
11R
</a>
</li><li class="">
<a href="?race_id=202205030412" title="3歳以上1勝クラス">
12R
</a>
</li>
</ul>
</div><!-- /.RaceNumWrap -->
<!-- block=shutuba__race_main_column (cg) -->
<div class="RaceList_NameBox">
<div class="RaceList_Item01">
<span class="RaceNum">11R</span>
</div><!-- /.RaceList_Item01 -->
<div class="RaceList_Item02">
<div class="RaceName">エプソムC



<span class="Icon_GradeType Icon_GradeType3"></span>












<span class="Icon_GradeType Icon_GradeType13 Icon_GradePos01"></span>
</div>
<div class="RaceData01">
15:45発走 /<!-- <span class="Turf"> --><span> 芝1800m</span> (左)
/ 天候:晴<span class="Icon_Weather Weather01"></span>
<span class="Item03">/ 馬場:重</span>

</div>
<div class="RaceData02">
<span>3回</span>
<span>東京</span>
<span>4日目</span>
<span>サラ系３歳以上</span>
<span>オープン</span>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<span>(国際)(特指)</span>
<span>別定</span>
<span>12頭</span>
<br>
<span>本賞金:4300,1700,1100,650,430万円</span>
</div>
</div><!-- /.RaceList_Item02 -->
<div class="RaceList_Item03">
<div class="Refundlink">
<a href="../top/payback_list.html?kaisai_date=20220612&kaisai_id=2022050304" class="LinkMore">東京 払戻一覧</a>
</div>
<ul class="RaceHeadBtnArea">
<li>
<a href="https://cdn.netkeiba.com/img.racev3/common/img/course/05_t1800.png?2019073001" class="Popup_Img MapRaceBtn">
<span><img src="https://cdn.netkeiba.com/img.racev3/common/img/course/thumb_62/05_t1800.png?2019073001" onerror="replaceDefaultNoImage()" alt="Course"/></span>
コース詳細
</a>
<script>
function replaceDefaultNoImage() {
var baseurl = "https://cdn.netkeiba.com/img.racev3/common/img/course/";
$("a.Popup_Img").attr("href", baseurl + "soon.png");
$("a.Popup_Img img").attr("src", baseurl + "soon.png");
}
</script>
</li>
<li>
<a href="/ipat/dispatch.html?race_id=202205030411" target="_blank" class="IpatBtn01">
<img disabled="false" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/icon_ipat01.png?2019073001" alt="IPAT" /><span>連携</span>
</a>

</li>
</ul>
<div class="OreproLink">
<a class="LinkMore SpecialGo" href="../special/index.html?race_id=202205030411">特集へ</a>
<a class="LinkMore" href="https://orepro.netkeiba.com/bet/shutuba.html?race_id=202205030411&mode=init"><span>俺プロへ</span></a></div>
</div><!-- /.RaceList_Item03 -->
</div><!-- /.RaceList_NameBox -->
<script>
$(function() {
$('.RaceList_NameBox > a').append('<span class="Icon_ArrowB"></span>');
$('.RaceList_NameBox > a').click(function() {
$('.RaceList_NameBox a > span').toggleClass('Icon_ArrowT').toggleClass('Icon_ArrowB')
$('.RaceData_Hide').slideToggle('fast');
return false;
});
if ($("a.Popup_Img").length) {
$("a.Popup_Img").colorbox();
}
});
</script>
</div><!-- /.RaceMainColumn -->
<div class="RaceSideColumn">

<!-- block=common__advertisement (d) -->
<script src="https://cdn.netkeiba.com/img.sp/common/js/loadFif.js?ver=20200228"></script>
<div class="nk_AdvBox_pc new_race_rectangle race_shutuba  ">
<div id="new_race_rectangle"></div>
<script language="JavaScript" type="text/javascript">
if(typeof loadDuraFiF !== "undefined") {
loadDuraFiF("new_race_rectangle",23);
}
</script>
</div>
</div>
</div><!-- /.RaceColumnWrap -->
</div><!-- /.RaceColumn01 -->
<div class="RaceColumn02">
<!-- block=shutuba__race_menu (d) -->
<div class="RaceMenuArea">
<ul class="RaceMainMenu">
<li id="navi_shutuba" class="race_navi_shutuba"><a href="../race/shutuba.html?race_id=202205030411&rf=race_submenu" class="Active" title="出馬表"><span class="IconRaceMenu01 IconShutuba"></span>出馬表</a></li>
<li id="navi_odds_view" class="race_navi_odds"><a href="../odds/index.html?race_id=202205030411&rf=race_submenu" title="オッズ・購入" class=""><span class="IconRaceMenu01 IconOdds"></span>オッズ・購入</a></li>
<li id="navi_yoso_mark_list" class="race_navi_yoso"><a href="../yoso/mark_list.html?race_id=202205030411&rf=race_submenu" class="" title="予想"><span class="IconRaceMenu01 IconYoso"></span>予想</a></li>
<li class="race_navi_chokyo"><a href="../race/oikiri.html?race_id=202205030411&rf=race_submenu" class="" title="調教"><span class="IconRaceMenu01 IconTraining"></span>調教</a></li>
<li class="race_navi_comment"><a href="../race/comment.html?race_id=202205030411&rf=race_submenu" class="" title="厩舎コメント"><span class="IconRaceMenu01 IconComment"></span>厩舎コメント</a></li>
<li class="race_navi_data"><a href="../race/data_top.html?race_id=202205030411&rf=race_submenu" class="" title="データ分析"><span class="IconRaceMenu01 IconData"></span>データ分析</a></li>
<li class="race_navi_result"><a href="../race/result.html?race_id=202205030411&rf=race_submenu" class="" title="結果・払戻"><span class="IconRaceMenu01 IconResult"></span>結果・払戻</a></li>
<li class="race_navi_movie"><a href="../race/movie.html?race_id=202205030411&rf=race_submenu" class="" title="レース映像"><span class="IconRaceMenu01 IconMovie"></span>レース映像</a></li>
<li class="race_navi_bbs"><a href="../race/bbs.html?race_id=202205030411&rf=race_submenu" title="掲示板" class="" ><span class="IconRaceMenu01 IconBBS"></span>掲示板</a></li>
</ul>
<div id="AllRaceSubMenu">
<ul class="RaceSubMenu" id="shutuba_submenu">
<li><a href="../race/shutuba.html?race_id=202205030411&rf=shutuba_submenu" class="Active">出走馬</a></li>
<li><a href="../race/newspaper.html?race_id=202205030411&rf=shutuba_submenu" class="">競馬新聞</a></li>
<!-- li><a href="https://yoso.netkeiba.com/senmonshi/jra/yoso_list.html?race_id=202205030411&rf=shutuba_submenu" class="NewFlag">専門紙<span class="icon_new_submenu"></span></a></li -->
<li><a href="https://yoso.netkeiba.com/senmonshi/jra/yoso_list.html?race_id=202205030411&rf=shutuba_submenu">専門紙</a></li>
<li><a href="../race/shutuba_past.html?race_id=202205030411&rf=shutuba_submenu" class="">馬柱(5走)</a></li>
<li><a href="../race/shutuba_past_9.html?race_id=202205030411&rf=shutuba_submenu" target="_blank" class="">馬柱(9走)</a></li>
<li><a href="../race/speed.html?race_id=202205030411&rf=shutuba_submenu" class="">タイム指数</a></li>
<li><a href="../race/holding_time.html?race_id=202205030411&rf=shutuba_submenu" class="">持ちタイム</span></a></li>
<li><a href="../race/paddock.html?race_id=202205030411&rf=shutuba_submenu" class="">パドック速報</a></li>
<li><a href="../race/bias.html?race_id=202205030411&rf=shutuba_submenu" class="">血統</a></li>
<li><a href="../race/match.html?race_id=202205030411&rf=shutuba_submenu" class="">対戦表</a></li>
<li><a href="https://race.sp.netkeiba.com/barometer/score.html?race_id=202205030411&rf=shutuba_submenu">調子偏差値</a></li>
</ul>






</div>
</div><!-- /.RaceMenuArea -->
<script>
function newspaper_link()
{
window.location.href = 'https://rapl.netkeiba.com/race/newspaper.html?race_id=202205030411';
}
</script>
<script type="text/javascript">
function getDataOdds(baken_kind, housiki) {
if (typeof housiki == 'undefined') {
housiki = '';
}
$("#odds_view_result").html('');
if (housiki != '') {
var url = "../odds/odds_get_form.html?type="+baken_kind+"&race_id=202205030411&housiki="+housiki+"&rf=shutuba_submenu";
} else {
var url = "../odds/odds_get_form.html?type="+baken_kind+"&race_id=202205030411&rf=shutuba_submenu";
}
$("[id^=odds_navi_] a").each ( function() { $(this).removeClass("Active"); } )
$.ajax({
type: "GET",
cache: false,
url: url,
data: null,
success: function(data)
{
$('#odds_navi_' + baken_kind + ' a').addClass('Active');
window.history.pushState(null,null, url.replace('odds_get_form','index'));
$("#odds_view_form").empty().append(data);
}
});
}
</script>
<!-- block=shutuba__race_content (cg) -->
<style>
.sort_icon { display:none; }
th {
outline:none;
-webkit-tap-highlight-color: rgba(0,0,0,0);
tap-highlight-color: rgba(0, 0, 0, 0);
-webkit-box-shadow: none;
box-shadow: none;
outline: none;
}
</style>
<script>
$(function(){
//   var ua = window.navigator.userAgent;
//   if(ua.indexOf('Edge') != -1 || ua.indexOf('Trident') != -1 || ua.indexOf('MSIE') != -1) {
//     var style = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.1/css/all.css">';
//     $('head link:last').after(style);
//   } else {
//     // var style ='<style>.sort_icon { padding-right: 18px;position: relative;}.sort_icon::before,.sort_icon::after {border: 4px solid transparent;content: "";display: block;height: 0;right: 5px;top: 70%;position: absolute;width: 0;}.sort_icon::before {border-bottom-color: #66666687;margin-top: -9px;}.sort_icon::after {border-top-color: #66666687;margin-top: 1px;}</style>';
//     $('head link:last').after(style);
//   }
});
</script>
<link rel='stylesheet' href="https://cdn.netkeiba.com/img.racev3/common/css/jquery-ui-1.12.1.css?2019102501" type='text/css'>
<script type="text/javascript" src="https://cdn.netkeiba.com/img.racev3/common/js/jquery-ui-1.12.1.js?2019102501"></script>
<script type="text/javascript">
// $Id: shutuba.html 18964 2018-12-17 10:00:57Z t-kaizuka $
var _action_api_url = 'https://race.netkeiba.com'+'/api/api_post_social_cart.html';
var _action_api_url_myhorse = 'https://race.netkeiba.com'+'/api/api_get_myhorse_entry.html';
var _race_location_url = 'https://race.netkeiba.com';
var _shutuba_cart_group = 'horse_202205030411';
var _shutuba_race_id = '202205030411';
var _race_cookie_domain_ = '.netkeiba.com';
</script>
<script type="text/javascript" src="https://cdn.netkeiba.com/img.racev3/common/js/social_cart.js?2019073001"></script>
<script type="text/javascript" src="https://cdn.netkeiba.com/img.racev3/common/js/race/shutuba.js?2020061101"></script>
<script type="text/javascript" src="https://cdn.netkeiba.com/img.racev3/common/js/race/api_myhorse.action.js?2019073001"></script>
<script type="text/javascript" src="https://cdn.netkeiba.com/img.racev3/common/js/jquery.odds_update.js?2019073001"></script>
<script type="text/javascript" src="https://cdn.netkeiba.com/img.racev3/common/js/ndcommon.min.js?2019073001"></script>
<script type="text/javascript" src="https://cdn.netkeiba.com/img.racev3/common/js/zlib.min.js?2019073001"></script>
<script type="text/javascript" src="https://cdn.netkeiba.com/img.racev3/common/js/jquery.tablesorter.js?2019103101"></script>
<div class="RaceTableArea">
<table class="Shutuba_Table RaceTable01 ShutubaTable">
<thead>
<tr class="Header">
<th rowspan="2" class="Waku">枠</th>
<th rowspan="2" class="Umaban sort_common"><div class="Inner_Shutuba">馬<br>番<span class="sort_icon"></span></div></th>
<th rowspan="2" class="CheckMark">印
<div class="ChangeMarkBtn">

<div class="BtnInput BtnInputTick">
<input type="button" value="切替" class="BtnInputLabel" onclick="change_mark_mode('shutuba','202205030411', _race_cookie_domain_);">
</div>
</div><!-- /.ChangeMarkBtn -->
</th>
<th rowspan="2" class="HorseInfo sort_common " id="sort_cell_name">
<div class="Inner_Shutuba">
<span class="HorseName">馬名</span><span class="sort_icon"></span>
</div>
</th>
<th rowspan="2" class="Barei">性齢</th>
<th rowspan="2" class="Dredging sort_common "><div class="Inner_Shutuba">斤量<span class="sort_icon"></span></div></th>
<th rowspan="2" class="Jockey">騎手</th>
<th rowspan="2" class="Trainer">厩舎</th>
<th rowspan="2" class="Weight sort_common " id="sort_cell_weight"><div class="Inner_Shutuba">馬体重<br/><small>(増減)</small><span class="sort_icon"></span></div></th>
<th rowspan="2" class="Popular" id="sort_cell_odds">
<div id="odds_update_info" class="Tooltip_OddsUpLimit_Wrap">
<span id="odds_title"></span>
<button type="button" id="act-manual_update" class="BtnInputLabel OddsUpdataBtn LiveOddsUpdate" style="display:none">
<span class="OddsUpLimitTxt01">更新</span>
</button>
</div></th>
<th rowspan="2" class="Popular Popular_Ninki Txt_C sort_common " id="sort_cell_ninki"><div class="Inner_Shutuba">人気<span class="sort_icon"></span></div></th>
<th colspan="2" class="FavHorse"><a href="https://db.netkeiba.com/bookmark/horse_bookmark_list.html">お気に入り馬</a></th>
</tr>
<tr class="Header FavHorseSub">
<th class="FavRegist">登録</th>
<th class="Memo">メモ</th>
</tr>
</thead>
<tr class="HorseList" id="tr_4">
<td class="Waku1 Txt_C"><span>1</span></td>
<td class="Umaban1 Txt_C">1</td>
<td class="CheckMark Horse_Select">

<select class="makeMeFancy_4" name="4" id="mark_4" style="display: none;">
<option data-html-text="--" value="1_0">--</option><option data-html-text="◎" value="1_1">◎</option><option data-html-text="◯" value="1_2">◯</option><option data-html-text="▲" value="1_3">▲</option><option data-html-text="△" value="1_4">△</option><option data-html-text="☆" value="1_5">☆</option><option data-html-text="&amp;#10003" value="1_98">&amp;#10003</option><option data-html-text="消" value="1_99">消</option>
</select>
</td>
<td class="HorseInfo">
<div>
<div>
 <span class="HorseName"><a href="https://db.netkeiba.com/horse/2016104791" target="_blank" title="シャドウディーヴァ">シャドウディーヴァ<img id="myhorse_2016104791" class="disp_none Favorite" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/icon_horse.png?2019073001" alt="" width="18"></a></span>
</div>
</div>
</td>
<td class="Barei Txt_C">牝6</td>
<td class="Txt_C">56.0</td>
<td class="Jockey">
<a  href="https://db.netkeiba.com/jockey/result/recent/01163/" target="_blank" title="坂井">坂井</a>


</td>
<td class="Trainer"><span class="Label1">美浦</span><a href="https://db.netkeiba.com/trainer/result/recent/01086/" target="_blank" title="斎藤誠">斎藤誠</a></td>
<td class="Weight">
486<small>(+4)</small>
</td>
<td class="Txt_R Popular"><span id="odds-1_01" style="font-weight : bold">---.-</span></td>
<td class="Popular Popular_Ninki Txt_C">
<span id="ninki-1_01">**</span>
</td>
<td class="FavRegist Txt_C">
<a href="../popup/horse_bookmark.html?ketto_num=2016104791&race_id=202205030411" title="お気に入り馬登録" class="popup_link_04 cboxElement ">
<img src="https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001" class="horsebookmark myhorse1_2016104791" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'">
<img id="myhorse1_2016104791" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png" width="20" height="20"  class="disp_none horsebookmark myhorse_2016104791" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'">
</a> </td>
<td class="FavMemo"><div><a href="../popup/horse_bookmark.html?ketto_num=2016104791&race_id=202205030411" id="Bamei_2016104791" title="" class="popup_link_04 cboxElement"></a></div></td>
</tr>
<tr class="HorseList" id="tr_9">
<td class="Waku2 Txt_C"><span>2</span></td>
<td class="Umaban2 Txt_C">2</td>
<td class="CheckMark Horse_Select">

<select class="makeMeFancy_9" name="9" id="mark_9" style="display: none;">
<option data-html-text="--" value="2_0">--</option><option data-html-text="◎" value="2_1">◎</option><option data-html-text="◯" value="2_2">◯</option><option data-html-text="▲" value="2_3">▲</option><option data-html-text="△" value="2_4">△</option><option data-html-text="☆" value="2_5">☆</option><option data-html-text="&amp;#10003" value="2_98">&amp;#10003</option><option data-html-text="消" value="2_99">消</option>
</select>
</td>
<td class="HorseInfo">
<div>
<div>
 <span class="HorseName"><a href="https://db.netkeiba.com/horse/2018100184" target="_blank" title="タイムトゥヘヴン">タイムトゥヘヴン<img id="myhorse_2018100184" class="disp_none Favorite" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/icon_horse.png?2019073001" alt="" width="18"></a></span>
</div>
</div>
</td>
<td class="Barei Txt_C">牡4</td>
<td class="Txt_C">56.0</td>
<td class="Jockey">
<a  href="https://db.netkeiba.com/jockey/result/recent/05386/" target="_blank" title="戸崎圭">戸崎圭</a>


</td>
<td class="Trainer"><span class="Label1">美浦</span><a href="https://db.netkeiba.com/trainer/result/recent/01054/" target="_blank" title="戸田">戸田</a></td>
<td class="Weight">
484<small>(+6)</small>
</td>
<td class="Txt_R Popular"><span id="odds-1_02" style="font-weight : bold">---.-</span></td>
<td class="Popular Popular_Ninki Txt_C">
<span id="ninki-1_02">**</span>
</td>
<td class="FavRegist Txt_C">
<a href="../popup/horse_bookmark.html?ketto_num=2018100184&race_id=202205030411" title="お気に入り馬登録" class="popup_link_04 cboxElement ">
<img src="https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001" class="horsebookmark myhorse1_2018100184" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'">
<img id="myhorse1_2018100184" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png" width="20" height="20"  class="disp_none horsebookmark myhorse_2018100184" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'">
</a> </td>
<td class="FavMemo"><div><a href="../popup/horse_bookmark.html?ketto_num=2018100184&race_id=202205030411" id="Bamei_2018100184" title="" class="popup_link_04 cboxElement"></a></div></td>
</tr>
<tr class="HorseList" id="tr_6">
<td class="Waku3 Txt_C"><span>3</span></td>
<td class="Umaban3 Txt_C">3</td>
<td class="CheckMark Horse_Select">

<select class="makeMeFancy_6" name="6" id="mark_6" style="display: none;">
<option data-html-text="--" value="3_0">--</option><option data-html-text="◎" value="3_1">◎</option><option data-html-text="◯" value="3_2">◯</option><option data-html-text="▲" value="3_3">▲</option><option data-html-text="△" value="3_4">△</option><option data-html-text="☆" value="3_5">☆</option><option data-html-text="&amp;#10003" value="3_98">&amp;#10003</option><option data-html-text="消" value="3_99">消</option>
</select>
</td>
<td class="HorseInfo">
<div>
<div>
 <span class="HorseName"><a href="https://db.netkeiba.com/horse/2017101805" target="_blank" title="コルテジア">コルテジア<img id="myhorse_2017101805" class="disp_none Favorite" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/icon_horse.png?2019073001" alt="" width="18"></a></span>
</div>
</div>
</td>
<td class="Barei Txt_C">牡5</td>
<td class="Txt_C">56.0</td>
<td class="Jockey">
<a  href="https://db.netkeiba.com/jockey/result/recent/01122/" target="_blank" title="三浦">三浦</a>


</td>
<td class="Trainer"><span class="Label2">栗東</span><a href="https://db.netkeiba.com/trainer/result/recent/01111/" target="_blank" title="鈴木孝">鈴木孝</a></td>
<td class="Weight">
464<small>(+6)</small>
</td>
<td class="Txt_R Popular"><span id="odds-1_03" style="font-weight : bold">---.-</span></td>
<td class="Popular Popular_Ninki Txt_C">
<span id="ninki-1_03">**</span>
</td>
<td class="FavRegist Txt_C">
<a href="../popup/horse_bookmark.html?ketto_num=2017101805&race_id=202205030411" title="お気に入り馬登録" class="popup_link_04 cboxElement ">
<img src="https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001" class="horsebookmark myhorse1_2017101805" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'">
<img id="myhorse1_2017101805" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png" width="20" height="20"  class="disp_none horsebookmark myhorse_2017101805" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'">
</a> </td>
<td class="FavMemo"><div><a href="../popup/horse_bookmark.html?ketto_num=2017101805&race_id=202205030411" id="Bamei_2017101805" title="" class="popup_link_04 cboxElement"></a></div></td>
</tr>
<tr class="HorseList" id="tr_10">
<td class="Waku4 Txt_C"><span>4</span></td>
<td class="Umaban4 Txt_C">4</td>
<td class="CheckMark Horse_Select">

<select class="makeMeFancy_10" name="10" id="mark_10" style="display: none;">
<option data-html-text="--" value="4_0">--</option><option data-html-text="◎" value="4_1">◎</option><option data-html-text="◯" value="4_2">◯</option><option data-html-text="▲" value="4_3">▲</option><option data-html-text="△" value="4_4">△</option><option data-html-text="☆" value="4_5">☆</option><option data-html-text="&amp;#10003" value="4_98">&amp;#10003</option><option data-html-text="消" value="4_99">消</option>
</select>
</td>
<td class="HorseInfo">
<div>
<div>
 <span class="HorseName"><a href="https://db.netkeiba.com/horse/2018102020" target="_blank" title="ヤマニンサンパ">ヤマニンサンパ<img id="myhorse_2018102020" class="disp_none Favorite" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/icon_horse.png?2019073001" alt="" width="18"></a></span>
</div>
</div>
</td>
<td class="Barei Txt_C">牡4</td>
<td class="Txt_C">56.0</td>
<td class="Jockey">
<a  href="https://db.netkeiba.com/jockey/result/recent/01088/" target="_blank" title="川田">川田</a>


</td>
<td class="Trainer"><span class="Label2">栗東</span><a href="https://db.netkeiba.com/trainer/result/recent/01151/" target="_blank" title="斉藤崇">斉藤崇</a></td>
<td class="Weight">
472<small>(0)</small>
</td>
<td class="Txt_R Popular"><span id="odds-1_04" style="font-weight : bold">---.-</span></td>
<td class="Popular Popular_Ninki Txt_C">
<span id="ninki-1_04">**</span>
</td>
<td class="FavRegist Txt_C">
<a href="../popup/horse_bookmark.html?ketto_num=2018102020&race_id=202205030411" title="お気に入り馬登録" class="popup_link_04 cboxElement ">
<img src="https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001" class="horsebookmark myhorse1_2018102020" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'">
<img id="myhorse1_2018102020" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png" width="20" height="20"  class="disp_none horsebookmark myhorse_2018102020" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'">
</a> </td>
<td class="FavMemo"><div><a href="../popup/horse_bookmark.html?ketto_num=2018102020&race_id=202205030411" id="Bamei_2018102020" title="" class="popup_link_04 cboxElement"></a></div></td>
</tr>
<tr class="HorseList" id="tr_8">
<td class="Waku5 Txt_C"><span>5</span></td>
<td class="Umaban5 Txt_C">5</td>
<td class="CheckMark Horse_Select">

<select class="makeMeFancy_8" name="8" id="mark_8" style="display: none;">
<option data-html-text="--" value="5_0">--</option><option data-html-text="◎" value="5_1">◎</option><option data-html-text="◯" value="5_2">◯</option><option data-html-text="▲" value="5_3">▲</option><option data-html-text="△" value="5_4">△</option><option data-html-text="☆" value="5_5">☆</option><option data-html-text="&amp;#10003" value="5_98">&amp;#10003</option><option data-html-text="消" value="5_99">消</option>
</select>
</td>
<td class="HorseInfo">
<div>
<div>
<span class="Icon_HorseMark Icon_MaruGai"></span><span class="HorseName"><a href="https://db.netkeiba.com/horse/2017110026" target="_blank" title="ダーリントンホール">ダーリントンホール<img id="myhorse_2017110026" class="disp_none Favorite" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/icon_horse.png?2019073001" alt="" width="18"></a></span>
</div>
</div>
</td>
<td class="Barei Txt_C">牡5</td>
<td class="Txt_C">56.0</td>
<td class="Jockey">
<a  href="https://db.netkeiba.com/jockey/result/recent/05339/" target="_blank" title="ルメール">ルメール</a>


</td>
<td class="Trainer"><span class="Label1">美浦</span><a href="https://db.netkeiba.com/trainer/result/recent/01126/" target="_blank" title="木村">木村</a></td>
<td class="Weight">
536<small>(-8)</small>
</td>
<td class="Txt_R Popular"><span id="odds-1_05" style="font-weight : bold">---.-</span></td>
<td class="Popular Popular_Ninki Txt_C">
<span id="ninki-1_05">**</span>
</td>
<td class="FavRegist Txt_C">
<a href="../popup/horse_bookmark.html?ketto_num=2017110026&race_id=202205030411" title="お気に入り馬登録" class="popup_link_04 cboxElement ">
<img src="https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001" class="horsebookmark myhorse1_2017110026" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'">
<img id="myhorse1_2017110026" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png" width="20" height="20"  class="disp_none horsebookmark myhorse_2017110026" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'">
</a> </td>
<td class="FavMemo"><div><a href="../popup/horse_bookmark.html?ketto_num=2017110026&race_id=202205030411" id="Bamei_2017110026" title="" class="popup_link_04 cboxElement"></a></div></td>
</tr>
<tr class="HorseList" id="tr_11">
<td class="Waku5 Txt_C"><span>5</span></td>
<td class="Umaban5 Txt_C">6</td>
<td class="CheckMark Horse_Select">

<select class="makeMeFancy_11" name="11" id="mark_11" style="display: none;">
<option data-html-text="--" value="6_0">--</option><option data-html-text="◎" value="6_1">◎</option><option data-html-text="◯" value="6_2">◯</option><option data-html-text="▲" value="6_3">▲</option><option data-html-text="△" value="6_4">△</option><option data-html-text="☆" value="6_5">☆</option><option data-html-text="&amp;#10003" value="6_98">&amp;#10003</option><option data-html-text="消" value="6_99">消</option>
</select>
</td>
<td class="HorseInfo">
<div>
<div>
 <span class="HorseName"><a href="https://db.netkeiba.com/horse/2018102348" target="_blank" title="ノースブリッジ">ノースブリッジ<img id="myhorse_2018102348" class="disp_none Favorite" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/icon_horse.png?2019073001" alt="" width="18"></a></span>
</div>
</div>
</td>
<td class="Barei Txt_C">牡4</td>
<td class="Txt_C">56.0</td>
<td class="Jockey">
<a  href="https://db.netkeiba.com/jockey/result/recent/05203/" target="_blank" title="岩田康">岩田康</a>


</td>
<td class="Trainer"><span class="Label1">美浦</span><a href="https://db.netkeiba.com/trainer/result/recent/01145/" target="_blank" title="奥村武">奥村武</a></td>
<td class="Weight">
492<small>(-4)</small>
</td>
<td class="Txt_R Popular"><span id="odds-1_06" style="font-weight : bold">---.-</span></td>
<td class="Popular Popular_Ninki Txt_C">
<span id="ninki-1_06">**</span>
</td>
<td class="FavRegist Txt_C">
<a href="../popup/horse_bookmark.html?ketto_num=2018102348&race_id=202205030411" title="お気に入り馬登録" class="popup_link_04 cboxElement ">
<img src="https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001" class="horsebookmark myhorse1_2018102348" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'">
<img id="myhorse1_2018102348" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png" width="20" height="20"  class="disp_none horsebookmark myhorse_2018102348" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'">
</a> </td>
<td class="FavMemo"><div><a href="../popup/horse_bookmark.html?ketto_num=2018102348&race_id=202205030411" id="Bamei_2018102348" title="" class="popup_link_04 cboxElement"></a></div></td>
</tr>
<tr class="HorseList" id="tr_2">
<td class="Waku6 Txt_C"><span>6</span></td>
<td class="Umaban6 Txt_C">7</td>
<td class="CheckMark Horse_Select">

<select class="makeMeFancy_2" name="2" id="mark_2" style="display: none;">
<option data-html-text="--" value="7_0">--</option><option data-html-text="◎" value="7_1">◎</option><option data-html-text="◯" value="7_2">◯</option><option data-html-text="▲" value="7_3">▲</option><option data-html-text="△" value="7_4">△</option><option data-html-text="☆" value="7_5">☆</option><option data-html-text="&amp;#10003" value="7_98">&amp;#10003</option><option data-html-text="消" value="7_99">消</option>
</select>
</td>
<td class="HorseInfo">
<div>
<div>
 <span class="HorseName"><a href="https://db.netkeiba.com/horse/2016103815" target="_blank" title="トーセングラン">トーセングラン<img id="myhorse_2016103815" class="disp_none Favorite" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/icon_horse.png?2019073001" alt="" width="18"></a></span>
</div>
</div>
</td>
<td class="Barei Txt_C">牡6</td>
<td class="Txt_C">56.0</td>
<td class="Jockey">
<a  href="https://db.netkeiba.com/jockey/result/recent/01075/" target="_blank" title="田辺">田辺</a>


</td>
<td class="Trainer"><span class="Label1">美浦</span><a href="https://db.netkeiba.com/trainer/result/recent/01027/" target="_blank" title="田村">田村</a></td>
<td class="Weight">
442<small>(-6)</small>
</td>
<td class="Txt_R Popular"><span id="odds-1_07" style="font-weight : bold">---.-</span></td>
<td class="Popular Popular_Ninki Txt_C">
<span id="ninki-1_07">**</span>
</td>
<td class="FavRegist Txt_C">
<a href="../popup/horse_bookmark.html?ketto_num=2016103815&race_id=202205030411" title="お気に入り馬登録" class="popup_link_04 cboxElement ">
<img src="https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001" class="horsebookmark myhorse1_2016103815" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'">
<img id="myhorse1_2016103815" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png" width="20" height="20"  class="disp_none horsebookmark myhorse_2016103815" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'">
</a> </td>
<td class="FavMemo"><div><a href="../popup/horse_bookmark.html?ketto_num=2016103815&race_id=202205030411" id="Bamei_2016103815" title="" class="popup_link_04 cboxElement"></a></div></td>
</tr>
<tr class="HorseList" id="tr_7">
<td class="Waku6 Txt_C"><span>6</span></td>
<td class="Umaban6 Txt_C">8</td>
<td class="CheckMark Horse_Select">

<select class="makeMeFancy_7" name="7" id="mark_7" style="display: none;">
<option data-html-text="--" value="8_0">--</option><option data-html-text="◎" value="8_1">◎</option><option data-html-text="◯" value="8_2">◯</option><option data-html-text="▲" value="8_3">▲</option><option data-html-text="△" value="8_4">△</option><option data-html-text="☆" value="8_5">☆</option><option data-html-text="&amp;#10003" value="8_98">&amp;#10003</option><option data-html-text="消" value="8_99">消</option>
</select>
</td>
<td class="HorseInfo">
<div>
<div>
 <span class="HorseName"><a href="https://db.netkeiba.com/horse/2017102833" target="_blank" title="ガロアクリーク">ガロアクリーク<img id="myhorse_2017102833" class="disp_none Favorite" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/icon_horse.png?2019073001" alt="" width="18"></a></span>
</div>
</div>
</td>
<td class="Barei Txt_C">牡5</td>
<td class="Txt_C">56.0</td>
<td class="Jockey">
<a  href="https://db.netkeiba.com/jockey/result/recent/01077/" target="_blank" title="石橋脩">石橋脩</a>


</td>
<td class="Trainer"><span class="Label1">美浦</span><a href="https://db.netkeiba.com/trainer/result/recent/00423/" target="_blank" title="上原博">上原博</a></td>
<td class="Weight">
510<small>(-2)</small>
</td>
<td class="Txt_R Popular"><span id="odds-1_08" style="font-weight : bold">---.-</span></td>
<td class="Popular Popular_Ninki Txt_C">
<span id="ninki-1_08">**</span>
</td>
<td class="FavRegist Txt_C">
<a href="../popup/horse_bookmark.html?ketto_num=2017102833&race_id=202205030411" title="お気に入り馬登録" class="popup_link_04 cboxElement ">
<img src="https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001" class="horsebookmark myhorse1_2017102833" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'">
<img id="myhorse1_2017102833" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png" width="20" height="20"  class="disp_none horsebookmark myhorse_2017102833" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'">
</a> </td>
<td class="FavMemo"><div><a href="../popup/horse_bookmark.html?ketto_num=2017102833&race_id=202205030411" id="Bamei_2017102833" title="" class="popup_link_04 cboxElement"></a></div></td>
</tr>
<tr class="HorseList" id="tr_1">
<td class="Waku7 Txt_C"><span>7</span></td>
<td class="Umaban7 Txt_C">9</td>
<td class="CheckMark Horse_Select">

<select class="makeMeFancy_1" name="1" id="mark_1" style="display: none;">
<option data-html-text="--" value="9_0">--</option><option data-html-text="◎" value="9_1">◎</option><option data-html-text="◯" value="9_2">◯</option><option data-html-text="▲" value="9_3">▲</option><option data-html-text="△" value="9_4">△</option><option data-html-text="☆" value="9_5">☆</option><option data-html-text="&amp;#10003" value="9_98">&amp;#10003</option><option data-html-text="消" value="9_99">消</option>
</select>
</td>
<td class="HorseInfo">
<div>
<div>
 <span class="HorseName"><a href="https://db.netkeiba.com/horse/2016102692" target="_blank" title="ハッピーアワー">ハッピーアワー<img id="myhorse_2016102692" class="disp_none Favorite" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/icon_horse.png?2019073001" alt="" width="18"></a></span>
</div>
</div>
</td>
<td class="Barei Txt_C">牡6</td>
<td class="Txt_C">56.0</td>
<td class="Jockey">
<a  href="https://db.netkeiba.com/jockey/result/recent/01142/" target="_blank" title="長岡">長岡</a>


</td>
<td class="Trainer"><span class="Label2">栗東</span><a href="https://db.netkeiba.com/trainer/result/recent/01178/" target="_blank" title="杉山佳">杉山佳</a></td>
<td class="Weight">
448<small>(-2)</small>
</td>
<td class="Txt_R Popular"><span id="odds-1_09" style="font-weight : bold">---.-</span></td>
<td class="Popular Popular_Ninki Txt_C">
<span id="ninki-1_09">**</span>
</td>
<td class="FavRegist Txt_C">
<a href="../popup/horse_bookmark.html?ketto_num=2016102692&race_id=202205030411" title="お気に入り馬登録" class="popup_link_04 cboxElement ">
<img src="https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001" class="horsebookmark myhorse1_2016102692" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'">
<img id="myhorse1_2016102692" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png" width="20" height="20"  class="disp_none horsebookmark myhorse_2016102692" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'">
</a> </td>
<td class="FavMemo"><div><a href="../popup/horse_bookmark.html?ketto_num=2016102692&race_id=202205030411" id="Bamei_2016102692" title="" class="popup_link_04 cboxElement"></a></div></td>
</tr>
<tr class="HorseList" id="tr_5">
<td class="Waku7 Txt_C"><span>7</span></td>
<td class="Umaban7 Txt_C">10</td>
<td class="CheckMark Horse_Select">

<select class="makeMeFancy_5" name="5" id="mark_5" style="display: none;">
<option data-html-text="--" value="10_0">--</option><option data-html-text="◎" value="10_1">◎</option><option data-html-text="◯" value="10_2">◯</option><option data-html-text="▲" value="10_3">▲</option><option data-html-text="△" value="10_4">△</option><option data-html-text="☆" value="10_5">☆</option><option data-html-text="&amp;#10003" value="10_98">&amp;#10003</option><option data-html-text="消" value="10_99">消</option>
</select>
</td>
<td class="HorseInfo">
<div>
<div>
 <span class="HorseName"><a href="https://db.netkeiba.com/horse/2016106518" target="_blank" title="トーラスジェミニ">トーラスジェミニ<img id="myhorse_2016106518" class="disp_none Favorite" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/icon_horse.png?2019073001" alt="" width="18"></a></span>
</div>
</div>
</td>
<td class="Barei Txt_C">牡6</td>
<td class="Txt_C">58.0</td>
<td class="Jockey">
<a  href="https://db.netkeiba.com/jockey/result/recent/01184/" target="_blank" title="原">原</a>


</td>
<td class="Trainer"><span class="Label1">美浦</span><a href="https://db.netkeiba.com/trainer/result/recent/01005/" target="_blank" title="小桧山">小桧山</a></td>
<td class="Weight">
464<small>(-4)</small>
</td>
<td class="Txt_R Popular"><span id="odds-1_10" style="font-weight : bold">---.-</span></td>
<td class="Popular Popular_Ninki Txt_C">
<span id="ninki-1_10">**</span>
</td>
<td class="FavRegist Txt_C">
<a href="../popup/horse_bookmark.html?ketto_num=2016106518&race_id=202205030411" title="お気に入り馬登録" class="popup_link_04 cboxElement ">
<img src="https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001" class="horsebookmark myhorse1_2016106518" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'">
<img id="myhorse1_2016106518" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png" width="20" height="20"  class="disp_none horsebookmark myhorse_2016106518" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'">
</a> </td>
<td class="FavMemo"><div><a href="../popup/horse_bookmark.html?ketto_num=2016106518&race_id=202205030411" id="Bamei_2016106518" title="" class="popup_link_04 cboxElement"></a></div></td>
</tr>
<tr class="HorseList" id="tr_12">
<td class="Waku8 Txt_C"><span>8</span></td>
<td class="Umaban8 Txt_C">11</td>
<td class="CheckMark Horse_Select">

<select class="makeMeFancy_12" name="12" id="mark_12" style="display: none;">
<option data-html-text="--" value="11_0">--</option><option data-html-text="◎" value="11_1">◎</option><option data-html-text="◯" value="11_2">◯</option><option data-html-text="▲" value="11_3">▲</option><option data-html-text="△" value="11_4">△</option><option data-html-text="☆" value="11_5">☆</option><option data-html-text="&amp;#10003" value="11_98">&amp;#10003</option><option data-html-text="消" value="11_99">消</option>
</select>
</td>
<td class="HorseInfo">
<div>
<div>
 <span class="HorseName"><a href="https://db.netkeiba.com/horse/2018104576" target="_blank" title="ジャスティンカフェ">ジャスティンカフェ<img id="myhorse_2018104576" class="disp_none Favorite" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/icon_horse.png?2019073001" alt="" width="18"></a></span>
</div>
</div>
</td>
<td class="Barei Txt_C">牡4</td>
<td class="Txt_C">56.0</td>
<td class="Jockey">
<a  href="https://db.netkeiba.com/jockey/result/recent/00660/" target="_blank" title="横山典">横山典</a>


</td>
<td class="Trainer"><span class="Label2">栗東</span><a href="https://db.netkeiba.com/trainer/result/recent/01164/" target="_blank" title="安田翔">安田翔</a></td>
<td class="Weight">
490<small>(0)</small>
</td>
<td class="Txt_R Popular"><span id="odds-1_11" style="font-weight : bold">---.-</span></td>
<td class="Popular Popular_Ninki Txt_C">
<span id="ninki-1_11">**</span>
</td>
<td class="FavRegist Txt_C">
<a href="../popup/horse_bookmark.html?ketto_num=2018104576&race_id=202205030411" title="お気に入り馬登録" class="popup_link_04 cboxElement ">
<img src="https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001" class="horsebookmark myhorse1_2018104576" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'">
<img id="myhorse1_2018104576" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png" width="20" height="20"  class="disp_none horsebookmark myhorse_2018104576" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'">
</a> </td>
<td class="FavMemo"><div><a href="../popup/horse_bookmark.html?ketto_num=2018104576&race_id=202205030411" id="Bamei_2018104576" title="" class="popup_link_04 cboxElement"></a></div></td>
</tr>
<tr class="HorseList" id="tr_3">
<td class="Waku8 Txt_C"><span>8</span></td>
<td class="Umaban8 Txt_C">12</td>
<td class="CheckMark Horse_Select">

<select class="makeMeFancy_3" name="3" id="mark_3" style="display: none;">
<option data-html-text="--" value="12_0">--</option><option data-html-text="◎" value="12_1">◎</option><option data-html-text="◯" value="12_2">◯</option><option data-html-text="▲" value="12_3">▲</option><option data-html-text="△" value="12_4">△</option><option data-html-text="☆" value="12_5">☆</option><option data-html-text="&amp;#10003" value="12_98">&amp;#10003</option><option data-html-text="消" value="12_99">消</option>
</select>
</td>
<td class="HorseInfo">
<div>
<div>
 <span class="HorseName"><a href="https://db.netkeiba.com/horse/2016104772" target="_blank" title="ザダル">ザダル<img id="myhorse_2016104772" class="disp_none Favorite" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/icon_horse.png?2019073001" alt="" width="18"></a></span>
</div>
</div>
</td>
<td class="Barei Txt_C">牡6</td>
<td class="Txt_C">58.0</td>
<td class="Jockey">
<a  href="https://db.netkeiba.com/jockey/result/recent/05585/" target="_blank" title="レーン">レーン</a>


</td>
<td class="Trainer"><span class="Label1">美浦</span><a href="https://db.netkeiba.com/trainer/result/recent/01102/" target="_blank" title="大竹">大竹</a></td>
<td class="Weight">
504<small>(0)</small>
</td>
<td class="Txt_R Popular"><span id="odds-1_12" style="font-weight : bold">---.-</span></td>
<td class="Popular Popular_Ninki Txt_C">
<span id="ninki-1_12">**</span>
</td>
<td class="FavRegist Txt_C">
<a href="../popup/horse_bookmark.html?ketto_num=2016104772&race_id=202205030411" title="お気に入り馬登録" class="popup_link_04 cboxElement ">
<img src="https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001" class="horsebookmark myhorse1_2016104772" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/prof_icon_favhorse_comp_01.png?2019073001'">
<img id="myhorse1_2016104772" src="https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png" width="20" height="20"  class="disp_none horsebookmark myhorse_2016104772" onmouseover="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'" onmouseout="this.src='https://cdn.netkeiba.com/img.racev3/common/img/icon/horse_favorite_icon_pc.png'">
</a> </td>
<td class="FavMemo"><div><a href="../popup/horse_bookmark.html?ketto_num=2016104772&race_id=202205030411" id="Bamei_2016104772" title="" class="popup_link_04 cboxElement"></a></div></td>
</tr>

</tbody>
</table>
<div class="ShutubaTableFormWrap clearfix">
<!-- オッズ -->
<form id="shutuba_form" method="get" action="" class="Contents_Box">

<input type="hidden" name="race_id" value="202205030411">
<div class="Shutuba_Form_Footer Phase01_Btn">
<button class="SubmitBtn" type="submit"><span class="Icon_Sprite_Nk Icon_RaceInfo32_3"></span>選んだ馬のオッズを見る</button>
</div>
</form><!-- /.shutuba_form -->
<style>
.apl_conductor {
}
.apl_conductor a{
display: block;
margin:auto;
}
.apl_conductor a img {
display: block;
max-width: 100%;
margin:auto;
}
</style>
<div class="apl_conductor">
<script language="JavaScript" type="text/javascript">
noCacheParam=Math.random()*10000000000;document.write('<scr'+'ipt type="text/javascript" src="https://netdreamersad.durasite.net/A-affiliate2/mobile?site=23&keyword=nd_contents_race&isJS=true&encoding=EUC-JP&ord=' + noCacheParam + '"></scr'+'ipt>');
</script>
</div>
<div class="OnOffArea OddsAutoCheck ToggleCheck LiveOddsUpdate" style="display:none">
<label class="OddsAutoCheckLabel">
<span class="OddsAutoTxt">オッズの自動更新をONにする(最終更新 <span id="official_time"></span>)</span>
<input type="checkbox" id="act-auto_update">
<span class="CheckLabelTxt"></span>
</label>
</div><!-- /.OddsAutoCheck ToggleCheck -->
</div>
<div style="display:none;" id="free_odds_limit_overlay"></div>
<script type="text/javascript">
$(function(){
//tablesorterの不具合のため、馬番がNULLの場合に馬名のソートの振る舞いを変更する
$("tbody .HorseInfo").each( function() {
var rowIndex = $(this).parent().index();
if ($("tbody [class^=Umaban]").eq(rowIndex).text() == "") {
$(this).attr("data-sort-value", rowIndex+1);
}
});
// オッズ更新click
$(".OddsUpdataBtn").on({"click":
function(){
$(".OddsUpdataBtn").removeClass("OddsUpdataClick");
$(".OddsUpdataBtn").addClass("OddsUpdataClick");
}
});
});
</script>
<script>
"use strict"
$(function(){
/* Area created in the intern Start */
const nullCheak = function(date){ return !date[0] ? true : false };
var firstTime = true;
const table_sorte = function(t_header_flg){
$('.Shutuba_Table th').unbind();
$.tablesorter.destroy( $('.Shutuba_Table'), true, function(table) {});
$('.Shutuba_Table').tablesorter({
headers: {
0: { sorter: "false" },
1: { sorter: t_header_flg[1] },
2: { sorter: "false" },
3: { sorter: "text" },
4: { sorter: "false" },
5: { sorter: t_header_flg[5]  },
6: { sorter: "false" },
7: { sorter: "false" },
8: { sorter: t_header_flg[8]  },
9: { sorter: "false" },
10: { sorter: t_header_flg[10] },
11: { sorter: "false" },
12: { sorter: "false" },
13: { sorter: "false" },
},
//tablesorterの不具合のため、馬番がNULLの場合に馬名のソートの振る舞いを変更する
textExtraction: function(node) {
var attr = $(node).attr('data-sort-value');
if (typeof attr !== 'undefined' && attr !== false) {
return attr;
}
return $(node).text();
}
});
};
// $(window).load(function(){
var tableSorteAction = function() {
const Umaban = $('td.Umaban');
const weight = $('td.Weight small');
const t_header_icons = $('.sort_icon');
// sort flag [0:枠,1:印,2:名,3:オッズ,4:体重]
var t_sorts_flg = [true,true,true,true,true,true,true,true, true, true, true, false ];
// sort Icon generation
const icon = $('<i></i>',{
'class' : 'fas fa-sort',
});
t_header_icons.append(icon);
// Empty check in frame order
if($('td').hasClass('Umaban')){
t_header_icons[0].remove();
t_sorts_flg[1] = false;
}
// Empty check of horse weight
if(!weight.length){
t_header_icons[3].remove();
// t_sorts_flg[3] = false;
t_sorts_flg[8] = false;
}
table_sorte(t_sorts_flg);
$('.sort_icon').css("display", "block");
$('.sort_icon').show();
};
/* Area created in the intern End */
$.oddsUpdate({
apiUrl:'https://race.netkeiba.com/api/api_get_jra_odds.html',
raceId:'202205030411',
isPremium:0,
displayDiffTime:false,
PremiumLinkReturnUrl : 'http%3A%2F%2Frace.netkeiba.com%2Frace%2Fshutuba.html%3Frace_id%3D202205030411',
PremiumLinkReturnRf : 'shutuba',
isBrackets : false,
compress:true,
callbackApiComplete:function(_this,_odds_status,_data){
// オッズ見出し
if(_odds_status=='yoso'){
$('#odds_title').html('予想<br />オッズ');
} else if(_odds_status=='result'){
$('#odds_title').html('オッズ');
} else if(_odds_status=='middle') {
$('#premium_guide').show();
$('#odds_title').html('オッズ');
} else {
$('#odds_title').html('オッズ');
}
// マイオッズ遷移先
var action = 'https://race.netkeiba.com';
var action_form_pid = '../odds/myodds';
if(_odds_status=='yoso'){
action = '';
action_form_pid = '../odds/index';
}
$('#shutuba_form').attr('action',action_form_pid+".html");
// オッズ着色
$('[id^="odds-1_"]').each(function(){
var data_key = $(this).prop('id').replace('odds-','').split('_');
var type = data_key[0];
var no = data_key[1];
if (_data) {
if(!$.isEmptyObject(_data['odds'][type])){
var ary_row = _data['odds'][type];
var row = ary_row[no];
if (row) {
$(this).text(row[0]);
if(type==1){
$(this).parent().parent().find(".Popular_Ninki")
.removeClass("BgYellow")
.removeClass("BgBlue02")
.removeClass("BgOrange");
if (row[2] == 1) {
$(this).parent().parent().find(".Popular_Ninki").addClass("BgYellow")
} else if (row[2] ==2) {
$(this).parent().parent().find(".Popular_Ninki").addClass("BgBlue02")
} else if (row[2] ==3) {
$(this).parent().parent().find(".Popular_Ninki").addClass("BgOrange")
}
}
}
}
}
$(this).parent().removeClass('Odds_Ninki');
$(this).removeClass('Odds_Ninki');
if($(this).text()<10){
$(this).parent().removeClass('Odds_Ninki');
$(this).addClass('Odds_Ninki');
}
});
var tmDeleteUpdateOddsClass = setTimeout(function(){
clearTimeout(tmDeleteUpdateOddsClass);
$(".Shutuba_Table tr .UpdateOdds").removeClass("UpdateOdds");
}, 700);
if (firstTime) {
firstTime = false;
tableSorteAction();
} else {
$(".Shutuba_Table").trigger('update', [true])
}
},
});
});
</script>
</div><!-- /.RaceTableArea -->
<!-- <div class="diary_snap_write_box">
<p><a href="/diary_snapshot.html?snap=aHR0cDovL3JhY2UubmV0a2VpYmEuY29tLz9waWQ9cmFjZSZpZD1wMjAxOTA1MDIwMTAxJm1vZGU9dG9w&meta=race_result" title="ひとこと日記を書く">ひとこと日記を書く</a></p>
</div> -->
<!-- dev2 -->
<div class="Result_Guide" id='premium_guide' style="display: none;">
<p>プレミアムサービスのご利用で<br>
最新オッズをいち早くお届け！</p>
<a href="https://regist.netkeiba.com/account/?pid=login" class="mb20">登録済みの方はこちらからログイン</a>
<div class="MoreLinkBtn Detail"><a href="https://regist.netkeiba.com?pid=premium&service=p16&return_url=http%3A%2F%2Frace.netkeiba.com%2Frace%2Fshutuba.html%3Frace_id%3D202205030411" id="a_monthly_goods_link_12" data-theme="01022">プレミアムサービスの<br />詳細はこちら</a></div>
</div>

<div class="RaceInfo_Notice RaceInfo_Notice01">
<p>
※結果・成績・オッズなどのデータは、必ず主催者発表のものと照合しご確認ください。
<br>※予想オッズは<a href="https://orepro.netkeiba.com/orepro/top.html">俺プロ</a>の投票データを元に算出し、リアルタイムで更新しています。対象は全レースです。 公開時間は特別レースが日曜夕方、その他のレースは木曜18時頃です(変則開催を除く)。 なお、馬券発売開始後は実際のオッズに切り替わります。
</p>
</div><!-- /.RaceInfo_Notice01 -->
<!--<div class="RaceInfo_Notice RaceInfo_Notice02"></div>&lt;!&ndash; /.RaceInfo_Notice02 &ndash;&gt;-->
<script type="text/javascript">
$(function () {
$(".ShutubaTable td.FavMemo a").tooltip({
hide: false,
show: false,
position: {
my: "left top",
at: "left bottom",
using: function (position, feedback) {
console.log(feedback);
var isIE = /*@cc_on!@*/false || !!document.documentMode;
if (isIE) {
position.top = feedback.target.top - (feedback.element.height);
position.left = feedback.target.left
}
$(this).css(position);
}
}
});
});
</script>
<!-- BEGIN _b_shutuba__race_info_notice01 -->

<!-- END _b_shutuba__race_info_notice -->
<!-- block=shutuba__race_info_notice02 (d) -->

<!-- block=shutuba__race_surf (d) -->
<div class="RaceHeadlineAll">
<div class="RaceHeadline" id="race_message_box">
<div class="ListHeadlineWrapper">
</div>
</div>
</div>
<!--<script type="text/javascript" src="https://cdn.netkeiba.com/img.racev3/common/js/raceapi.action.js?2019073001"></script>-->
<script type="text/javascript">
var _raceapi_action_api_url = "https://race.netkeiba.com"+'/api/api_get_racev3_surf.html';
$( document ).ready( function() {
showRaceV3Surf( "race_message_box", "202205030411" );
} );
/**
* 空であるかどうか
*
* @param  mixd    _var 変数
* @return boolean      true=空である false=空ではない
*/
function _empty( _var )
{
if ( undefined == _var || null == _var || '' == _var )
{
return true;
}
return false;
}
</script>
<div class="shutuba_movie">
<div class="special_step_new">
<!-- block=special_step_new (cg) -->
<div class="Title_Sec Special_Step_New">
<h2>エプソムカップ 予想参考映像</h2>
</div><!-- /.Title_Sec -->


<div class="VideoSampleThum special_step_new_" id="race_digest">
<a href="javascript:void(0);" class="PremiumModalLink01">
<img src="https://cdn.netkeiba.com/img.racev3/common/img/netkeiba750.png" alt="参考レース映像" class="Movie_MainImgBox_Thumb lazyload" data-src="https://cdn.netkeiba.com/img.tv/tv_image.php?type=movie&id=6431">

</a>
</div><!-- /.VideoSampleThum -->
<style>
.adminttv {
position:absolute;
top:0;
left:0;
width:100%;
height:100%;
}
</style>
<script>
// function setCookie() {
//     var monthly_goods_cd = '01049';
//     if( monthly_goods_cd != "" ){
//         var limit_time = new Date().getTime() + 30*60*1000;
//         var tmp_date = new Date( limit_time ).toUTCString();
//         var mdomain = document.domain.substr( document.domain.lastIndexOf(".netkeiba") );
//         var cookie_str = "netkeiba_monthly_goods_cd=" + monthly_goods_cd + ";domain=" + mdomain +";path=/;expires=" + tmp_date;document.cookie = cookie_str;
//     }
// }
$(function(){
$('#race_digest').html('<div class="special_step_new" style="position:relative; padding-bottom: 56.25%; height:0; overflow:hidden;" id="race_digest"><iframe id="07197c773d874b7eb993dda23c84df8f" class="adminttv" src="https://tv-player.ap1.admint.biz/5d4b839a9332e/digest/cXZ0cmZnNXE0bzgzOW45MzMycjA3MTk3cDc3M3E4NzRvN3JvOTkzcXFuMjNwODRxczhz/4bfe5210953aaa4419417716271ebaee?site_id=5d4b839a9332e" allowfullscreen="true" frameborder="0" scrolling="no" width="100%" height="100%" allow="encrypted-media *;"></iframe></div>');
// if (navigator.userAgent.indexOf("Firefox") > 0) {
//     $(".ReferenceRace .special_step_new").mouseenter(function(event) {
//         if ($(".ReferenceRace .special_step_new iframe").length) {
//             console.log(event);
//         }
//     });
// }
// $(".ReferenceRace .special_step_new").mouseenter(function(event) {
//     if ($(".ReferenceRace .special_step_new iframe").length) {
//     console.log(event);
//     }
// });
window.focus();
window.addEventListener('blur', function() {
if (document.activeElement.id == $(".special_step_new iframe").attr("id")) {
var monthly_goods_cd = '01049';
// console.log(monthly_goods_cd);
if( monthly_goods_cd != "" ){
var limit_time = new Date().getTime() + 30*60*1000;
var tmp_date = new Date( limit_time ).toUTCString();
var mdomain = document.domain.substr( document.domain.lastIndexOf(".netkeiba") );
var cookie_str = "netkeiba_monthly_goods_cd=" + monthly_goods_cd + ";domain=" + mdomain +";path=/;expires=" + tmp_date;document.cookie = cookie_str;
}
setTimeout(function(){
window.focus();
}, 300);
}
});
} );
</script>
<!-- プレミアム案内モーダル -->
<div class="ModalOverlay PremiumModal02" style="display: none;">
<div class="ModalPremiumInfo">
<div class="Premium_Regist_Box02">
<div class="Premium_Regist_MsgArea01">
<p class="Premium_Regist_Msg01">スーパープレミアムコースなら</p>
<p class="Premium_Regist_Msg02">参考レース映像が見放題</p>
</div><!-- /.Premium_Regist_MsgArea01 -->
<p class="Premium_Regist_Msg_Campaign01">今なら<em>14日間無料</em>でお試し</p>
<a class="Premium_Regist_Btn" id="a_monthly_goods_link_022" data-theme="01049" href="https://regist.netkeiba.com/?pid=premium&course=430">参考レース映像を見る</a>
<p class="Premium_Regist_Txt02">
<a href="https://regist.netkeiba.com/account/?pid=login">登録済みの方はこちらから</a>
</p>
</div><!-- /.Premium_Regist_Box02 -->
<p class="Modal_Close"><a href="javascript:void:(0);">閉じる</a></p>
</div><!-- /.ModalPremiumInfo -->
</div><!-- /.ModalOverlay.PremiumModal02 -->

<script>
$(function() {
// プレミアム案内modal02
var $window = $(window),
$overlay = $('.ModalOverlay'),
scrollbar_width = window.innerWidth - document.body.scrollWidth,
touch_start_y;
$window.on('touchstart', function(event) {
touch_start_y = event.originalEvent.changedTouches[0].screenY;
});
$('a.PremiumModalLink01').on('click', function() {
// プレミアム案内
$window.on('touchmove.noscroll', function(event) {
var overlay = $overlay[0],
current_y = event.originalEvent.changedTouches[0].screenY,
height = $overlay.outerHeight(),
is_top = touch_start_y <= current_y && overlay.scrollTop === 0,
is_bottom = touch_start_y >= current_y && overlay.scrollHeight - overlay.scrollTop === height;
if (is_top || is_bottom) {
event.preventDefault();
}
});
$('html, body').css('overflow', 'hidden');
if (scrollbar_width) {
$('html').css('padding-right', scrollbar_width);
}
$('.PremiumModal02').fadeIn(300);
});
// モーダル閉じる処理
var closeModal = function() {
$('body').removeAttr('style');
$window.off('touchmove.noscroll');
$overlay.animate({
opacity: 0
}, 300, function() {
$overlay.scrollTop(0).hide().removeAttr('style');
$('html').removeAttr('style');
});
};
$overlay.on('click', function(event) {
if (!$(event.target).closest('.ModalPremiumInfo').length) {
closeModal();
}
});
$('.Modal_Close').on('click', function() {
closeModal();
});
// 全頭表示
$('.horse_list1  .ReferenceRaceHorseMore').click(function(){
$('.horse_list1 .ReferenceRaceHorseMore').hide();
$('.horse_list1 dl dt:nth-of-type(n+4), .horse_list1 dl dd:nth-of-type(n+4)').show();
});
$('.horse_list2  .ReferenceRaceHorseMore').click(function(){
$('.horse_list2 .ReferenceRaceHorseMore').hide();
$('.horse_list2 dl dt:nth-of-type(n+4), .horse_list2 dl dd:nth-of-type(n+4)').show();
});
$('.horse_list3  .ReferenceRaceHorseMore').click(function(){
$('.horse_list3 .ReferenceRaceHorseMore').hide();
$('.horse_list3 dl dt:nth-of-type(n+4), .horse_list3 dl dd:nth-of-type(n+4)').show();
});
});
</script>
</div>
<div class="advertisement_news">

<!-- block=common__advertisement_gam (d) -->
<div class="nk_AdvBox_pc mt30">


<!-- /9116787/1491441 -->
<div id='1491441'>
<script>
googletag.cmd.push(function() { googletag.display('1491441'); });
if($('.Special_Step_New').length<1){
$('#1491441').parent('.nk_AdvBox_pc').remove();
}
</script>
</div>


</div>
</div>
</div>
<!-- block=race_expect (cg) -->
<script type="text/javascript" src="https://cdn.netkeiba.com/img.racev3/common/js/slick.min.js"></script>
<section class="Sec_Deploy_Race">
<div class="Title_Sec" style="position: relative">
<h2>レース展開予想</h2>
<dl class="RacePace">
<dt>ペース</dt>
<dd class="Pace_M">M</dd>
</dl>
</div><!-- / .Title_Sec -->
<div class="race_expect">
<p class="deploy_race_image"><img  src="https://cdn.netkeiba.com/img.racev3/common/img/race/05_t1800.png?2019073001" alt=""></p>
<div class="race_expect_slide" >
<div class="RaceOddsArea">
<div class="RaceOddsMenu">
<ul class="jyo_tab">
<li><div><a href="javascript:void(0)" class="Active">スタート後</a></div></li>
<li><div><a href="javascript:void(0)" class="" >3コーナー</a></div></li>
<li><div><a href="javascript:void(0)" class="" >4コーナー</a></div></li>
</ul>
</div>
</div>
<div class="DeployRace_Slide">
<div class="DeployRace_SlideBox" id="DeployRace">
<div class="DeployRace_SlideBoxItem">
<ul>
<li>
<dl>
<dt>先頭</dt>
<dd>
<ul>
<li><span class="lblWaku WakuBan7">10</span>トーラ</li><li><span class="lblWaku WakuBan5">6</span>ノース</li>
</ul>
</dd>
</dl>
</li><li>
<dl>
<dt>先団</dt>
<dd>
<ul>

</ul>
</dd>
</dl>
</li><li>
<dl>
<dt>中団</dt>
<dd>
<ul>
<li><span class="lblWaku WakuBan5">5</span>ダーリ</li><li><span class="lblWaku WakuBan8">12</span>ザダル</li><li><span class="lblWaku WakuBan2">2</span>タイム</li><li><span class="lblWaku WakuBan8">11</span>ジャス</li><li><span class="lblWaku WakuBan1">1</span>シャド</li><li><span class="lblWaku WakuBan4">4</span>ヤマニ</li><li><span class="lblWaku WakuBan6">8</span>ガロア</li><li><span class="lblWaku WakuBan6">7</span>トーセ</li><li><span class="lblWaku WakuBan3">3</span>コルテ</li><li><span class="lblWaku WakuBan7">9</span>ハッピ</li>
</ul>
</dd>
</dl>
</li><li>
<dl>
<dt>後方</dt>
<dd>
<ul>

</ul>
</dd>
</dl>
</li>
</ul>
</div><!-- /.DeployRace_SlideBoxItem --><div class="DeployRace_SlideBoxItem">
<ul>
<li>
<dl>
<dt>先頭</dt>
<dd>
<ul>
<li><span class="lblWaku WakuBan5">6</span>ノース</li><li><span class="lblWaku WakuBan7">10</span>トーラ</li><li><span class="lblWaku WakuBan5">5</span>ダーリ</li><li><span class="lblWaku WakuBan8">12</span>ザダル</li>
</ul>
</dd>
</dl>
</li><li>
<dl>
<dt>先団</dt>
<dd>
<ul>
<li><span class="lblWaku WakuBan2">2</span>タイム</li><li><span class="lblWaku WakuBan8">11</span>ジャス</li><li><span class="lblWaku WakuBan1">1</span>シャド</li><li><span class="lblWaku WakuBan4">4</span>ヤマニ</li>
</ul>
</dd>
</dl>
</li><li>
<dl>
<dt>中団</dt>
<dd>
<ul>
<li><span class="lblWaku WakuBan6">8</span>ガロア</li><li><span class="lblWaku WakuBan6">7</span>トーセ</li><li><span class="lblWaku WakuBan3">3</span>コルテ</li>
</ul>
</dd>
</dl>
</li><li>
<dl>
<dt>後方</dt>
<dd>
<ul>
<li><span class="lblWaku WakuBan7">9</span>ハッピ</li>
</ul>
</dd>
</dl>
</li>
</ul>
</div><!-- /.DeployRace_SlideBoxItem --><div class="DeployRace_SlideBoxItem">
<ul>
<li>
<dl>
<dt>先頭</dt>
<dd>
<ul>
<li><span class="lblWaku WakuBan5">6</span>ノース</li><li><span class="lblWaku WakuBan5">5</span>ダーリ</li><li><span class="lblWaku WakuBan8">12</span>ザダル</li><li><span class="lblWaku WakuBan2">2</span>タイム</li>
</ul>
</dd>
</dl>
</li><li>
<dl>
<dt>先団</dt>
<dd>
<ul>
<li><span class="lblWaku WakuBan8">11</span>ジャス</li><li><span class="lblWaku WakuBan1">1</span>シャド</li><li><span class="lblWaku WakuBan4">4</span>ヤマニ</li><li><span class="lblWaku WakuBan6">8</span>ガロア</li>
</ul>
</dd>
</dl>
</li><li>
<dl>
<dt>中団</dt>
<dd>
<ul>
<li><span class="lblWaku WakuBan7">10</span>トーラ</li><li><span class="lblWaku WakuBan6">7</span>トーセ</li><li><span class="lblWaku WakuBan3">3</span>コルテ</li>
</ul>
</dd>
</dl>
</li><li>
<dl>
<dt>後方</dt>
<dd>
<ul>
<li><span class="lblWaku WakuBan7">9</span>ハッピ</li>
</ul>
</dd>
</dl>
</li>
</ul>
</div><!-- /.DeployRace_SlideBoxItem -->
</div><!-- /.DeployRace_SlideBox -->
</div><!-- /.DeployRace_Slide -->
</div>
</div>
</section><!-- Sec_Deploy_Race -->
<script>
$(document).ready(function(){
//
var $slider = $('#DeployRace');
if($slider.hasClass('slick-initialized')){
$('.jyo_tab li  a').removeClass('Active');
$('.jyo_tab li').eq(0).find('a').addClass('Active');
$slider.slick('slickGoTo', parseInt(0));
}else{
$slider.slick({
slidesToShow: 1,
dots: false,
infinite: true,
arrows: true,
autoplay: false,
speed: 300,
adaptiveHeight: true,
});
}
$slider.on('afterChange', function(event, slick, currentSlide){
$('.jyo_tab li a').removeClass('Active');
var curSlider = $(slick.$slides[currentSlide]);
var ChangeslideIndex = curSlider.data('slick-index');
$('.jyo_tab li').eq(ChangeslideIndex).find('a').addClass('Active');
});
$('.jyo_tab a').click(function(e){
e.preventDefault();
var activeLi = $(this).closest('li');
var slideIndex = $('.jyo_tab li').index(activeLi);
$slider.slick('slickGoTo', parseInt(slideIndex));
});
});
</script>
<!-- block=top3data (cg) -->
<!-- 各データ上位3頭 -->
<section class="top3data">
<div class="Contents_Header">
<div class="Title_Sec Border_Bottom Border_Top">
<h2>各データ上位3頭</h2>
</div><!-- /.Title_Sec -->
</div><!-- /.Contents_Header -->
<div class="PickupHorseArea">
<table class="RaceCommon_Table PickupHorseTable01 AnaBestTable">
<tbody>
<tr>
<th>
<div class="PickupHorseTableTitle">能力</div><!-- /.PickupHorseTableTitle -->
</th>
<td>
<a href="https://race.netkeiba.com/race/speed.html?race_id=202205030411">
<div class="AnaBest_HorseBox">
<div class="Kyaku_Type_box">
<span class="WakuBan1 Kyaku_Type_Num">1</span><br>
<span class="UmaName" style="font-size: 9px;">シャド</span>
</div><div class="Kyaku_Type_box">
<span class="WakuBan2 Kyaku_Type_Num">2</span><br>
<span class="UmaName" style="font-size: 9px;">タイム</span>
</div><div class="Kyaku_Type_box">
<span class="WakuBan8 Kyaku_Type_Num">12</span><br>
<span class="UmaName" style="font-size: 9px;">ザダル</span>
</div>
<span class="AnaBest_More LinkMore">タイム指数へ</span>
</div>
</a>
</td>
</tr>
</tbody>
</table>
<table class="RaceCommon_Table PickupHorseTable01 AnaBestTable">
<tbody>
<tr>
<th>
<div class="PickupHorseTableTitle">上昇度</div><!-- /.PickupHorseTableTitle -->
</th>
<td>
<a href="https://race.sp.netkeiba.com/barometer/score.html?race_id=202205030411&rf=be3">
<div class="AnaBest_HorseBox">
<div class="Kyaku_Type_box">
<span class="WakuBan2 Kyaku_Type_Num">2</span>
<br>
<span class="UmaName" style="font-size: 9px;">タイム</span>
</div><div class="Kyaku_Type_box">
<span class="WakuBan5 Kyaku_Type_Num">6</span>
<br>
<span class="UmaName" style="font-size: 9px;">ノース</span>
</div><div class="Kyaku_Type_box">
<span class="WakuBan8 Kyaku_Type_Num">12</span>
<br>
<span class="UmaName" style="font-size: 9px;">ザダル</span>
</div>
<span class="AnaBest_More LinkMore">調子偏差値へ</span>
</div>
</a>
</td>
</tr>
</tbody>
</table>
<table class="RaceCommon_Table PickupHorseTable01 AnaBestTable">
<tbody>
<tr>
<th>
<div class="PickupHorseTableTitle">騎手</div><!-- /.PickupHorseTableTitle -->
</th>
<td>
<a href="https://race.netkeiba.com/race/data.html?mode=ranking&race_id=202205030411">
<div class="AnaBest_HorseBox">
<div class="Kyaku_Type_box">
<span class="WakuBan2 Kyaku_Type_Num">2</span><br>
<span class="UmaName" style="font-size: 9px;">戸崎圭</span>
</div><div class="Kyaku_Type_box">
<span class="WakuBan5 Kyaku_Type_Num">5</span><br>
<span class="UmaName" style="font-size: 9px;">ルメー</span>
</div><div class="Kyaku_Type_box">
<span class="WakuBan8 Kyaku_Type_Num">12</span><br>
<span class="UmaName" style="font-size: 9px;">レーン</span>
</div>
<span class="AnaBest_More LinkMore">該当コースランキングへ</span>
</div>
</a>
</td>
</tr>
</tbody>
</table>
<table class="RaceCommon_Table PickupHorseTable01 AnaBestTable">
<tbody>
<tr>
<th>
<div class="PickupHorseTableTitle">距離</div><!-- /.PickupHorseTableTitle -->
</th>
<td>
<a href="https://race.netkeiba.com/race/data.html?mode=distance&race_id=202205030411">
<div class="AnaBest_HorseBox">
<div class="Kyaku_Type_box">
<span class="WakuBan3 Kyaku_Type_Num">3</span><br>
<span class="UmaName" style="font-size: 9px;">コルテ</span>
</div><div class="Kyaku_Type_box">
<span class="WakuBan5 Kyaku_Type_Num">5</span><br>
<span class="UmaName" style="font-size: 9px;">ダーリ</span>
</div><div class="Kyaku_Type_box">
<span class="WakuBan5 Kyaku_Type_Num">6</span><br>
<span class="UmaName" style="font-size: 9px;">ノース</span>
</div>
<span class="AnaBest_More LinkMore">距離別成績へ</span>
</div>
</a>
</td>
</tr>
</tbody>
</table>
</div>
</section>

<!-- block=shutuba__race_kyaku_type (d) -->


<!-- block=common__advertisement_gam (d) -->
<div class="nk_AdvBox_pc mt30">
<!-- /9116787/1491440 -->
<div id='1491440'>
<script>
googletag.cmd.push(function() { googletag.display('1491440'); });
</script>
</div>




</div>
<!-- block=shutuba__race_yos_gensen_list_box (d) -->
<!-- raceドメイン内　ウマいブロック　専用css -->
<link rel='stylesheet' href="https://cdn.netkeiba.com/img.racev3/common/css/race_pc_umai_new.css?20200205" type='text/css' media="all">
<div class="Contents_Box YosoGensenListBox padd_bottom">
<link href="https://cdn.netkeiba.com/img.yoso/common/css/umai_area01.css?2019073001" rel="stylesheet" type="text/css" media="all">
<div class="GensenYosoTitle">
<h2 class="TitleHeading  CardBackground"><span>厳選予想 ウマい馬券</span></h2>
</div><!-- /.GensenYosoTitle -->
<div id="ow_bunner_view" style="display: none; text-align: center; margin: 10px 0;"></div>
<div id="delay_umai_baken">
<div id="goods_view">
<div class="FileLoader"><img src="https://cdn.netkeiba.com/img.racev3/common/img/common/gif-load.gif?2019073001"></div>
</div>
</div>
</div><!-- /.Contents_Box.YosoGensenListBox -->
<script src="https://cdn.netkeiba.com/img.yoso/common/js/social_cart.js?2019073001" type="text/javascript"></script>
<script src="https://yoso.netkeiba.com/common/js/yoso/YosoJraNar.js?2020012904" type="text/javascript"></script>
<script src="https://cdn.netkeiba.com/img.racev3/common/js/jquery.lazyscript.js?2019073001" type="text/javascript"></script>
<script type="text/javascript">
$(document).ready( function(){
var yoso_jra_nar = new YosoJraNar('https://yoso.netkeiba.com');
var _show_id = 'goods_view';
var _race_id = '202205030411';
var _sort = ''; // defualt
var _limit =100;
var _device = '1'; // defualt
var _return_url = encodeURIComponent(location.href);
var _mode = 'sendmsg';
var options = {
type: "visible",
id: "delay_umai_baken",
scripts: [
],
success: function () {

yoso_jra_nar.ShowGoodsListRace(_show_id, _race_id, _sort, _limit, _device, _return_url, _mode, function(data){
$("#" + _show_id).html( data.html );
});
}
};
if(isNaN(_race_id*1)){
options.success() // 海外は遅延なし
} else {
$.lazyscript(options);
}
});
</script>

<!-- block=umai_goods_list_f (d) -->
<div id="delay_umai_goods_f">
<div class="Senmonshi_Box mb00" id="sec_umai_goods_f" style="display:none;">
<h3 class="TitleHeading TitleHeading_Senmonshi_Box">
<span>競馬専門紙<i class="icon_netkeiba"></i></span>
<em class="Subtitle" style="display: none"></em>
<a href="https://yoso.netkeiba.com/senmonshi/jra/?rf=pcrace_shutuba" title="競馬専門紙一覧" class="LinkMore Heading_Win">販売一覧</a>
</h3>
<div id="umai_goods_list_f_view">
<div class="FileLoader"><img src="https://cdn.netkeiba.com/img.racev3/common/img/common/gif-load.gif?20190116" alt=""></div>
</div>
</div>
</div>
<script src="https://cdn.netkeiba.com/img.racev3/common/js/jquery.lazyscript.js"></script>
<script type="text/javascript">
$(document).ready(function() {
var _race_id = '202205030411';
var _show_id = 'umai_goods_list_f_view';
var _is_apppli = '';
var options = {
type: "visible",
id: "delay_umai_goods_f",
scripts: [
],
success: function () {
get_umai_goods_f_data(_race_id, _show_id, function(data) {
// console.log(data);
if (data.status == 'OK') {
$("#sec_umai_goods_f").css("display", "block");
$("#" + _show_id).html( data.html );
}
});
}
};
$.lazyscript(options);
// ------------------------------------------------------------------------
function get_umai_goods_f_data(_race_id, _show_id, _callback)
{
console.log('get_umai_goods_f_data');
var _data = {};
_data.input       = 'UTF-8';
_data.output      = 'jsonp';
_data.race_id     = _race_id;
_data.show_id     = _show_id;
_data.rf_param    = 'pcrace_shutuba';
if(_is_apppli === '1'){
_data.appli_modal     = _is_apppli;
}
$.ajax({
type     : 'GET',
url      : 'https://yoso.netkeiba.com/senmonshi/api/api_get_goods_list_f.html',
data     : _data,
dataType : _data.output,
success  : function( data ){
if (undefined != _callback) {
_callback( data );
}
},
error    : function(XMLHttpRequest, textStatus, errorThrown) {
console.log('XMLHttpRequest: %O',XMLHttpRequest);
console.log('textStatus: %O',textStatus);
}
});
}
});
</script>
<!-- block=common__advertisement_taboola_main (d) -->
<div id="taboola-below-article-thumbnails_race"></div>
<script type="text/javascript">
window._taboola = window._taboola || [];
_taboola.push({
mode: 'alternating-thumbnails-a-race',
container: 'taboola-below-article-thumbnails_race',
placement: 'Below Article Thumbnails_race',
target_type: 'mix'
});
</script>

<!-- block=common__advertisement_gam (d) -->
<div class="nk_AdvBox_pc mt30">

<!-- /9116787/1492791 -->
<div id='1492791'>
<script>
googletag.cmd.push(function() { googletag.display('1492791'); });
</script>
</div>



</div>
</div><!-- / .RaceColumn02 -->
</div><!-- / #page -->
<footer>
<!-- block=common__race_footer (cg) -->
<div class="NkFooterArea">
<div class="BtnPagetop">
<a href="javascript:void(0)" title="ページトップへ"></a>
</div><!-- /.BtnPagetop -->
<script type="text/javascript">
$(function() {
$('.BtnPagetop a').click(function () {
$('body,html').animate({
scrollTop: 0
}, 400);
return false;
});
});
</script>
<div class="KeirinLink01">
<a href="//keirin.netkeiba.com/?rf=nk_pc_footer" title="netkeirin"><img src="https://cdn.netkeiba.com/img.www/style/netkeiba.ja/image/common/PC_footer_bnr01.png" alt="いま競輪が熱い！nerkeirinで競輪を気軽に楽しもう" /></a>
</div><!-- /.KeirinLink01 -->
<dl class="FootSiteTitle fc">
<dt>
<a href="https://www.netkeiba.com/?rf=footer" title="netkeiba.com">
<img src="https://cdn.netkeiba.com/img.www/style/netkeiba.ja/image/common/netkeiba_logo01.png?2019073001" alt="netkeiba.com" />
</a>
</dt>
<dd>
<p>利用者数<strong>1700</strong>万人突破！<strong>No.1</strong>競馬サイト</p>
</dd>
</dl>
<div class="FootWrap">
<dl class="NkFoot01 NkFootCateLink">
<dt>カテゴリ</dt>
<dd class="fc">
<ul>
<li>
<a href="https://news.netkeiba.com?rf=footer" title="ニュース">ニュース</a>
</li>
<li>
<a href="https://race.netkeiba.com/top/?rf=footer" title="レース">レース</a>
</li>
<li>
<a href="https://yoso.netkeiba.com?rf=footer" title="ウマい馬券">ウマい馬券</a>
</li>
<li>
<a href="https://news.netkeiba.com?pid=column_top&rf=footer" title="コラム">コラム</a>
</li>
<li>
<a href="https://tv.netkeiba.com/?rf=footer" title="netkeibaTV">netkeibaTV</a>
</li>
<li>
<a href="https://nar.netkeiba.com/top/?rf=footer" title="地方競馬">地方競馬</a>
</li>
<li>
<a href="https://db.netkeiba.com?rf=footer" title="データベース">データベース</a>
</li>
<li>
<a href="https://orepro.netkeiba.com?rf=footer" title="俺プロ">俺プロ</a>
</li>
</ul>
<ul>
<li>
<a href="https://owner.netkeiba.com?rf=footer" title="一口馬主">一口馬主</a>
</li>
<li>
<a href="https://pog.netkeiba.com?rf=footer" title="POG">POG</a>
</li>
<li>
<a href="https://bbs.pc.keiba.findfriends.jp?rf=footer" title="競馬広場">競馬広場</a>
</li>
<li>
<a href="https://dir.netkeiba.com//keibamatome/index.html?rf=footer" title="まとめ">まとめ</a>
</li>
<li>
<a href="https://yoso.netkeiba.com/senmonshi/?rf=footer" title="競馬新聞">競馬新聞</a>
</li>
<li>
<a href="https://race.netkeiba.com/bookmark/bookmark.html?rf=footer" title="お気に入り馬">お気に入り馬</a>
</li>
<li>
<a href="https://regist.netkeiba.com?rf=footer" title="アカウント">アカウント</a>
</li>
</ul>
</dd>
</dl>
<dl class="NkFoot01">
<dt>ヘルプ＆ガイド</dt>
<dd>
<ul>
<li>
<a href="https://info.netkeiba.com//?rf=footer" title="お知らせ">お知らせ</a>
</li>
<li>
<a href="https://regist.netkeiba.com?pid=premium&rf=footer" title="プレミアムサービスのご案内">プレミアムサービスのご案内</a>
</li>
<li>
<a href="https://regist.netkeiba.com?pid=help&rf=footer" title="よくある質問・お問い合わせ">よくある質問・お問い合わせ</a>
</li>
</ul>
</dd>
</dl>
<dl class="NkFoot01">
<dt>netkeiba.comについて</dt>
<dd>
<ul>
<li>
<a href="https://www.netkeiba.com/recruit/?rf=footer" title="採用情報">採用情報</a>
</li>
<li>
<a href="https://www.netkeiba.com/info/ad/?rf=footer" title="広告掲載について">広告掲載について</a>
</li>
<li>
<a href="https://www.netkeiba.com/info/kiyaku.html?rf=footer" title="利用規約">利用規約</a>
</li>
<li>
<a href="https://www.netdreamers.co.jp/company/about/privacy.html?rf=footer" title="プライバシーポリシー">プライバシーポリシー</a>
</li>
<li>
<a href="https://www.netkeiba.com/info/guide.html?rf=footer" title="投稿ガイドライン">投稿ガイドライン</a>
</li>
<li>
<a href="https://www.netkeiba.com/info/tokusyo.html?rf=footer" title="特定商取引法に基づく表記">特定商取引法に基づく表記</a>
</li>
<li>
<a href="https://www.netdreamers.co.jp/?rf=footer" title="運営会社">運営会社</a>
</li>
</ul>
</dd>
</dl>
<dl class="NkFoot01">
<dt>スマホでnetkeiba</dt>
<dd class="SpNkInfoImg">
<img src="https://cdn.netkeiba.com/img.www/style/netkeiba.ja/image/common/img_nk_searchimg01.png?2019073001" alt="検索" class="SearchImg01" />
<img src="https://cdn.netkeiba.com/img.www/style/netkeiba.ja/image/common/img_nk_qr01.png?2019073001" alt="バーコード" class="QrImg01" />
</dd>
<dt>アプリでサクサクnetkeiba</dt>
<dd>
<ul class="AprStoreList fc">
<li>
<a href="https://itunes.apple.com/jp/app/id464562684/" title="Appstore"><img src="https://cdn.netkeiba.com/img.www/style/netkeiba.ja/image/common/bnr_appstore_01.png?2019073001" alt="Appstore" class="" /></a>
</li>
<li>
<a href="https://play.google.com/store/apps/details?id=jp.co.netdreamers.netkeiba" title="googleplay"><img src="https://cdn.netkeiba.com/img.www/style/netkeiba.ja/image/common/bnr_googleplay_01.png?20210728" alt="googleplay" class="" /></a>
</li>
</ul>
</dd>
<dd class="Nk_Sns">
<ul class="fc">
<li>
<a href="https://twitter.com/netkeiba" title="公式 Twitter" class="Tw"></a>
</li>
<li>
<a href="https://ja-jp.facebook.com/netkeiba" title="公式 Facebook" class="Fb"></a>
</li>
<li>
<a href="https://line.me/R/ti/p/%40oa-netkeiba" title="LINE" class="Line"></a>
</li>
<li>
<a href="http://www.youtube.com/user/netkeibaTV" title="netkeibaチャンネル" class="Yt"></a>
</li>
<li>
<a href="https://www.instagram.com/netkeiba/" title="Instagram" class="Ig"></a>
</li>
<li>
<a href="https://www.netkeiba.com/?pid=rss" title="RSS" class="Rss"></a>
</li>
</ul>
</dd>
</dl>
</div><!-- /.FootWrap -->
</div><!-- /.NkFooterArea -->
<div class="GlobalFooterArea">
<div class="FootWrap">
<dl class="NkFoot02">
<dt class="GfootIcon01 IconGame01">netkeiba.com 公式競馬ゲーム</dt>
<dd>
<ul>
<li>
<a href="https://www.netkeiba.com/game/umasta.html?rf=footer" target='_blank' title="うまいるスタジアム">みんなの愛馬とバトル！ <strong>うまいるスタジアム</strong></a>
</li>
</ul>
</dd>
<dt class="GfootIcon01 IconSisterSite01">netkeiba.com 姉妹サイト</dt>
<dd>
<ul>
<li>
<a href="//keirin.netkeiba.com/?rf=footer" target='_blank'>競輪総合メディア <strong>netkeirin(ネットケイリン)</strong></a>
</li>
</ul>
</dd>
</dl>
<dl class="NkFoot02">
<dt class="GfootIcon01 IconMedia01">関連メディア</dt>
<dd>
<ul>
<li>
<a href="https://sp.baseball.findfriends.jp/?rf=footer" target='_blank' title="週刊ベースボールONLINE">徹底取材！野球情報は <strong>週刊ベースボールONLINE</strong></a>
</li>
<li>
<a href="https://sp.golf.findfriends.jp/?rf=footer" target='_blank' title="ワッグルオンライン">ゴルフレッスン情報サイト <strong>ワッグルオンライン</strong></a>
</li>
<li>
<a href="https://recipe.sp.findfriends.jp/?rf=footer" target='_blank' title="KATSUYOレシピ">小林カツ代直伝！ <strong>KATSUYOレシピ</strong></a>
</li>
</ul>
</dd>
</dl>
<dl class="NkFoot02">
<dt class="GfootIcon01 IconSoftware01">ソフトウェア・プロダクト</dt>
<dd>
<ul>
<li>
<a href="https://smart.lets-ktai.jp/?rf=footer" target='_blank' title="SMART会員証">もっともセキュアな店舗売上向上アプリ <strong>SMART会員証</strong></a>
</li>
<li>
<a href="https://lets-ktai.jp/?rf=footer" target='_blank' title="Let'sケータイ！">スマホサイト制作ASP <strong>Let'sケータイ！</strong></a>
</li>
<li>
<a href="https://webspiral.jp/?rf=footer" target='_blank' title="WEB SPIRAL">サイト運営を劇的に効率化するCMS <strong>WEB SPIRAL</strong></a>
</li>
</ul>
</dd>
</dl>
</div><!-- /.FootWrap -->
<p class="CopyRight">
<small>&copy; Net Dreamers Co., Ltd.</small>
</p>
</div><!-- /.GlobalFooterArea -->
<!-- Google Tag Manager -->
<noscript><iframe src="//www.googletagmanager.com/ns.html?id=GTM-K6PJT6"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'//www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-K6PJT6');</script>
<!-- End Google Tag Manager -->

<!-- block=common__advertisement_gam (d) -->
<div class="nk_AdvBox_pc mt30">




<div id="geniee_overlay_outer" style="position:fixed; bottom: 0px; width:100%; height:90px; left:0px; right:0px; margin:auto; z-index:1000000000; text-align: center;background-color: rgba(40, 40, 40, 0.2);">    <img src="https://js.gsspcln.jp/i/7c087a913cb9d4e76b672c4dc767c1a2.png" id="gn_interstitial_close_icon" style="height: 29px; width: 29px; display: block; position: absolute; top: 0px; left: 0px; right:0px; margin: 0px auto; z-index: 999999; transform: translateX(-378.5px);" onclick="document.getElementById('geniee_overlay_outer').style.display='none';">
<!-- /9116787/1491463 -->
<div id='1491463' style="text-align: center;">
<script>
googletag.cmd.push(function() { googletag.display('1491463'); });
</script>
</div>
</div>
</div>
</footer>
<!-- block=common__advertisement_taboola_bottom (d) -->
<script type="text/javascript">
window._taboola = window._taboola || [];
_taboola.push({flush: true});
</script>
<!-- block=lazyload_js (d) -->
<script>
/* Disable minification (remove `.min` from URL path) for more info */
(function(undefined) {}).call('object' === typeof window && window || 'object' === typeof self && self || 'object' === typeof global && global || {});
(function (root, factory) {
if (typeof exports === "object") {
module.exports = factory(root);
} else if (typeof define === "function" && define.amd) {
define([], factory(root));
} else {
root.LazyLoad = factory(root);
}
}) (typeof global !== "undefined" ? global : this.window || this.global, function (root) {
"use strict";
const defaults = {
src: "data-src",
srcset: "data-srcset",
selector: ".lazyload"
};
/**
* Merge two or more objects. Returns a new object.
* @private
* @param   deep     If true, do a deep (or recursive) merge [optional]
* @param    objects  The objects to merge together
* @returns           Merged values of defaults and options
*/
const extend = function ()  {
let extended = {};
let deep = false;
let i = 0;
let length = arguments.length;
/* Check if a deep merge */
if (Object.prototype.toString.call(arguments[0]) === "[object Boolean]") {
deep = arguments[0];
i++;
}
/* Merge the object into the extended object */
let merge = function (obj) {
for (let prop in obj) {
if (Object.prototype.hasOwnProperty.call(obj, prop)) {
/* If deep merge and property is an object, merge properties */
if (deep && Object.prototype.toString.call(obj[prop]) === "[object Object]") {
extended[prop] = extend(true, extended[prop], obj[prop]);
} else {
extended[prop] = obj[prop];
}
}
}
};
/* Loop through each object and conduct a merge */
for (; i < length; i++) {
let obj = arguments[i];
merge(obj);
}
return extended;
};
function LazyLoad(images, options) {
this.settings = extend(defaults, options || {});
this.images = images || document.querySelectorAll(this.settings.selector);
this.observer = null;
this.init();
}
LazyLoad.prototype = {
init: function() {
/* Without observers load everything and bail out early. */
if (!root.IntersectionObserver) {
this.loadImages();
return;
}
let self = this;
let observerConfig = {
root: null,
rootMargin: "0px",
threshold: [0, 0.5, 1.0]
};
this.observer = new IntersectionObserver(function(entries) {
entries.forEach(function (entry) {
if (entry.intersectionRatio > 0) {
self.observer.unobserve(entry.target);
let src = entry.target.getAttribute(self.settings.src);
let srcset = entry.target.getAttribute(self.settings.srcset);
if ("img" === entry.target.tagName.toLowerCase()) {
if (src) {
entry.target.src = src;
}
if (srcset) {
entry.target.srcset = srcset;
}
} else {
entry.target.style.backgroundImage = "url(" + src + ")";
}
entry.target.classList.remove("lazyload");
}
});
}, observerConfig);
this.images.forEach(function (image) {
self.observer.observe(image);
});
},
loadAndDestroy: function () {
if (!this.settings) { return; }
this.loadImages();
this.destroy();
},
loadImages: function () {
if (!this.settings) { return; }
let self = this;
this.images.forEach(function (image) {
let src = image.getAttribute(self.settings.src);
let srcset = image.getAttribute(self.settings.srcset);
if ("img" === image.tagName.toLowerCase()) {
if (src) {
image.src = src;
}
if (srcset) {
image.srcset = srcset;
}
} else {
image.style.backgroundImage = "url(" + src + ")";
}
});
},
destroy: function () {
if (!this.settings) { return; }
this.observer.disconnect();
this.settings = null;
}
};
root.lazyload = function(images, options) {
return new LazyLoad(images, options);
};
if (root.jQuery) {
const $ = root.jQuery;
$.fn.lazyload = function (options) {
options = options || {};
options.attribute = options.attribute || "data-src";
new LazyLoad($.makeArray(this), options);
return this;
};
}
return LazyLoad;
});
</script>
<script>
$(function() {
if (typeof lazyload === 'function') {
$('.lazyload').lazyload();
} else {
var lazyImages = [].slice.call(document.querySelectorAll(".lazyload"));
lazyImages.forEach(function(lazyImage) {
console.log(lazyImage.tagName);
if (lazyImage.tagName == 'DIV') {
lazyImage.style.backgroundImage = "url(" + lazyImage.dataset.src + ")";
} else {
lazyImage.src = lazyImage.dataset.src;
}
lazyImage.classList.remove("lazyload");
});
}
});
</script>
</body>
</html>
    """

    print(url)

    df = pd.read_html(source_code, match='馬名')[0]  # Tableを抽出
    df.columns = df.columns.droplevel(0)  # headerのMultiIndexを解除

    # レース情報を取得
    soup = BeautifulSoup(source_code, "html.parser")
    race_origin = soup.select_one('div.RaceData01')
    race_name = race_origin.select_one('span').contents[0].replace(' ', '')
    race_name_other = re.split('[()]', race_origin.contents[3].split('/')[0].replace(' ', ''))[1][0]
    race_name = race_name[0] + race_name_other + race_name[1:]  # レース名
    try:
        race_weather = race_origin.contents[3].split('/')[1].split(':')[1]  # 天候
        race_cond = race_origin.select_one('span[class="Item03"]').contents[0].split(':')[1]  # レースの状態
    except IndexError:
        race_weather = np.nan
        race_cond = np.nan
    race_type = re.split('[()]', soup.title.contents[0])[1]  # レースの種類

    # 騎手のリストを取得
    soup = BeautifulSoup(source_code, "html.parser")
    race_table = soup.select_one('div.RaceTableArea')
    jockey_url_list = race_table.find_all('a', href=re.compile('/jockey/result/recent/[0-90-9]+'))

    # horse_idを取得
    horse_list = race_table.find_all('a', href=re.compile('/horse/[0-90-9]+'))
    horse_id_list = []
    [horse_id_list.append(horse_url.attrs['href'].split('/')[4]) for horse_url in horse_list]
    # jockey_idを取得
    jockey_list = race_table.find_all('a', href=re.compile('/jockey/result/recent/[0-90-9]+'))
    jockey_id_list = []
    [jockey_id_list.append(jockey_url.attrs['href'].split('/')[6]) for jockey_url in jockey_list]
    # trainer_idを取得
    trainer_list = race_table.find_all('a', href=re.compile('/trainer/result/recent/[0-90-9]+'))
    trainer_id_list = []
    [trainer_id_list.append(trainer_url.attrs['href'].split('/')[6]) for trainer_url in trainer_list]

    jockey_list = []
    for jockey in jockey_url_list:
        # 各騎手名を取得
        jockey_url = jockey.attrs['href']
        res = requests.get(jockey_url, proxies=proxies, verify=False)
        time.sleep(1)
        soup = BeautifulSoup(res.content, "html.parser")
        title = soup.find('title').text
        jockey_list.append(title.split(' ')[0].replace('．', '')[:4])

    # 調教師のリストを取得
    trainer_url_list = race_table.find_all('a', href=re.compile('/trainer/result/recent/[0-90-9]+'))

    trainer_list = []
    for trainer, trainer_origin in zip(trainer_url_list, df['厩舎']):
        # 各調教師名を取得
        trainer_url = trainer.attrs['href']
        res = requests.get(trainer_url, proxies=proxies, verify=False)
        time.sleep(1)
        soup = BeautifulSoup(res.content, "html.parser")
        title = soup.find('title').text
        trainer_name = title.split(' ')[0][:4]
        if trainer_origin[:2] == '栗東':
            trainer_type = '[西] '
        elif trainer_origin[:2] == '美浦':
            trainer_type = '[東] '
        else:
            trainer_type = '[地] '
        trainer_list.append(trainer_type + trainer_name)

    # 不要な属性を削除
    del df['印']
    del df['登録']
    del df['メモ']

    # ヘッダーを変更，並び替え
    df = df.rename(columns={'枠': 'frame_num', '馬番': 'horse_num', '馬名': 'horse_name', '性齢': 'sex_age',
                            '斤量': 'weight_to_carry', '騎手': 'jockey', '厩舎': 'trainer',
                            '馬体重(増減)': 'horse_weight', 'オッズ 更新': 'win', '予想オッズ': 'win', '人気': 'popular'})

    df = df.reindex(columns=['frame_num', 'horse_num', 'horse_name', 'sex_age', 'weight_to_carry', 'jockey', 'win',
                             'popular', 'horse_weight', 'trainer'])

    # 値の置き換え
    df['jockey'] = jockey_list
    df['trainer'] = trainer_list

    win_list = [9.3, 8.6, 52.2, 10.8, 4.1, 7.3, 38.9, 23.1, 118.9, 30.0, 3.7, 5.9]
    df['win'] = win_list

    # 馬体重を使わない場合
    if pd.isnull(df['horse_weight'][0]):
        df['horse_weight'] = '502(0)'

    # 馬体重が前計不の場合
    for i, horse_weight in enumerate(df['horse_weight']):
        weight_list = re.split('[()]', horse_weight)
        if weight_list[1] == '前計不':
            df['horse_weight'][i] = weight_list[0] + '(0)'

        print(weight_list)

    # レース名，天候，レース状態を追加
    df['race_name'] = race_name

    df['weather'] = race_weather
    # 天候を使わない場合
    if pd.isnull(df['weather'][0]):
        df['weather'] = '晴'

    df['race_cond'] = race_cond
    # 馬場状態を使わない場合
    if pd.isnull(df['race_cond'][0]):
        df['race_cond'] = '良'

    df['race_type'] = race_type

    df.insert(3, 'horse_id', horse_id_list)
    df.insert(7, 'jockey_id', jockey_id_list)
    df.insert(12, 'trainer_id', trainer_id_list)

    print(df.head())

    # ブラウザを閉じる
    driver.quit()

    # CSVファイルとして出力
    df.to_csv(f'{result_dir}test.csv', index=False)


if __name__ == '__main__':
    url = 'https://race.netkeiba.com/race/shutuba.html?race_id=202206030111&rf=race_submenu'
    get_test_data(url)