<div class="row layout-top-spacing">
<?if(!empty($reports)):?>
<div class="col-xl-12 col-lg-12 col-sm-12 layout-spacing">
                            <div class="statbox widget box box-shadow">
                                <div class="widget-content widget-content-area">
                                    <div class="table-form">
                                        <div class="form-group row mr-3">
                                            <label for="min" class="col-sm-6 col-form-label col-form-label-sm">Дата скачивания от:</label>
                                            <div class="col-sm-6">
                                                <input type="text" class="myDateInput form-control form-control-sm" name="start_date" id="min" placeholder="">
                                            </div>
                                        </div>
        
                                        <div class="form-group row">
                                            <label for="max" class="col-sm-6 col-form-label col-form-label-sm">Дата скачивания до:</label>
                                            <div class="col-sm-6">
                                                <input type="text" class="myDateInput form-control form-control-sm" name="end_date" id="max" placeholder="">
                                            </div>
                                        </div>
                                    </div>
                                    <table id="range-search" class="display table dt-table-hover" style="width:100%">
                                        <thead>
                                            <tr>
                                                <th>Отчёт</th>
                                                <th>Дата скачивания</th>
                                                <th>Пользователь</th>
                                                <th class="dt-no-sorting">Просмотр файла</th>
                                                <th class="text-center dt-no-sorting">Удалить</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <?foreach($reports as $k=>$v):?>
                                            <tr id="jsDelReportTr<?=$v['id'];?>">
                                                <td><?=$v['title'];?></td>
                                                <td><?=$v['date'];?></td>
                                                <td><?=$v['user'];?></td>
                                                <td>
                                                <?if(!empty($v['file'])):?>
                                                <a href="<?=$v['file'];?>" class="btn btn-primary" target="_blank">Посмотреть</a>
                                                <?endif;?>
                                                </td>
                                                <td class="text-center">
                                                  <span class="jsDelReportBtn" data-id="jsReportId" data-value="<?=$v['id'];?>" data-btn="jsDelReport">
                                                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash-2 table-cancel"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                                                  </span>
                                                </td>
                                            </tr>
                                            <?endforeach;?>
                                        </tbody>
                                        
                                    </table>
                                </div>
                            </div>
                        </div>
                        
                        <form method="post" action="" id="form_jsDelReport" class="hidden">
                         <input type="hidden" name="module" value="reports" />
                         <input type="hidden" name="component" value="" />
                         <input type="hidden" name="ok" value="Отчёт удалён!" />
                         <input type="hidden" name="report_id" id="jsReportId" value="" />
                         <input type="hidden" name="removeElement" id="jsRemoveElement" value="" />
                         
                         <button class="send_form" id="jsDelReport"></button>
                        </form>
  <?endif;?>                  
</div>