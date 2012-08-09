var settings = require('./settings.js').settings,
    provider = settings['google-oauth2'],
    domain = provider.domain || settings.domain,
    casper = require('casper').create(settings.casper);

casper.start(domain + '/', function () {
    this.click('a#google-oauth2');
});

casper.then(function () {
    this.fill('form#gaia_loginform', {
        'Email': provider.username,
        'Passwd': provider.password
    }, true);
});

casper.then(function () {
    if (this.getCurrentUrl() !== domain + '/done/') {
        // app not authorized yet
        this.click('#submit_approve_access');
    }
});

casper.then(function () {
    this.test.assert(this.getCurrentUrl() === domain + '/done/',
                     'Expected URL');
});

casper.run();
