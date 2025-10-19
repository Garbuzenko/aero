<!--  BEGIN SIDEBAR  -->
<div class="sidebar-wrapper sidebar-theme">
<nav id="sidebar">
  <div class="navbar-nav theme-brand flex-row  text-center">
                    <div class="nav-logo">
                        <div class="nav-item theme-logo">
                            <a href="./index.html">
                                <img src="<?=$xc['tmp_url'];?>/src/assets/img/logo.svg" class="navbar-logo" alt="logo">
                            </a>
                        </div>
                        <div class="nav-item theme-text">
                            <a href="./index.html" class="nav-link"> CORK </a>
                        </div>
                    </div>
                    <div class="nav-item sidebar-toggle">
                        <div class="btn-toggle sidebarCollapse">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-chevrons-left"><polyline points="11 17 6 12 11 7"></polyline><polyline points="18 17 13 12 18 7"></polyline></svg>
                        </div>
                    </div>
                </div>
                <div class="shadow-bottom"></div>
                <ul class="list-unstyled menu-categories" id="accordionExample">
                    <li class="menu <?=$xc['mod_menu']['main'];?>">
                        <a href="<?=DOMAIN;?>" aria-expanded="false" class="dropdown-toggle">
                            <div class="">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trending-up"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
                                <span>Рейтинг</span>
                            </div>
                            
                        </a>
                    </li>
                    <?if($_SESSION['role_id']==1):?>
                    <li class="menu <?=$xc['mod_menu']['upload'];?>">
                        <a href="<?=DOMAIN;?>/upload" aria-expanded="false" class="dropdown-toggle">
                            <div class="">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-download"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                                <span>Импорт файла</span>
                            </div>
                            
                        </a>
                    </li>
                    <?endif;?>

                    <li class="menu <?=$xc['mod_menu']['regions'];?>">
                        <a href="<?=DOMAIN;?>/regions" aria-expanded="false" class="dropdown-toggle">
                            <div class="">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-box"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
                                <span>Регионы</span>
                            </div>
                            
                        </a>
                    </li>
                    
                    <li class="menu <?=$xc['mod_menu']['module'];?>">
                        <a href="#dashboard4" data-bs-toggle="collapse" aria-expanded="<?if(!empty($xc['mod_menu']['module'])):?>true<?else:?>false<?endif;?>" class="dropdown-toggle">
                            <div class="">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-bar-chart-2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                                <span>BI-дашборды</span>
                            </div>
                            <div>
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-chevron-right"><polyline points="9 18 15 12 9 6"></polyline></svg>
                            </div>
                        </a>
                        <ul class="collapse submenu list-unstyled <?if(!empty($xc['mod_menu']['module'])):?>show<?endif;?>" id="dashboard4" data-bs-parent="#accordionExample">
                            <li class="<?=$xc['mod_menu']['dash-regions'];?>">
                                <a href="<?=DOMAIN;?>/dash-regions">Регионы</a>
                            </li>
                            <li class="<?=$xc['mod_menu']['dash-flights'];?>">
                                <a href="<?=DOMAIN;?>/dash-flights">Полёты</a>
                            </li>
                            <li class="<?=$xc['mod_menu']['dash-honeycombs'];?>">
                                <a href="<?=DOMAIN;?>/dash-honeycombs">Гексагоны</a>
                            </li>
                            <li class="<?=$xc['mod_menu']['flight-density'];?>">
                                <a href="<?=DOMAIN;?>/flight-density">Плотность полётов</a>
                            </li>
                            <li class="<?=$xc['mod_menu']['platforms-bpla'];?>">
                                <a href="<?=DOMAIN;?>/platforms-bpla">Площадки БПЛА</a>
                            </li>
                            <li class="<?=$xc['mod_menu']['dash-clusterization'];?>">
                                <a href="<?=DOMAIN;?>/dash-clusterization">Кластеризация</a>
                            </li>
                            <li class="<?=$xc['mod_menu']['dash-heatmap'];?>">
                                <a href="<?=DOMAIN;?>/dash-heatmap">Тепловая карта</a>
                            </li>
                            <li class="<?=$xc['mod_menu']['dash-infrastructure'];?>">
                                <a href="<?=DOMAIN;?>/dash-infrastructure">Инфраструктура</a>
                            </li>
                            <li class="<?=$xc['mod_menu']['dash-aviation'];?>">
                                <a href="<?=DOMAIN;?>/dash-aviation">Онлайн авиация</a>
                            </li>
                        </ul>
                    </li>
                    <?if($_SESSION['role_id']==1):?>
                    <li class="menu <?=$xc['mod_menu']['reports'];?>">
                        <a href="<?=DOMAIN;?>/reports" aria-expanded="false" class="dropdown-toggle">
                            <div class="">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-airplay"><path d="M5 17H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-1"></path><polygon points="12 15 17 21 7 21 12 15"></polygon></svg>
                                <span>Отчёты</span>
                            </div>
                        </a>
                    </li>
                    
                    <li class="menu <?=$xc['mod_menu']['api-info'];?>">
                        <a href="<?=DOMAIN;?>/api-info" aria-expanded="false" class="dropdown-toggle">
                            <div class="">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-log-out"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
                                <span>API</span>
                            </div>
                        </a>
                    </li>
                    <?endif;?>
                    
                    <li class="menu <?=$xc['mod_menu']['gis'];?>">
                        <a href="#dashboard3" data-bs-toggle="collapse" aria-expanded="<?if(!empty($xc['mod_menu']['gis'])):?>true<?else:?>false<?endif;?>" class="dropdown-toggle">
                            <div class="">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-globe"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
                                <span>Интеграции</span>
                            </div>
                            <div>
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-chevron-right"><polyline points="9 18 15 12 9 6"></polyline></svg>
                            </div>
                        </a>
                        <ul class="collapse submenu list-unstyled <?if(!empty($xc['mod_menu']['gis'])):?>show<?endif;?>" id="dashboard3" data-bs-parent="#accordionExample">
                            <li class="<?=$xc['mod_menu']['overpass'];?>">
                                <a href="<?=DOMAIN;?>/gis/overpass">Overpass API</a>
                            </li>
                            <li class="<?=$xc['mod_menu']['opensky'];?>">
                                <a href="<?=DOMAIN;?>/gis/opensky">Opensky API</a>
                            </li>
                            <li class="<?=$xc['mod_menu']['skyarc'];?>">
                                <a href="<?=DOMAIN;?>/gis/skyarc">Skyarc API</a>
                            </li>
                        </ul>
                    </li>
                    
                    <li class="menu">
                        <a target="_blank" href="https://docs.google.com/document/d/e/2PACX-1vR-7JGtmZtZA_yZKT9r4vBPS2EDBZcMlgMerFUV4VeQjE2rK8lvc96A1UkUJ8TowRKb92iEtQmFup-S/pub?embedded=true" aria-expanded="false" class="dropdown-toggle">
                            <div class="">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-book"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                                <span>Документация</span>
                            </div>
                        </a>
                    </li>
                    
                    <li class="menu <?=$xc['mod_menu']['presentation'];?>">
                        <a  href="<?=DOMAIN;?>/presentation" aria-expanded="false" class="dropdown-toggle">
                            <div class="">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-zap"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
                                <span>Презентация</span>
                            </div>
                        </a>
                    </li>
                    
                    <li class="menu <?=$xc['mod_menu']['video'];?>">
                        <a href="<?=DOMAIN;?>/video" aria-expanded="false" class="dropdown-toggle">
                            <div class="">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-youtube"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"></path><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"></polygon></svg>
                                <span>Видео</span>
                            </div>
                        </a>
                    </li>

                </ul>
            </nav>
        </div>
        <!--  END SIDEBAR  -->