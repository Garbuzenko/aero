<div class="auth-container d-flex">

        <div class="container mx-auto align-self-center">
    
            <div class="row">
    
                <div class="col-xxl-4 col-xl-5 col-lg-5 col-md-8 col-12 d-flex flex-column align-self-center mx-auto">
                    <div class="card mt-3 mb-3">
                        <div class="card-body">
                            <form method="post" action="" id="form_signIn">
                            <div class="row">
                                <div class="col-md-12 mb-3">
                                    <h2>Авторизация</h2>
                                    <p>Логин и пароль уже введены. Нажмите на кнопку "войти"</p>
                                </div>
                                <div class="col-md-12">
                                    <div class="mb-3">
                                        <label class="form-label">Логин</label>
                                        <input type="text" name="login@" value="admin" class="form-control" />
                                    </div>
                                </div>
                                <div class="col-12">
                                    <div class="mb-4">
                                        <label class="form-label">Пароль</label>
                                        <input type="password" name="pass@" value="aerometr" class="form-control">
                                    </div>
                                </div>
                                <div class="col-12">
                                    <div class="mb-3">
                                        <div class="form-check form-check-primary form-check-inline">
                                            <input class="form-check-input me-3" type="checkbox" id="form-check-default" name="remember" checked="" />
                                            <label class="form-check-label" for="form-check-default">
                                                Запомнить меня
                                            </label>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="col-12">
                                    <div class="mb-4">
                                        <button class="send_form btn btn-secondary w-100" id="signIn">Войти</button>
                                    </div>
                                </div>
                                
                                <div class="col-12 mb-2">
                                    <div class="">
                                        <div class="seperator">
                                            <hr>
                                            <div class="seperator-text"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="col-sm-12 col-12">
                                    <div class="mb-4">
                                        <p>Так же можно авторизоваться как оператор:<br />
                                        Логин: <strong style="color: #fff;">operator</strong><br />
                                        Пароль: <strong style="color: #fff;">aerometr</strong></p>
                                    </div>
                                </div>
                            </div>
                            
                            <input type="hidden" name="module" value="login" />
                            <input type="hidden" name="component" value="" />
                            <input type="hidden" name="url" value="<?=$_SERVER['REQUEST_URI'];?>" />
                            <input type="hidden" name="alert" value="" />
                            
                            </form>
                        </div>
                    </div>
                </div>
                
            </div>
            
        </div>

    </div>