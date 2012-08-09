var casper = require('casper').create({
    verbose: false,
    logLevel: 'debug'
});
var settings = require('./settings.js').settings['google-oauth2'];
var domain = settings.domain;

casper.start(domain + '/', function () {
    this.click('a#google-oauth2');
});

casper.then(function () {
    this.fill('form#gaia_loginform', {
        'Email': settings.username,
        'Passwd': settings.password
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
