<?php defined('DOMAIN') or exit(header('Location: /'));?>
<div class="col-lg-12 layout-spacing">
   <div class="widget-content widget-content-area">

                                    <div class="table-responsive">
                                        <table class="table table-bordered">
                                            <thead>
                                                <tr>
                                                    <th scope="col">Название файла</th>
                                                    <th scope="col">Дата</th>
                                                    <th class="text-center" scope="col">Ссылка</th>
                                                    <th class="text-center" scope="col">Статус</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <?foreach($pf as $val):?>
                                                <tr>
                                                    <td><?=$val['filename'];?></td>
                                                    <td>
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-calendar"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                                                        <span class="table-inner-text"><?=date("H:i d.m.Y",strtotime($val['processed_at']))?></span>
                                                    </td>
                                                    <td class="text-center">
                                                    <a href="<?=DOMAIN;?>/files/<?=$val['filename'];?>" target="_blank">Посмотреть</a>
                                                    </td>
                                                    <td class="text-center">
                                                        <span class="badge badge-light-success"><?=$val['status'];?></span>
                                                    </td>
                                                </tr>
                                                <?endforeach;?>
                                            </tbody>
                                        </table>
                                    </div>
                                    
<form method="post" action="" id="form_jsClearFiles">
  <input type="hidden" name="module" value="upload" />
  <input type="hidden" name="component" value="del" />
  <input type="hidden" name="initAnyPlugin" value="jsUploadFilesFunc" />
  <input type="hidden" name="ok" value="Файлы удалены" />
  <input type="hidden" name="alert" value="" />
  <button class="send_form btn btn-primary mt-2" data-text="Вы уверены, что хотите удалить все файлы?" id="jsClearFiles">Очистить</button>
</form>
                                    
                                    
</div>
</div>