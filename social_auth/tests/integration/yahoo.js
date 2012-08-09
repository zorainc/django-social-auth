var settings = require('./settings.js').settings,
    provider = settings.yahoo,
    domain = provider.domain || settings.domain,
    casper = require('casper').create(settings.casper);

casper.start(domain + '/', function () {
    this.click('a#yahoo');
});

casper.then(function () {
    this.fill('form[name="login_form"]', {
        'login': provider.username,
        'passwd': provider.password
    }, true);
});

casper.then(function () {
    if (this.getCurrentUrl() !== domain + '/done/') {
        // app not authorized yet
        this.click('[name="agree"]');
    }
});

casper.then(function () {
    this.test.assert(this.getCurrentUrl() === domain + '/done/',
                     'Expected URL');
});

casper.run();
